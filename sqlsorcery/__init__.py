from os import getenv
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text


class Connection:
    def exec_sproc(self, stored_procedure):
        sql_str = f"EXEC {self.schema}.{stored_procedure}"
        command = sa_text(sql_str)
        return self.engine.execute(command)

    def _read_sql_file(self, filename):
        with open(filename) as f:
            return f.read()

    def query(self, sql_string):
        df = pd.read_sql_query(sql_string, self.engine)
        return df

    def query_from_file(self, filename):
        sql_statement = self._read_sql_file(filename)
        df = pd.read_sql_query(sql_statement, self.engine)
        return df

    def insert_into(self, table, df, if_exists="append"):
        df.to_sql(
            table, self.engine, schema=self.schema, if_exists=if_exists, index=False
        )


class MSSQL(Connection):
    def __init__(self, schema=None, server=None, db=None, user=None, pwd=None):
        self.server = server or getenv("MS_SERVER") or getenv("DB_SERVER")
        self.db = db or getenv("MS_DB") or getenv("DB")
        self.user = user or getenv("MS_USER") or getenv("DB_USER")
        self.pwd = pwd or getenv("MS_PWD") or getenv("DB_PWD")
        self.schema = schema or getenv("MS_SCHEMA") or getenv("DB_SCHEMA") or "dbo"
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={self.server};DATABASE={self.db};UID={self.user};PWD={self.pwd}"
        )
        self.engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}", isolation_level="AUTOCOMMIT"
        )

class PostgreSQL(Connection):
    def __init__(self, schema=None, server=None, port=None, db=None, user=None, pwd=None):
        self.server = server or getenv("PG_SERVER") or getenv("DB_SERVER")
        self.port = port or getenv("PG_PORT") or getenv("DB_PORT")
        self.db = db or getenv("PG_DB") or getenv("DB")
        self.user = user or getenv("PG_USER") or getenv("DB_USER")
        self.pwd = pwd or getenv("PG_PWD") or getenv("DB_PWD")
        self.schema = schema or getenv("PG_SCHEMA") or getenv("DB_SCHEMA") or "public"
        sid = f'{self.server}:{self.port}/{self.db}'
        cstr = f'postgres://{self.user}:{self.pwd}@{sid}'
        self.engine =  create_engine(cstr)

