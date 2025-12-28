from abc import abstractmethod, ABC
from typing import List

from src.domain.models import Company


class CompanySource(ABC):
    @abstractmethod
    def get_companies(self) -> List[Company]:
        pass
