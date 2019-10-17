ETL
===

SQLSorcery is also useful for simple script based ETL actions. 

.. note:: Keep in mind performance constraints when attempting 
    bulk insertions. 

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

Performance Testing
^^^^^^^^^^^^^^^^^^^

The following bulk insert metrics were gathered using two datasets from IMDB:

1. **medium sized**: `title.ratings.tsv <https://datasets.imdbws.com/title.ratings.tsv.gz>`_ 16MB ~980K records
2. **large sized**: `title.basics.tsv <https://datasets.imdbws.com/title.basics.tsv.gz>`_ 506MB ~6.2m records

Elapsed time to insert was measured using unix time command.

.. code-block:: bash

    $ time pipenv run python main.py

================= =========== ==========
Database          Medium Size Large Size
================= =========== ==========
**Microsoft SQL**                         
**MySQL**         0m34.074s   6m35.116s   
**Oracle**                                         
**PostgreSQL**                                     
**SQLite**        0m10.381s   2m13.472s                      
================= =========== ==========

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

Dynamic update
^^^^^^^^^^^^^^

Complex but static update
^^^^^^^^^^^^^^^^^^^^^^^^^

Truncate a table
----------------

Execute a stored procedure
--------------------------

*Upsert example*

Execute any arbitrary command 
-----------------------------
Any valid SQL command can be passed raw to be executed. This is a catch
all for things like function calls, create, or drop commands, etc.

Example: Create a table from SQL command string
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

Example: Create a table from a .sql file
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