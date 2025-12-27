import sqlite3
from datetime import datetime

from src.domain.models import FinancialMetric, Revenue
from src.domain.storage.financial_metric_storage import FinancialMetricStorage


class SqlCFinancialMetricStorage(FinancialMetricStorage):

    _instance = None  # Змінна для зберігання єдиного екземпляра

    def __new__(cls, db_connection, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False  # Для контролю ініціалізації
        return cls._instance

    def __init__(self, db_connection):
        if self._initialized:
            return  # Якщо об'єкт вже ініціалізований, нічого не робимо
        self.db_connection = db_connection
        self._initialized = True

    def get_company_revenue_statistic(self, company_id: int) -> list[Revenue]:
        """
            Повертає стовпці my_date і value з таблиці financial_metrics
            для заданого tax_id і code.
            """
        conn = self.db_connection

        cursor = conn.cursor()

        query = """
            SELECT my_date, value
            FROM financial_metrics
            WHERE tax_id = ? AND code = ?
            """

        revenue_code = 2000
        cursor.execute(query, (company_id, revenue_code))
        rows = cursor.fetchall()

        revenue_list = []
        for my_date, value in rows:
            # Перетворюємо my_date у datetime
            date_obj = datetime.strptime(my_date, "%Y-%m-%d")
            revenue_list.append(Revenue(date=date_obj, value=float(value)))

        conn.close()
        return revenue_list
