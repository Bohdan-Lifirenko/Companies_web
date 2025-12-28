import os
import sqlite3
from pathlib import Path

import pandas as pd


class CompanyStorageInitializer:
    @staticmethod
    def init(db_connection):

        cursor = db_connection.cursor()
        # Create companies_description table
        db_connection.execute("""
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
        db_connection.execute("""
            CREATE TABLE IF NOT EXISTS financial_metrics (
                tax_id VARCHAR(8),
                my_date DATE,
                code INTEGER,
                value REAL,
                c_doc_sub VARCHAR(10),
                FOREIGN KEY (tax_id) REFERENCES companies_description(tax_id)
            )
            """)
