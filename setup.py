from setuptools import setup

setup(name='sqlsorcery',
      version='0.1',
      description='Dead simple wrapper for pandas and sqlalchemy',
      url='http://github.com/dchess/sqlsorcery',
      author='dchess',
      author_email='dc.hess@gmail.com',
      license='MIT',
      packages=['sqlsorcery'],
      install_requires=['pandas', 'sqlalchemy', 'pyodbc'],
      zip_safe=False)
