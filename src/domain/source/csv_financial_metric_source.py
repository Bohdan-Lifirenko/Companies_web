import csv
from abc import ABC
from datetime import datetime
from typing import List

from src.domain.models import FinancialMetric
from src.domain.source.financial_metric_source import FinancialMetricSource


class CsvFinancialMetricSource(FinancialMetricSource):
    def __init__(self, fin_metrics_file_path: str):
        self.fin_metrics_file_path = fin_metrics_file_path


    def get_fin_metrics(self) -> list[FinancialMetric]:
        """
           Читає CSV-файл і повертає список об'єктів FinancialMetric.
           CSV повинен містити колонки:
           tax_id,my_date,code,value,c_doc_sub
           """
        metrics: List[FinancialMetric] = []

        with open(self.fin_metrics_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                metric = FinancialMetric(
                    tax_id=row['tax_id'],
                    date=datetime.strptime(row['my_date'], "%Y-%m-%d"),
                    code=int(row['code']),
                    value=float(row['value']),
                    c_doc_sub=row['c_doc_sub']
                )
                metrics.append(metric)

        return metrics
