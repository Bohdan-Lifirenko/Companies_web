import sqlite3
from pathlib import Path

from src.domain.storage import SQLiteConnectionManager


class CompanyStorageInitializer:
    @staticmethod
    def init(connection_manager: SQLiteConnectionManager):
        with connection_manager.transaction_context() as connection:
            # Create companies_description table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS companies_description (
                    tax_id VARCHAR(8) PRIMARY KEY,
                    name TEXT,
                    kved VARCHAR(10),
                    opf_code VARCHAR(10),
                    katottg VARCHAR(20),
                    region_code VARCHAR(10),
                    local_code VARCHAR(10),
                    num_workers INTEGER
                )
                """)

            # create financial_metrics table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS financial_metrics (
                    tax_id VARCHAR(8),
                    my_date DATE,
                    code INTEGER,
                    value REAL,
                    c_doc_sub VARCHAR(10),
                    FOREIGN KEY (tax_id) REFERENCES companies_description(tax_id)
                )
                """)

            # Додаємо індекси для покращення продуктивності
            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_financial_metrics_tax_id
                ON financial_metrics(tax_id)
                """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_financial_metrics_date
                ON financial_metrics(my_date)
                """)
