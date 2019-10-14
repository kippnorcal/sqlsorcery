from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sqlsorcery",
    version="0.1.3",
    description="Dead simple wrapper for pandas and sqlalchemy",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="http://github.com/dchess/sqlsorcery",
    author="dchess",
    author_email="dc.hess@gmail.com",
    license="MIT",
    packages=["sqlsorcery"],
    install_requires=["pandas", "sqlalchemy"],
    extras_require={
        "postgres": ["psycopg2-binary"],
        "mssql": ["pyodbc"],
        "mysql": ["PyMySQL"],
        "oracle": ["cx_Oracle"],
    },
    zip_safe=False,
)
