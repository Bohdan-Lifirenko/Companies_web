import os
from pathlib import Path
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

from src.domain.controler.company_controller import CompanyController
from src.domain.service import CompanyService
from src.domain.source.csv_company_source import CSVCompanySource
from src.domain.storage import CompanyStorageInitializer, SQLiteConnectionManager
from src.domain.storage.sqllite_company_storage import SqliteCompanyStorage

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Додаємо секретний ключ для роботи flash повідомлень


@app.route('/')
def index():
    # Головна сторінка з формою пошуку
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # Обробка форми пошуку
    company_id = request.form.get('company_id', '')

    if not company_id:
        flash('Будь ласка, введіть ЄДРПОУ компанії', 'danger')
        return redirect(url_for('index'))

    # Перевірка, чи існує компанія в базі даних
    try:
        company = company_storage.get(company_id)
        if not company:
            flash(f'Компанію з ЄДРПОУ {company_id} не знайдено', 'warning')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Помилка при пошуку: {str(e)}', 'danger')
        return redirect(url_for('index'))

    # Перенаправлення на сторінку компанії
    return redirect(url_for('company', company_id=company_id))


@app.route('/search/<company_id>')
def company(company_id):
    # Перевірка, чи існує компанія
    try:
        company = company_storage.get(company_id)
        if not company:
            flash(f'Компанію з ЄДРПОУ {company_id} не знайдено', 'warning')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Помилка при пошуку: {str(e)}', 'danger')
        return redirect(url_for('index'))

    return render_template('company.html', company_id=company_id)


# Глобальні змінні для доступу в маршрутах
company_storage = None
company_service = None
storage_connection_manager = None


def init_app():
    global company_storage, company_service, storage_connection_manager

    # Визначення шляхів
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

    print(f"Loading data from {DATA_DIR}")

    # Ініціалізація менеджера бази даних
    db_path = DATA_DIR / "company.db"
    storage_connection_manager = SQLiteConnectionManager(db_path)

    # Ініціалізація БД
    CompanyStorageInitializer.init(storage_connection_manager)

    # Отримання даних з джерела
    firms_path = DATA_DIR / "firms.csv"
    fin_values_path = DATA_DIR / "fin_values.csv"
    company_source = CSVCompanySource(firms_path, fin_values_path)

    # Створення сховища
    company_storage = SqliteCompanyStorage(storage_connection_manager)
    company_storage.add(company_source.get_companies())

    # Створення сервісу
    company_service = CompanyService(company_storage)

    # Реєстрація контролера
    company_controller = CompanyController(company_service)
    app.register_blueprint(company_controller.blueprint())


if __name__ == '__main__':
    # Ініціалізація додатку
    init_app()

    # Запуск веб-додатку
    app.run(debug=True)


# При завершенні роботи програми
def cleanup():
    if storage_connection_manager:
        storage_connection_manager.close_connection()


# Реєстрація функції для виклику при завершенні роботи Flask
@app.teardown_appcontext
def teardown_db(exception):
    if storage_connection_manager:
        storage_connection_manager.close_connection()
