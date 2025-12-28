import sqlite3
from datetime import datetime
from typing import Optional, List

from src.domain.models import FinancialMetric, Company
from src.domain.storage import SQLiteConnectionManager
from src.domain.storage.company_storage import CompanyStorage


class SqliteCompanyStorage(CompanyStorage):

    def __init__(self, connection_manager: SQLiteConnectionManager):
        self.db_manager = connection_manager

    def get(self, company_id: str) -> Optional[Company]:
        with self.db_manager.cursor_context() as cursor:
            # Fetch company description
            cursor.execute("""
                SELECT tax_id, name, kved, opf_code, katottg, region_code, local_code, num_workers
                FROM companies_description
                WHERE tax_id = ?
            """, (company_id,))

            company_row = cursor.fetchone()
            if not company_row:
                return None

            # Unpack company details
            tax_id, name, kved, opf_code, katottg, region_code, local_code, num_workers = company_row

            # Fetch financial metrics
            cursor.execute("""
                SELECT tax_id, my_date, code, value, c_doc_sub
                FROM financial_metrics
                WHERE tax_id = ?
            """, (tax_id,))

            metrics = []
            for row in cursor.fetchall():
                metric_tax_id, my_date_str, code, value, c_doc_sub = row
                # Parse date string to datetime
                date = datetime.strptime(my_date_str, '%Y-%m-%d')
                metrics.append(FinancialMetric(
                    tax_id=metric_tax_id,
                    date=date,
                    code=code,
                    value=value,
                    c_doc_sub=c_doc_sub
                ))

            # Create and return Company instance
            return Company(
                tax_id=tax_id,
                name=name,
                kved=kved,
                opf_code=opf_code,
                katottg=katottg,
                region_code=region_code,
                local_code=local_code,
                num_workers=num_workers,
                financial_metrics=metrics
            )

    def add(self, companies: list[Company]) -> None:
        # Використовуємо транзакцію для атомарного додавання всіх компаній
        with self.db_manager.transaction_context() as connection:
            cursor = connection.cursor()

            for company in companies:
                # Insert company description, ignore if tax_id already exists
                cursor.execute("""
                    INSERT OR IGNORE INTO companies_description
                    (tax_id, name, kved, opf_code, katottg, region_code, local_code, num_workers)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    company.tax_id,
                    company.name,
                    company.kved,
                    company.opf_code,
                    company.katottg,
                    company.region_code,
                    company.local_code,
                    company.num_workers
                ))

                # Insert financial metrics
                for metric in company.financial_metrics:
                    # Format datetime to 'YYYY-MM-DD' for SQLite DATE
                    date_str = metric.date.strftime('%Y-%m-%d')
                    cursor.execute("""
                        INSERT INTO financial_metrics
                        (tax_id, my_date, code, value, c_doc_sub)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        metric.tax_id,
                        date_str,
                        metric.code,
                        metric.value,
                        metric.c_doc_sub
                    ))
