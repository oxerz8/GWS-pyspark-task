from abc import ABC, abstractmethod

class BaseDBInterface(ABC):
    """Abstract base class to define a database interface."""

    @abstractmethod
    def connect(self):
        """Establish DB connection"""
        pass

    @abstractmethod
    def read(self, query):
        """Execute SELECT query and return all results"""
        pass

    @abstractmethod
    def stream_read(self, query):
        """Execute SELECT query and yield results row-by-row"""
        pass

    @abstractmethod
    def insert(self, query, params):
        """Execute INSERT query with parameters"""
        pass

    @abstractmethod
    def bulk_upsert(self, query, params):
        """Execute bulk UPSERT query with parameters"""
        pass

    @abstractmethod
    def update(self, query, params):
        """Execute UPDATE query with parameters"""
        pass

    @abstractmethod
    def execute(self, query):
        """Execute generic DDL/DML (create, drop, call, etc.)"""
        pass

    @abstractmethod
    def close(self):
        """Close the DB connection"""
        pass
