import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Generator
from sqlite3 import Connection, Cursor


class SQLiteConnectionManager:
    """Class for centralized management of connections to SQLite databases"""

    _instance = None  # To implement the Singleton pattern
    _lock = threading.Lock()  # Locks for multithreading

    def __new__(cls, db_path: Optional[Path] = None):
        """Provides the Singleton pattern for DatabaseManager"""
        with cls._lock:
            if cls._instance is None and db_path:
                cls._instance = super(SQLiteConnectionManager, cls).__new__(cls)
                cls._instance.db_path = db_path
                cls._instance.connection = None
                cls._instance._conn_lock = threading.Lock()  # Locks for connection
            return cls._instance

    def __init__(self, db_path: Optional[Path] = None):
        """Initializes the database manager"""
        # __new__ has already initialized the attributes for Singleton
        pass

    def get_connection(self) -> Connection:
        """Connect to the database"""
        with self._conn_lock:
            if self.connection is None:
                # Added check_same_thread=False for use in different threads
                self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
                # Setting row_factory to access query results by column name
                self.connection.row_factory = sqlite3.Row
            return self.connection

    def close_connection(self):
        """Close connection to database"""
        with self._conn_lock:
            if self.connection is not None:
                self.connection.close()
                self.connection = None

    @contextmanager
    def connection_context(self) -> Generator[Connection, None, None]:
        """Contextual manager for secure connection management"""
        connection = self.get_connection()
        try:
            yield connection
        finally:
            # do not close the connection, as it is reused
            pass

    @contextmanager
    def transaction_context(self) -> Generator[Connection, None, None]:
        """Context manager for working with transactions"""
        connection = self.get_connection()
        with self._conn_lock:  # Blocking for secure transactions
            try:
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    @contextmanager
    def cursor_context(self) -> Generator[Cursor, None, None]:
        """Context manager for working with the cursor"""
        with self.connection_context() as connection:
            with self._conn_lock:  # Lock for secure access to the cursor
                cursor = connection.cursor()
                try:
                    yield cursor
                finally:
                    cursor.close()
