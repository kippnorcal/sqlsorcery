# sqlsorcery
Dead simple wrapper for pandas and sqlalchemy

## Dependencies

* Python3.7
* Pipenv
* MS SQL odbc driver

## Getting Started

1. Install this library

```
$ pipenv install sqlsorcery
```

2. Install MS SQL Drivers

```
wget https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.2.0.1-1_amd64.deb 
apt-get update
apt-get install -y apt-utils unixodbc unixodbc-dev
yes | dpkg -i msodbcsql17_17.2.0.1-1_amd64.deb
```

3. Setup a `.env` file with environment credentials

Single database environment:
```
DB_SERVER=
DB_PORT=
DB=
DB_SCHEMA=
DB_USER=
DB_PWD=
```

For multi-database environment, use sql specific prefixes or specify connect vars at instantiation:
```
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
```
or

```python
from sqlsorcery import MSSQL

conn = MSSQL(server="server_host", db="dba_name", schema="schema", user="username", pwd="password")
```

## Examples

Query a table:

```python
from sqlsorcery import MSSQL


conn = MSSQL()
df = conn.query("SELECT * FROM my_table")
print(df)
```

Query from a `.sql` file:

```python
from sqlsorcery import MSSQL


conn = MSSQL()
df = conn.query_from_file("filename.sql")
print(df)
```


Insert into a table:

```python
from sqlsorcery import MSSQL
import pandas as pd


sample_data = [
    { "name": "Test 1", "value": 98 },
    { "name": "Test 2", "value": 100 },
]

df = pd.DataFrame(sample_data)
conn = MSSQL()
conn.insert_into("table_name", df) 
```

Execute a stored procedure:

```python
from sqlsorcery import MSSQL


conn = MSSQL()
conn.exec_sproc("sproc_name")
```

