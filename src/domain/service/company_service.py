from typing import List

from src.domain.models import Revenue
from src.domain.storage import CompanyStorage


class CompanyService:
    def __init__(self, company_storage: CompanyStorage):
        self.storage: CompanyStorage = company_storage

    def get_revenue_history(self, company_id) -> list[Revenue]:
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

