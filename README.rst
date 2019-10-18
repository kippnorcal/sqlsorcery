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

Getting Started
---------------

Install this library
^^^^^^^^^^^^^^^^^^^^

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


    conn = MSSQL()
    df = conn.query("SELECT * FROM my_table")
    print(df)


Query from a `.sql` file
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL


    conn = MSSQL()
    df = conn.query_from_file("filename.sql")
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
    conn = MSSQL()
    conn.insert_into("table_name", df) 


Execute a stored procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from sqlsorcery import MSSQL


    conn = MSSQL()
    conn.exec_sproc("sproc_name")

Documentation
---------------

Documentation and tutorials available at `sqlsorcery.readthedocs.io <https://sqlsorcery.readthedocs.io/en/latest/>`_