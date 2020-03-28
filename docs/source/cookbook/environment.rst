Environment
===========

Storing your progam's config in the environment is a common practice 
for several reasons:

1. You can add your `.env` to your `.gitignore` to ensure credentials and other project secrets don't end up exposed in your remote repository.
2. It makes it easier to add environment specific variables (development vs. production)
3. Separates config from code. Config varies across deploys, code does not.

One way to leverage environment variables as your config is to store them in 
a `.env` file. This file acts like a dictionary of key/value pairs which 
exist outside of the program. 

`Pipenv <https://pipenv.readthedocs.io/en/latest/advanced/#automatic-loading-of-env>`_ 
has native support for loading these variables at runtime. SQLSorcery 
leverages these for config by default, but you can also set them 
manually in your environment or use an alternative library like 
`python-dotenv <https://pypi.org/project/python-dotenv/>`_ if preferred.

Setup a `.env` file
-------------------

SQLSorcery takes a convention over configuration approach for locating
the correct environment variables. Environment variables are specified 
with a generic (`DB_`) or specific (`MS_`, `OR_`, etc.) prefix for each
connection parameter.

SQLSorcery looks for connection params in the following order:

1. specified at object instantiation
2. using the specific dialect prefix
3. using the generic `DB_` prefix

Generic env vars
^^^^^^^^^^^^^^^^

This is the simplest method for specifying connection variables
and works best when you need to connect to a single SQL database.

.. code-block:: bash

    DB_SERVER=
    DB_PORT=
    DB=
    DB_SCHEMA=
    DB_USER=
    DB_PWD=

Dialect specific env vars
^^^^^^^^^^^^^^^^^^^^^^^^^

For a list of each dialect's required variables see each dialect
listed below. This is also useful when doing database-to-database
ETL work or when doing cross-database analysis in `pandas` because
you can combine the params in your `.env` file for easy management.

**Microsoft (MS SQL)**

.. code-block:: bash

    MS_SERVER=
    MS_PORT=
    MS_DB=
    MS_SCHEMA=
    MS_USER=
    MS_PWD=

**MySQL**

.. code-block:: bash

    MY_SERVER=
    MY_PORT=
    MY_DB=
    MY_USER=
    MY_PWD=

**Oracle (PL/SQL)**

.. code-block:: bash

    OR_SERVER=
    OR_PORT=
    OR_SCHEMA=
    OR_SID=
    OR_USER=
    OR_PWD=

**PostgreSQL**

.. code-block:: bash

    PG_SERVER=
    PG_PORT=
    PG_DB=
    PG_SCHEMA=
    PG_USER=
    PG_PWD=

**Google BigQuery**

BigQuery uses dataset similar to how the others use schema. For autorization
a json credentials file is needed. The filepath is passed as the creds var.

.. code-block:: bash

    BQ_DATASET=
    BQ_CREDS=

**SQLite**

SQLite only requires a filepath to connect. It is generally unnecessary
to specify via an env var.