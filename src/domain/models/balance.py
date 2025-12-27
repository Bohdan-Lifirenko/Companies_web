from dataclasses import dataclass


@dataclass
class Balance:
    assets: float
    equity: float
    liabilities: float
