from abc import ABC, abstractmethod

from src.domain.models import Revenue


class FinancialMetricStorage(ABC):
    @abstractmethod
    def get_company_revenue_statistic(self, company_id: int) -> list[Revenue]:
        pass
