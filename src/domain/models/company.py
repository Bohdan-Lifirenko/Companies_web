from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class FinancialMetric:
    tax_id: str
    date: datetime
    code: int
    value: float
    c_doc_sub: str


@dataclass
class Company:
    tax_id: str
    name: str
    kved: str
    opf_code: str
    katottg: str
    region_code: str
    local_code: str
    num_workers: int
    financial_metrics: List[FinancialMetric]

    def __str__(self) -> str:
        """
        Returns a pretty-printed string representation of the Company instance.
        """
        metrics_str = "\n".join(
            f"  - Date: {metric.date.strftime('%Y-%m-%d')}, Code: {metric.code}, "
            f"Value: {metric.value:.2f}, C Doc Sub: {metric.c_doc_sub}"
            for metric in self.financial_metrics
        )

        return (
            f"Company:\n"
            f"  Tax ID: {self.tax_id}\n"
            f"  Name: {self.name}\n"
            f"  KVED: {self.kved}\n"
            f"  OPF Code: {self.opf_code}\n"
            f"  KATOTTG: {self.katottg}\n"
            f"  Region Code: {self.region_code}\n"
            f"  Local Code: {self.local_code}\n"
            f"  Number of Workers: {self.num_workers}\n"
            f"Financial Metrics:\n{metrics_str if metrics_str else '  No financial metrics available.'}"
        )

