from abc import abstractmethod, ABC

from src.domain.models import FinancialMetric


class FinancialMetricSource(ABC):
    @abstractmethod
    def get_fin_metrics(self) -> list[FinancialMetric]:
        pass
