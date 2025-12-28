from collections import defaultdict
from datetime import datetime
from typing import List

from src.domain.models import Revenue, CompanyProfile, Balance
from src.domain.storage import CompanyStorage


class CompanyService:
    def __init__(self, company_storage: CompanyStorage):
        self.storage: CompanyStorage = company_storage

    def get_profile(self, company_id: str) -> CompanyProfile:
        company = self.storage.get(company_id)

        return CompanyProfile(
            tax_id=company.tax_id,
            name=company.name,
            kved=company.kved,
            opf_code=company.opf_code,
            katottg=company.katottg,
            region_code=company.region_code
        )

    def get_revenue_history(self, company_id: str) -> list[Revenue]:
        company = self.storage.get(company_id)

        revenues: List[Revenue] = []

        for metric in company.financial_metrics:
            if metric.code == 2000:
                revenues.append(
                    Revenue(
                        date=metric.date,
                        value=metric.value
                    )
                )

        # Sort revenues by date in ascending order
        revenues.sort(key=lambda r: r.date)

        return revenues

    def get_balance_history(self, company_id: str) -> list[Balance]:
        company = self.storage.get(company_id)
        # Group metrics by date
        date_metrics = defaultdict(lambda: {'assets': 0.0, 'equity': 0.0})

        for metric in company.financial_metrics:
            if metric.code == 1300:
                date_metrics[metric.date]['assets'] += metric.value
            elif metric.code == 1495:
                date_metrics[metric.date]['equity'] += metric.value

        # Create Balance instances only for dates with both assets and equity
        balances = []
        for date, values in date_metrics.items():
            if values['assets'] != 0.0 and values['equity'] != 0.0:  # Skip if missing one
                liabilities = values['assets'] - values['equity']
                balances.append(Balance(
                    date=date,
                    assets=values['assets'],
                    equity=values['equity'],
                    liabilities=liabilities
                ))

        # Sort by date ascending
        balances.sort(key=lambda b: b.date)

        return balances

