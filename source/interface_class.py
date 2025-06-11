from source.base_class import BaseDBInterface
import pyodbc
from typing import Generator, Any, List

class SQLServerDB(BaseDBInterface):
    def __init__(self, server, database, username='', password='', driver='{ODBC Driver 17 for SQL Server}') -> None:
        '''Initialize the SQL Server database interface.'''
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.conn = None
        self.cursor = None

    def __enter__(self):
        '''Support for context manager (with statement).'''
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Ensure clean resource release.'''
        self.close()

    def connect(self):
        '''Establish a connection to the SQL Server database.'''
        try:
            if self.username:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            else:
                conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'

            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Connection failed: {e}")
            raise

    def read(self, query) -> List[dict]:
        '''Execute a read query and return the results as list of dicts.'''
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Read failed: {e}")
            raise

    def stream_read(self, query: str, batch_size: int = 100) -> List[tuple]:
        '''Reads first batch of rows. Call repeatedly to get next batch.'''
        try:
            if not hasattr(self, "_active_query") or self._active_query != query:
                self._active_query = query
                self.cursor.execute(query)
            return self.cursor.fetchmany(batch_size)
        except Exception as e:
            print(f"Stream read failed: {e}")
            raise

    def insert(self, query, params) -> None:
        '''Execute an insert query with parameters.'''
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Insert failed: {e}")
            self.conn.rollback()
            raise

    def update(self, query, params) -> None:
        '''Execute an update query with parameters.'''
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Update failed: {e}")
            self.conn.rollback()
            raise

    def execute(self, query) -> None:
        '''Execute a query that does not return results (e.g., DDL statements).'''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Execution failed: {e}")
            self.conn.rollback()
            raise

    def bulk_upsert(self, query, params_list):
        '''
        Execute bulk UPSERT query using MERGE.
        Each item in params_list is a tuple of values for the source.
        '''
        try:
            for params in params_list:
                self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Bulk upsert failed: {e}")
            self.conn.rollback()
            raise

    def close(self) -> None:
        '''Close the database connection and cursor.'''
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
