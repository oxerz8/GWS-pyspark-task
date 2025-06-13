from source.base_class import BaseDBInterface
import pyodbc
from typing import List

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

    def read(self, query_or_table: str) -> List[dict]:
        """
        Execute a read query and return the results as list of dicts.
        If only a table name is provided, it selects all rows.
        """
        try:
            # Auto-generate SELECT * if a plain table name is provided
            if not query_or_table.strip().lower().startswith("select"):
                query = f"SELECT * FROM {query_or_table}"
            else:
                query = query_or_table

            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            rows = self.cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            print(f"Read failed: {e}")
            raise

    def stream_read(self, query_or_table: str, batch_size: int = 100) -> List[tuple]:
        '''
        Reads a batch of rows from a query or table.
        If a table name is provided, it defaults to SELECT * FROM table.
        Call repeatedly to get the next batch.
        '''
        try:
            # Construct query if input is just a table name
            if not query_or_table.strip().lower().startswith("select"):
                query = f"SELECT * FROM {query_or_table}"
            else:
                query = query_or_table

            # Only execute if it's a new query
            if not hasattr(self, "_active_query") or self._active_query != query:
                self._active_query = query
                self.cursor.execute(query)

            return self.cursor.fetchmany(batch_size)

        except Exception as e:
            print(f"Stream read failed: {e}")
            raise

    def insert(self, query_or_table, params) -> None:
        '''Insert into a table using full query or just table name.'''
        try:
            if not query_or_table.strip().lower().startswith("insert"):
                # Build query from table name and number of params
                placeholders = ', '.join(['?' for _ in params])
                query = f"INSERT INTO {query_or_table} VALUES ({placeholders})"
            else:
                query = query_or_table

            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Insert failed: {e}")
            self.conn.rollback()
            raise

    def update(self, table: str, updates: dict, condition: str, condition_params: tuple) -> None:
        '''Update specific columns in a table where condition is met.'''
        try:
            set_clause = ', '.join([f"{col} = ?" for col in updates])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            params = tuple(updates.values()) + condition_params
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

    def bulk_upsert(self, table: str, columns: list, match_column: str, params_list: list[tuple]) -> None:
        '''
        Perform a bulk upsert (MERGE) into the given table using the specified columns.

        Args:
            table: Table name.
            columns: List of column names (order must match the tuple).
            match_column: Column to match for upsert (must be in columns).
            params_list: List of tuples with values.
        '''
        try:
            col_str = ', '.join(columns)
            val_placeholders = ', '.join(['?' for _ in columns])

            update_str = ', '.join(f'target.{col} = source.{col}' for col in columns if col != match_column)

            merge_query = f"""
            MERGE {table} AS target
            USING (SELECT {val_placeholders}) AS source ({col_str})
            ON target.{match_column} = source.{match_column}
            WHEN MATCHED THEN
                UPDATE SET {update_str}
            WHEN NOT MATCHED THEN
                INSERT ({col_str}) VALUES ({val_placeholders});
            """

            for params in params_list:
                self.cursor.execute(merge_query, params * 2)  # one for SELECT, one for INSERT
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
