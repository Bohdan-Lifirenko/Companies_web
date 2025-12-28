import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from src.domain.models import Company, FinancialMetric
from src.domain.source.company_source import CompanySource


class CSVCompanySource(CompanySource):
    def __init__(self, company_description_file_path: Path, fin_metrics_file_path: Path):
        self.company_description_file_path = company_description_file_path
        self.fin_metrics_file_path = fin_metrics_file_path

    def get_companies(self) -> List[Company]:
        # Зчитуємо фінансові метрики та групуємо їх по tax_id
        metrics_by_tax_id: Dict[str, List[FinancialMetric]] = {}

        with open(self.fin_metrics_file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = FinancialMetric(
                    tax_id=row["tax_id"],
                    date=datetime.strptime(row["my_date"], "%Y-%m-%d"),
                    code=int(row["code"]),
                    value=float(row["value"]),
                    c_doc_sub=row["c_doc_sub"]
                )

                metrics_by_tax_id.setdefault(metric.tax_id, []).append(metric)

        # 2. Зчитуємо компанії та під'єднуємо до них фінансові метрики
        companies: List[Company] = []

        with open(self.company_description_file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tax_id = row["tax_id"]

                company = Company(
                    tax_id=tax_id,
                    name=row["name"],
                    kved=row["kved"],
                    opf_code=row["opf_code"],
                    katottg=row["katottg"],
                    region_code=row["region_code"],
                    local_code=row["local_code"],
                    num_workers=int(row["num_workers"]),
                    financial_metrics=metrics_by_tax_id.get(tax_id, [])
                )

                companies.append(company)

        return companies
