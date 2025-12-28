import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, Generator
from sqlite3 import Connection, Cursor


class SQLiteConnectionManager:
    """Клас для централізованого управління підключеннями до SQLite бази даних"""

    _instance = None  # Для реалізації Singleton паттерну
    _lock = threading.Lock()  # Блокування для багатопоточності

    def __new__(cls, db_path: Optional[Path] = None):
        """Забезпечує патерн Singleton для DatabaseManager"""
        with cls._lock:
            if cls._instance is None and db_path:
                cls._instance = super(SQLiteConnectionManager, cls).__new__(cls)
                cls._instance.db_path = db_path
                cls._instance.connection = None
                cls._instance._conn_lock = threading.Lock()  # Блокування для з'єднання
            return cls._instance

    def __init__(self, db_path: Optional[Path] = None):
        """Ініціалізує менеджер бази даних"""
        # __new__ вже ініціалізував атрибути для Singleton
        pass

    def get_connection(self) -> Connection:
        """Отримати з'єднання з базою даних"""
        with self._conn_lock:
            if self.connection is None:
                # Додано check_same_thread=False для використання в різних потоках
                self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
                # Встановлення row_factory для доступу до результатів запиту за назвою колонки
                self.connection.row_factory = sqlite3.Row
            return self.connection

    def close_connection(self):
        """Закрити підключення до бази даних"""
        with self._conn_lock:
            if self.connection is not None:
                self.connection.close()
                self.connection = None

    @contextmanager
    def connection_context(self) -> Generator[Connection, None, None]:
        """Контекстний менеджер для безпечної роботи з підключенням"""
        connection = self.get_connection()
        try:
            yield connection
        finally:
            # Тут ми не закриваємо з'єднання, оскільки воно повторно використовується
            pass

    @contextmanager
    def transaction_context(self) -> Generator[Connection, None, None]:
        """Контекстний менеджер для роботи з транзакціями"""
        connection = self.get_connection()
        with self._conn_lock:  # Блокування для безпечних транзакцій
            try:
                yield connection
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    @contextmanager
    def cursor_context(self) -> Generator[Cursor, None, None]:
        """Контекстний менеджер для роботи з курсором"""
        with self.connection_context() as connection:
            with self._conn_lock:  # Блокування для безпечного доступу до курсора
                cursor = connection.cursor()
                try:
                    yield cursor
                finally:
                    cursor.close()
