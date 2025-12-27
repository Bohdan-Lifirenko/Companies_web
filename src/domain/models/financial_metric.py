from dataclasses import dataclass
from datetime import datetime

@dataclass
class FinancialMetric:
    tax_id: str
    date: datetime
    code: int
    value: float
    c_doc_sub: str
