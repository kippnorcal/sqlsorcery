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

```
DB_SERVER=
DB=
DB_USER=
DB_PWD=
```

## Examples

Query a table:

```python
from sqlsorcery import MSSQL


sql = MSSQL()
df = sql.query("SELECT * FROM my_table")
print(df)
```

Query from a `.sql` file:

```python
from sqlsorcery import MSSQL


sql = MSSQL()
df = sql.query("filename.sql")
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
sql = MSSQL()
sql.insert_into("table_name", df) 
```

Execute a stored procedure:

```python
from sqlsorcery import MSSQL


sql = MSSQL()
sql.exec_sproc("sproc_name")
```

