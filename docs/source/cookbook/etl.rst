ETL
===

SQLSorcery is also useful for simple script based ETL actions. 

.. note:: Keep in mind performance constraints when attempting 
    bulk insertions. Postgres and MSSQL have bulk insert configs
    defaulted but they can fail on very large inserts if used with
    limited memory. You can override this setting by passing 
    :code:`bulk_insert=False` to the connection class.

Insert csv to table
-------------------
Insert ~1 million `IMDB ratings <https://datasets.imdbws.com/title.ratings.tsv.gz>`_ 
into a MySQL table.

.. code-block:: python
    :linenos:

    from sqlsorcery import MySQL
    import pandas as pd

    sql = MySQL()
    df = pd.read_csv("title.ratings.tsv", sep="\t")
    sql.insert_into("ratings", df)


Copy table between databases
----------------------------
Copy the contents of a query in one database to another:

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL, PostgreSQL

    ms = MSSQL()
    pg = PostgreSQL()

    df = pg.query("SELECT * FROM tablename")
    ms.insert_into("new_table", df)


Query API endpoint and load into table
--------------------------------------

.. code-block:: python
    :linenos:

    import requests
    import pandas as pd
    from sqlsorcery import SQLite

    sql = SQLite(path="example.db")

    response = requests.get("https://swapi.co/api/people/").json()
    next_page = response["next"]

    while next_page:
        response = requests.get(next_page).json()
        results = response["results"]
        next_page = response["next"]

        df = pd.DataFrame(results)
        df["film_appearances"] = len(df["films"])
        df = df[["name", "gender", "film_appearances"]]
        sql.insert_into("star_wars", df)

Update table values
-------------------
It is often necessary to modify existing records in a table after
loading. There are several ways to accomplish this in SQLSorcery
depending on your use case including issuing raw commands or 
embedding within a stored procedure.

Via SQLAlchemy 
^^^^^^^^^^^^^^
.. code-block:: python
    :linenos:

    import datetime
    from sqlsorcery import MSSQL
    import pandas as pd
    

    sql = MSSQL()
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df)
    table = sql.table("ratings_cache")
    # Adds today's date as the datestamp to all records
    table.update().values(datestamp=datetime.date.today())

OR you could specify an additional :code:`WHERE` clause

.. code-block:: python

    # If you wanted to override a specific rating
    table.update().where(table.c.name=="Top Gun").values(avgRating="10")

Via pandas
^^^^^^^^^^
With this scenario you would just modify the dataframe in memory
before inserting into the database. This has trade-offs for 
performance as well as traceability.

.. code-block:: python
    :linenos:

    import datetime
    from sqlsorcery import MSSQL
    import pandas as pd
    

    sql = MSSQL()
    df = pd.read_csv("daily_ratings.csv")
    df["datestamp"] = datetime.date.today()
    sql.insert_into("ratings_cache", df)

Via command
^^^^^^^^^^^

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL
    import pandas as pd
    

    sql = MSSQL()
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df)
    sql.exec_cmd("UPDATE ratings_cache SET datestamp = GETDATE()")

Truncate a table
----------------
It is often desirable to empty a table's contents before
loading additional records during an ETL process. This is
commonly used in conjuntion with a cache table which will
be further transformed after the raw data is loaded into the
database.

There are several ways to accomplish this in SQLSorcery
depending on your use case.

Drop and replace during insert
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL
    import pandas as pd

    sql = MSSQL()
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df, if_exists="replace")

Truncate all records
^^^^^^^^^^^^^^^^^^^^
Most databases support :code:`TRUNCATE TABLE` statements which
differ from :code:`DELETE FROM` statements in how logging and
diskspace is handled. A truncate will also reset any identity
column on the table.

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL
    import pandas as pd

    sql = MSSQL()
    sql.truncate("ratings_cache")
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df)

Delete all records
^^^^^^^^^^^^^^^^^^
This will flush the table's contents, but will not reset the values in
the identity column (such as an id or primary key). This is useful if
you will want the insert to fail if the schema has changed.

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL
    import pandas as pd

    sql = MSSQL()
    sql.delete("ratings_cache")
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df)

Delete specific records
^^^^^^^^^^^^^^^^^^^^^^^
You might also find it necessary to only delete a subset of records.
To do so you can drop down into `SQLAlchemy` to pass a :code:`WHERE`
clause.


.. code-block:: python
    :linenos:

    import datetime
    from sqlsorcery import MSSQL
    import pandas as pd
    

    sql = MSSQL()
    table = sql.table("ratings_cache")
    table.delete().where(table.c.datestamp == datetime.date.today())
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df)

Execute a stored procedure
--------------------------

The following command will execute a stored procedure called 
`sproc_upsert_ratings` which merges data from a daily cache
table of movie ratings into longitudinal table which stores
all the daily results over time.

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL
    import pandas as pd

    sql = MSSQL()
    df = pd.read_csv("daily_ratings.csv")
    sql.insert_into("ratings_cache", df, if_exists="replace")
    sql.exec_sproc("sproc_upsert_ratings")

The content of this stored procedure might look like:

.. code-block:: sql
    :linenos:

    IF OBJECT_ID('sproc_upsert_ratings') IS NULL
        EXEC('CREATE PROCEDURE sproc_upsert_ratings AS SET NOCOUNT ON;')
    GO
    
    ALTER PROCEDURE dbo.sproc_upsert_ratings AS
    BEGIN  
        SET NOCOUNT ON;  
  
        MERGE dbo.factRatings AS target  
        USING dbo.ratings_cache AS source 
        ON (target.id = source.id)  
        WHEN MATCHED THEN
            UPDATE SET name = source.Name
                ,avgRating = source.avgRating
                ,numVotes = source.numVotes
        WHEN NOT MATCHED THEN  
            INSERT (id, name, avgRating, numVotes)
            VALUES (source.id, source.name, source.avgRating, source.numVotes) 
    END; 

Execute any arbitrary command 
-----------------------------
Any valid SQL command can be passed raw to be executed. This is a catch
all for things like function calls, create, or drop commands, etc.

Create a table from SQL command string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL

    sql = MSSQL()

    table = """
        CREATE TABLE star_wars (
            name VARCHAR(100) NULL,
            gender VARCHAR(25) NULL,
            film_appearances INT NULL
        )
    """
    sql.exec_cmd(table)

Create a table from a .sql file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming you have a `.sql` file named `table.auth_user.sql`:

.. code-block:: sql
    :linenos:

    CREATE TABLE IF NOT EXISTS auth_user (
        id SERIAL NOT NULL CONSTRAINT auth_user_pkey PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        last_login TIMESTAMP WITH TIME ZONE,
        is_superuser BOOLEAN NOT NULL,
        username VARCHAR(150)NOT NULL CONSTRAINT auth_user_username_key UNIQUE,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(150) NOT NULL,
        email VARCHAR(254) NOT NULL,
        is_staff BOOLEAN NOT NULL,
        is_active BOOLEAN NOT NULL,
        date_joined TIMESTAMP WITH TIME ZONE NOT NULL
    );

    ALTER TABLE auth_user OWNER TO admin;

    CREATE INDEX IF NOT EXISTS auth_user_username_idx ON auth_user (username);

You can execute it like so:

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL

    sql = MSSQL()
    sql.exec_cmd_from_file("table.auth_user.sql")


Drop a table from SQL command string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:

    from sqlsorcery import MSSQL

    sql = MSSQL()
    sql.exec_cmd("DROP TABLE star_wars")