Installation
============

While you can install `SQLSorcery <https://pypi.org/project/sqlsorcery/>`_ 
with pip via pypi we encourage the use of `pipenv <https://pipenv.kennethreitz.org/en/latest/>`_ 
because SQLSorcery takes advantage of environment variables for connection 
secrets. 

If you choose to install directly with pip, you will want to install a module 
like `python-dotenv <https://pypi.org/project/python-dotenv/>`_ to handle your 
.env file variables or manage them some other secure way. This cookbook assumes 
use of pipenv and all examples assume you are running your code through the 
pipenv shell.


Installing with Pipenv
----------------------

.. code-block:: bash

    $ pipenv install sqlsorcery

By default sqlsorcery does not install the sql dialect specific python drivers. 
To install these, you can specify the dialects as a comma separated list of each
dialect you will need drivers for.

.. code-block:: bash

    $ pipenv install sqlsorcery[mssql]

OR

.. code-block:: bash

    $ pipenv install sqlsorcery[mysql,postgres]


Additional drivers
------------------

Both Microsoft SQL and Oracle require additional system level drivers 
in order to function.

MS SQL
^^^^^^

You can find directions for installing MS SQL ODBC drivers for various 
systems on `docs.microsoft.com <https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server>`_

**Example for installing in a** `Python Dockerfile <https://hub.docker.com/_/python>`_:

.. code-block:: docker

    FROM python:3                                                                      
    WORKDIR /code                                                                      
    RUN wget https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.4.1.1-1_amd64.deb
    RUN apt-get update                                                                 
    RUN apt-get install -y apt-utils                                                   
    RUN apt-get install -y unixodbc unixodbc-dev                                       
    RUN pip install pipenv                                                             
    COPY Pipfile .                                                                     
    RUN pipenv install --skip-lock                                                     
    RUN yes | dpkg -i msodbcsql17_17.4.1.1-1_amd64.deb                                 
    COPY ./ .                                                                          
    ENTRYPOINT ["pipenv", "run", "python", "main.py"]  

Oracle
^^^^^^

You can find directions for installing Oracle instant-client drivers for 
various systems on `oracle.com <https://www.oracle.com/database/technologies/instant-client/downloads.html>`_

**Example for installing in a** `Python Dockerfile <https://hub.docker.com/_/python>`_:

.. code-block:: docker

    FROM python:3
    WORKDIR /code
    RUN mkdir -p /opt/oracle
    RUN wget https://download.oracle.com/otn_software/linux/instantclient/193000/instantclient-basic-linux.x64-19.3.0.0.0dbru.zip -P /opt/oracle
    RUN cd /opt/oracle && unzip instantclient-basic-linux.x64-19.3.0.0.0dbru.zip
    RUN ln -s /opt/oracle/instantclient_19_3/libclntsh.so.19.1 /opt/oracle/libclntsh.so
    ENV LD_LIBRARY_PATH="/opt/oracle/instantclient_19_3:${LD_LIBRARY_PATH}"
    RUN apt-get update
    RUN apt-get install -y libaio1
    RUN pip install pipenv                                                             
    COPY Pipfile .                                                                     
    RUN pipenv install --skip-lock                                                     
    COPY ./ .                                                                          
    ENTRYPOINT ["pipenv", "run", "python", "main.py"]  