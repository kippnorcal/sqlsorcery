from os import getenv
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text


class Connection:
    def __init__(self):
        self.server = getenv("DB_SERVER")
        self.db = getenv("DB")
        self.user = getenv("DB_USER")
        self.pwd = getenv("DB_PWD")

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
    def __init__(self, schema="dbo"):
        super().__init__()
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={self.server};DATABASE={self.db};UID={self.user};PWD={self.pwd}"
        )
        self.engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}", isolation_level="AUTOCOMMIT"
        )
        self.schema = schema
