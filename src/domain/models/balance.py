from dataclasses import dataclass
from datetime import datetime


@dataclass
class Balance:
    date: datetime
    assets: float
    equity: float
    liabilities: float
