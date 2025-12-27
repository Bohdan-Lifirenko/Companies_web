import os
import sqlite3
from pathlib import Path
import pandas as pd

from src.domain.source.csv_financial_metric_source import CsvFinancialMetricSource
from src.domain.storage import SqliteCFinancialMetricStorage


def create_db():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    print(f"Loading data from {data_dir}")
    firms_path = data_dir / "firms.csv"
    fin_values_path = data_dir / "fin_values.csv"

    # Крок 2: Читання .csv у DataFrame
    companies_description_df = pd.read_csv(firms_path, dtype=str)  # Всі колонки як рядки, щоб зберегти провідні нулі (наприклад, '00236903')
    financial_metrics_df = pd.read_csv(fin_values_path, dtype=str)

    # Крок 3: Створення бази даних (якщо не існує) і таблиці 'companies_discription'
    db_file = data_dir / 'analytics.db'
    if not os.path.exists(db_file):
        print(f"Створюємо нову базу даних: {db_file}")

    conn = sqlite3.connect(db_file)

    # Create companies_description table
    conn.execute("""
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
    conn.execute("""
    CREATE TABLE IF NOT EXISTS financial_metrics (
        tax_id VARCHAR(8),
        my_date DATE,
        code INTEGER,
        value REAL,
        c_doc_sub VARCHAR(10),
        FOREIGN KEY (tax_id) REFERENCES companies_description(tax_id)
    )
    """)

    cursor = conn.cursor()

    # Fill tables with data from .csv files  # 'replace' — для оновлення, якщо таблиця існує
    table_name = 'companies_description'
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    if not row_count > 0:
        companies_description_df.to_sql('companies_description', conn, if_exists='append', index=False)

    table_name = 'financial_metrics'
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]

    if not row_count > 0:
        financial_metrics_df.to_sql('financial_metrics', conn, if_exists='append', index=False)

    # Крок 4: Перевірка даних (опціонально)
    cursor.execute("PRAGMA table_info(companies_description);")
    columns = cursor.fetchall()

    print("Columns in companies_description table:")
    for col in columns:
        print(col)

    cursor.execute("PRAGMA table_info(financial_metrics);")
    columns = cursor.fetchall()

    print("\nColumns in financial_metrics table:")
    for col in columns:
        print(col)

    cursor.execute("SELECT * FROM companies_description LIMIT 10")
    print("Data from companies_description table:")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM financial_metrics LIMIT 10")
    print("\nData from financial_metrics table:")
    print(cursor.fetchall())

    conn.close()

def get_company_revenue(db_file, tax_id_value, code_value):
    """
    Повертає стовпці my_date і value з таблиці financial_metrics
    для заданого tax_id і code.
    """
    conn = sqlite3.connect(db_file)

    query = """
    SELECT my_date, value
    FROM financial_metrics
    WHERE tax_id = ? AND code = ?
    """

    # Використовуємо pandas для зручності
    df = pd.read_sql_query(query, conn, params=(tax_id_value, code_value))

    conn.close()
    return df

if __name__ == '__main__':
    create_db()

    data_dir = Path(__file__).resolve().parent.parent / "data"
    db_file = data_dir / 'analytics.db'
    revenue_df = get_company_revenue(db_file, '00236903', 2000)
    print(revenue_df)

    sql_db = SqliteCFinancialMetricStorage(sqlite3.connect(db_file))
    revenue_list = sql_db.get_company_revenue_statistic('00236903')
    print(revenue_list)

    csvmf = CsvFinancialMetricSource(data_dir / 'fin_values.csv')
    metrics = csvmf.get_fin_metrics()
    print(metrics)

