Queries
=======

SQLSorcery is designed to simplify data analysis and script based ETL.
A common need in both is the ability to run queries against database 
tables or views.

Connect to the database
-----------------------
If using a `.env` file:

.. code-block:: python
    :linenos:   

    from sqlsorcery import PostgreSQL

    sql = PostgreSQL()

If specifying at object instantiation:

.. code-block:: python
    :linenos:   

    from sqlsorcery import PostgreSQL

    sql = PostgreSQL(server="ip or url", port="port number", db="database name", schema="schema name", user="username", pwd="password")

.. warning:: It is generally inadvisable to specify connection variables directly in your code.  

Query from a string
-------------------
Reads a database table into a pandas dataframe and prints to console:

.. code-block:: python
    :linenos:   

    from sqlsorcery import PostgreSQL

    sql = PostgreSQL()
    df = sql.query("SELECT * FROM tablename")
    print(df)


Query from a .sql file
----------------------

If you had a `.sql` file with the following query named `user_location.sql`:

.. code-block:: sql
    :linenos:

    SELECT
          u.id
        , u.username
        , l.latitude
        , l.longitude
        , l.ip_address
        , u.is_staff
    FROM users u
    INNER JOIN location l
        ON u.id = l.user_id
    WHERE u.is_staff = false

You could query with it like so:

.. code-block:: python
    :linenos:   

    from sqlsorcery import PostgreSQL

    sql = PostgreSQL()
    df = sql.query_from_file("user_location.sql")
    print(df)


Query a view
------------

If that previous `.sql` file was a view in the database called `vw_user_location`
you could query it like so:

.. code-block:: python
    :linenos:   

    from sqlsorcery import PostgreSQL

    sql = PostgreSQL()
    df = sql.query("SELECT * FROM vw_user_location")
    print(df)