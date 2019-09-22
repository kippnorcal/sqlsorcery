from os import getenv
import urllib
import cx_Oracle
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text


class Connection:
    def exec_sproc(self, stored_procedure):
        sql_str = f"EXEC {self.schema}.{stored_procedure}"
        command = sa_text(sql_str).execution_options(autocommit=True)
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
    def __init__(self, schema="dbo", server=None, db=None, user=None, pwd=None):
        self.server = server or getenv("MS_SERVER") or getenv("DB_SERVER")
        self.db = db or getenv("MS_DB") or getenv("DB")
        self.user = user or getenv("MS_USER") or getenv("DB_USER")
        self.pwd = pwd or getenv("MS_PWD") or getenv("DB_PWD")
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={self.server};DATABASE={self.db};UID={self.user};PWD={self.pwd}"
        )
        self.engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}", isolation_level="AUTOCOMMIT"
        )
        self.schema = schema


class PostgreSQL(Connection):
    def __init__(
        self, schema="public", server=None, port=None, db=None, user=None, pwd=None
    ):
        self.server = server or getenv("PG_SERVER") or getenv("DB_SERVER")
        self.port = port or getenv("PG_PORT") or getenv("DB_PORT")
        self.db = db or getenv("PG_DB") or getenv("DB")
        self.user = user or getenv("PG_USER") or getenv("DB_USER")
        self.pwd = pwd or getenv("PG_PWD") or getenv("DB_PWD")
        sid = f"{self.server}:{self.port}/{self.db}"
        cstr = f"postgres://{self.user}:{self.pwd}@{sid}"
        self.engine = create_engine(cstr)
        self.schema = schema


class Oracle(Connection):
    def __init__(
        self,
        schema="public",
        server=None,
        port=None,
        db=None,
        sid=None,
        user=None,
        pwd=None,
    ):
        self.server = server or getenv("OR_SERVER") or getenv("DB_SERVER")
        self.port = port or getenv("OR_PORT") or getenv("DB_PORT")
        self.sid = sid or getenv("OR_SID") or getenv("DB_SID")
        self.user = user or getenv("OR_USER") or getenv("DB_USER")
        self.pwd = pwd or getenv("OR_PWD") or getenv("DB_PWD")
        self.db = db or getenv("OR_DB") or getenv("DB")
        sid = cx_Oracle.makedsn(self.server, self.port, sid=self.sid)
        cstr = f"oracle://{self.user}:{self.pwd}@{sid}"
        self.engine = create_engine(cstr)
        self.schema = schema
