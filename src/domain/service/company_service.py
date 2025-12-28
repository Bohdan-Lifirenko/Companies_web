from collections import defaultdict
from datetime import datetime
from typing import List

from src.domain.models import Revenue, CompanyProfile, Balance
from src.domain.storage import CompanyStorage

class FinancialMetricCode:
    REVENUE = 2000
    ASSETS = 1300
    EQUITY = 1495

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

        revenues = self._extract_revenues(company.financial_metrics)

        return self._sort_by_date(revenues)

    def get_balance_history(self, company_id: str) -> list[Balance]:
        company = self.storage.get(company_id)
        date_metrics = defaultdict(lambda: {'assets': None, 'equity': None})

        for metric in company.financial_metrics:
            if metric.code == FinancialMetricCode.ASSETS:
                date_metrics[metric.date]['assets'] = metric.value
            elif metric.code == FinancialMetricCode.EQUITY:
                date_metrics[metric.date]['equity'] = metric.value

        # Create a balance only if both values are present
        balances = []
        for date, values in date_metrics.items():
            if values['assets'] is not None and values['equity'] is not None:
                liabilities = values['assets'] - values['equity']
                balances.append(Balance(
                    date=date,
                    assets=values['assets'],
                    equity=values['equity'],
                    liabilities=liabilities
                ))

        return self._sort_by_date(balances)

    def _extract_revenues(self, financial_metrics) -> list[Revenue]:
        revenues = []
        for metric in financial_metrics:
            if metric.code == FinancialMetricCode.REVENUE:
                revenues.append(Revenue(date=metric.date, value=metric.value))
        return revenues

    def _sort_by_date(self, items) -> list:
        return sorted(items, key=lambda item: item.date)

