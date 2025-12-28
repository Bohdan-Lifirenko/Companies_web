from abc import abstractmethod, ABC
from typing import Optional

from src.domain.models import Company, Revenue


class CompanyStorage(ABC):
    @abstractmethod
    def get(self, company_id: str) -> Optional[Company]:
        pass

    @abstractmethod
    def add(self, companies: list[Company]):
        pass
