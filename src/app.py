import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

from src.domain.controler.company_controller import CompanyController
from src.domain.service import CompanyService
from src.domain.source.csv_company_source import CSVCompanySource
from src.domain.storage import CompanyStorageInitializer, SQLiteConnectionManager
from src.domain.storage.sqllite_company_storage import SqliteCompanyStorage

app = Flask(__name__)
app.secret_key = 'your-secret-key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    company_id = request.form.get('company_id', '')

    if not company_id:
        flash('Будь ласка, введіть ЄДРПОУ компанії', 'danger')
        return redirect(url_for('index'))

    try:
        if not company_service.company_exists(company_id):
            flash(f'Компанію з ЄДРПОУ {company_id} не знайдено', 'warning')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Помилка при пошуку: {str(e)}', 'danger')
        return redirect(url_for('index'))

    return redirect(url_for('company', company_id=company_id))


@app.route('/search/<company_id>')
def company(company_id):
    try:
        if not company_service.company_exists(company_id):
            flash(f'Компанію з ЄДРПОУ {company_id} не знайдено', 'warning')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Помилка при пошуку: {str(e)}', 'danger')
        return redirect(url_for('index'))

    return render_template('company.html', company_id=company_id)

company_storage = None
company_service = None
storage_connection_manager = None


def init_app():
    global company_storage, company_service, storage_connection_manager

    # Identifying paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

    print(f"Loading data from {DATA_DIR}")

    # Initializing the database manager
    db_path = DATA_DIR / "company.db"

    print(f"Database path: {db_path}")
    storage_connection_manager = SQLiteConnectionManager(db_path)

    # Database initialization
    CompanyStorageInitializer.init(storage_connection_manager)

    # Obtaining data from the source
    firms_path = DATA_DIR / "firms.csv"
    fin_values_path = DATA_DIR / "fin_values.csv"
    company_source = CSVCompanySource(firms_path, fin_values_path)

    # Creating a repository
    company_storage = SqliteCompanyStorage(storage_connection_manager)
    company_storage.add(company_source.get_companies())

    # Creation of the service
    company_service = CompanyService(company_storage)

    # Controller registration
    company_controller = CompanyController(company_service)
    app.register_blueprint(company_controller.blueprint())


# Application initialization
init_app()

if __name__ == '__main__':

    # Launching a web application
    app.run(debug=True)


# When the program finishes running
def cleanup():
    if storage_connection_manager:
        storage_connection_manager.close_connection()


# Registering a function to call when Flask finishes running
@app.teardown_appcontext
def teardown_db(exception):
    if storage_connection_manager:
        storage_connection_manager.close_connection()
