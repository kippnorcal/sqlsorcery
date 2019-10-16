README
======
SQLSorcery: Dead simple wrapper for pandas and sqlalchemy

Dependencies
^^^^^^^^^^^^

* Python3.7
* Pipenv
* MS SQL odbc driver (optional)

Getting Started
^^^^^^^^^^^^^^^

1. Install this library

.. code-block:: bash

    $ pipenv install sqlsorcery

By default sqlsorcery does not install the sql dialect specific python drivers. 
To install these, you can specify the dialects as a comma separated list of each
dialect you will need drivers for.

.. code-block:: bash

    $ pipenv install sqlsorcery[mssql]

OR

.. code-block:: bash

    $ pipenv install sqlsorcery[msql,postgres]


2. Install MS SQL Drivers

.. code-block:: bash

    wget https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.2.0.1-1_amd64.deb 
    apt-get update
    apt-get install -y apt-utils unixodbc unixodbc-dev
    yes | dpkg -i msodbcsql17_17.2.0.1-1_amd64.deb


3. Setup a `.env` file with environment credentials

Single database environment:

.. code-block:: bash

    DB_SERVER=
    DB_PORT=
    DB=
    DB_SCHEMA=
    DB_USER=
    DB_PWD=


For multi-database environment, use sql specific prefixes or specify connect vars at instantiation:

.. code-block:: bash

    PG_SERVER=
    PG_PORT=
    PG_DB=
    PG_SCHEMA=
    PG_USER=
    PG_PWD=

    MS_SERVER=
    MS_DB=
    MS_SCHEMA=
    MS_USER=
    MS_PWD=

or

.. code-block:: python

    from sqlsorcery import MSSQL

    conn = MSSQL(server="server_host", db="db_name", schema="schema", user="username", pwd="password")


Examples
^^^^^^^^

Query a table:

.. code-block:: python

    from sqlsorcery import MSSQL


    conn = MSSQL()
    df = conn.query("SELECT * FROM my_table")
    print(df)


Query from a `.sql` file:

.. code-block:: python

    from sqlsorcery import MSSQL


    conn = MSSQL()
    df = conn.query_from_file("filename.sql")
    print(df)


Insert into a table:

.. code-block:: python

    from sqlsorcery import MSSQL
    import pandas as pd


    sample_data = [
        { "name": "Test 1", "value": 98 },
        { "name": "Test 2", "value": 100 },
    ]

    df = pd.DataFrame(sample_data)
    conn = MSSQL()
    conn.insert_into("table_name", df) 


Execute a stored procedure:

.. code-block:: python

    from sqlsorcery import MSSQL


    conn = MSSQL()
    conn.exec_sproc("sproc_name")
