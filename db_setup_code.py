import pyodbc
from abc import ABC, abstractmethod
from typing import Generator

class BaseDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def read(self, query):
        pass

    @abstractmethod
    def stream_read(self, query):
        pass

    @abstractmethod
    def insert(self, query, params):
        pass

    @abstractmethod
    def update(self, query, params):
        pass

    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def close(self):
        pass

class SQLServerDB(BaseDBInterface):
    def __init__(self, server, database, username='', password='', driver='{ODBC Driver 17 for SQL Server}'):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.username:
            conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        else:
            conn_str = f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'

        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def stream_read(self, query) -> Generator:
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row:
            yield row
            row = self.cursor.fetchone()

    def insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def update(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
