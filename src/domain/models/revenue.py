from dataclasses import dataclass
from datetime import datetime


@dataclass
class Revenue:
    date: datetime
    value: float
