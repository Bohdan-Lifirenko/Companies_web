from abc import abstractmethod, ABC
from typing import Optional

from src.domain.models import Company


class CompanyStorage(ABC):
    @abstractmethod
    def get(self, company_id: str) -> Optional[Company]:
        pass

    @abstractmethod
    def add(self, companies: list[Company]):
        pass

    @abstractmethod
    def exists(self, company_id: str) -> bool:
        pass
