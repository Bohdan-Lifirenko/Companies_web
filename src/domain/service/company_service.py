from datetime import datetime
from typing import List

from src.domain.models import Revenue, CompanyProfile
from src.domain.storage import CompanyStorage


class CompanyService:
    def __init__(self, company_storage: CompanyStorage):
        self.storage: CompanyStorage = company_storage

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



