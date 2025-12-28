import os
import sqlite3
from pathlib import Path
import pandas as pd
from flask import Flask, render_template

from src.domain.controler.company_controller import CompanyController
from src.domain.service import CompanyService
from src.domain.source.csv_company_source import CSVCompanySource
from src.domain.storage import CompanyStorageInitializer
from src.domain.storage.sqllite_company_storage import SqliteCompanyStorage

app = Flask(__name__)

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

    cursor = conn.cursor()
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

@app.route('/search/<company_id>')
def company(company_id):

    return render_template('company.html', company_id=company_id)

if __name__ == '__main__':
    # Choose db file location
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    db_file = DATA_DIR / 'analytics.db'

    print(f"Loading data from {DATA_DIR}")

    # Creating db connection
    db_connection = sqlite3.connect(db_file, check_same_thread=False)

    # Initialize db
    CompanyStorageInitializer.init(db_connection)

    # Getting data from source
    firms_path = DATA_DIR / "firms.csv"
    fin_values_path = DATA_DIR / "fin_values.csv"
    company_source = CSVCompanySource(firms_path, fin_values_path)

    # Create storage
    company_storage = SqliteCompanyStorage(db_connection)
    company_storage.add(company_source.get_companies())

    company = company_storage.get("00236903")
    # print(company)

    # Create service
    company_service = CompanyService(company_storage)
    # Getting company profile
    profile = company_service.get_profile("00236903")
    # print(profile)

    # Getting revenue
    revenue_history = company_service.get_revenue_history("00236903")

    # print("\nRevenue history:")
    # for revenue in revenue_history:
    #     print(revenue)

    # Getting balance
    balance = company_service.get_balance_history("00236903")
    print("\nBalance history:")
    for balance_item in balance:
        print(balance_item)

    # Start WEB app
    company_controller = CompanyController(company_service)
    app.register_blueprint(company_controller.blueprint())

    app.run(debug=True)

    # Close db connection
    db_connection.close()


