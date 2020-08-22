README
======

.. image:: https://img.shields.io/badge/python-3.7-blue.svg 
    :target: https://www.python.org/downloads/release/python-370/

.. image:: https://img.shields.io/badge/license-MIT-green
    :target: https://github.com/dchess/sqlsorcery/blob/master/LICENSE

.. image:: https://img.shields.io/static/v1?label=pipenv&message=latest&color=green
    :target: https://pipenv.kennethreitz.org/en/latest/

----

**SQLSorcery**: Dead simple wrapper for pandas and sqlalchemy

SQLSorcery is just some good old fashion syntactic sugar 🍬. It really 
doesn't do anything new. It just makes doing it a little bit easier. It
started as a connection wrapper for SQLAlchemy to cut down on the need for
boilerplate code that was used to keep the database credentials secret,
connect to the database, and then pass the connection to Pandas for 
queries and inserts.

It wasn't much code, but needing to cut and paste it for each new project
seemed like a recipe for bugs. So here we are. We've added more utility 
methods to the module as well as added all of the basic dialects of SQL 
that SQLAlchemy supports.

In many cases, the methods available are less robust than the underlying 
libraries and are more of a shortcut. When you need something that is 
outside the bounds of the defaults you can always drop back down into 
Pandas or SQLAlchemy to get more functionality/flexibility.

Getting Started
---------------

Install this library
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ pipenv install sqlsorcery

By default, **sqlsorcery** does not install the sql dialect specific 
python drivers. To install these, you can specify the dialects as a 
comma separated list of each dialect you will need drivers for.

.. code-block:: bash

    $ pipenv install sqlsorcery[mssql]

OR

.. code-block:: bash

    $ pipenv install sqlsorcery[mysql,postgres]


Setup .env file with credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For use with a single database:

.. code-block:: bash

    DB_SERVER=
    DB_PORT=
    DB=
    DB_SCHEMA=
    DB_USER=
    DB_PWD=

Otherwise, refer to the `documentation <https://sqlsorcery.readthedocs.io/en/latest/cookbook/environment.html>`_ for instructions.

Examples
--------

Query a table
^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL


    sql = MSSQL()
    df = sql.query("SELECT * FROM my_table")
    print(df)


Query from a `.sql` file
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL


    sql = MSSQL()
    df = sql.query_from_file("filename.sql")
    print(df)


Insert into a table
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL
    import pandas as pd


    sample_data = [
        { "name": "Test 1", "value": 98 },
        { "name": "Test 2", "value": 100 },
    ]

    df = pd.DataFrame(sample_data)
    sql = MSSQL()
    sql.insert_into("table_name", df)


Execute a stored procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL


    sql = MSSQL()
    sql.exec_sproc("sproc_name")

Documentation
---------------

Documentation and tutorials available at `sqlsorcery.readthedocs.io <https://sqlsorcery.readthedocs.io/en/latest/>`_
