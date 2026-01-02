import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from src.domain.models import Company, FinancialMetric
from src.domain.source import CSVCompanySource

def test_getting_company_from_source(tmp_path):
    discr_path = tmp_path / "company_description.csv"
    metrics_path = tmp_path / "fin_metrics.csv"

    discr_path.write_text(
        'tax_id,name,kved,opf_code,katottg,region_code,local_code,num_workers\n'
        '00236903,"АКЦІОНЕРНЕ ТОВАРИСТВО ""ГОЛОВНИЙ ІНСТИТУТ ПО ПРОЕКТУВАННЮ ЗАВОДІВ ТРАКТОРНОГО, АВТОМОБІЛЬНОГО ТА СІЛЬСЬКОГОСПОДАРСЬКОГО МАШИНОБУДУВАННЯ\"\"\",71.12,,UA63120270010948820,63,012,0',
        encoding="utf-8"
    )
    metrics_path.write_text(
        'tax_id,my_date,code,value,c_doc_sub\n'
        '00236903,2020-12-31,1011,523.0,001',
        encoding="utf-8"
    )

    source = CSVCompanySource(discr_path, metrics_path)
    actual_result = source.get_companies()

    expected_result = [Company(
        tax_id='00236903',
        name='АКЦІОНЕРНЕ ТОВАРИСТВО "ГОЛОВНИЙ ІНСТИТУТ ПО ПРОЕКТУВАННЮ ЗАВОДІВ ТРАКТОРНОГО, АВТОМОБІЛЬНОГО ТА СІЛЬСЬКОГОСПОДАРСЬКОГО МАШИНОБУДУВАННЯ"',
        kved='71.12',
        opf_code='',
        katottg='UA63120270010948820',
        region_code='63',
        local_code='012',
        num_workers=0,
        financial_metrics=[
            FinancialMetric(
                tax_id='00236903',
                date=datetime(2020, 12, 31, 0, 0),
                code=1011,
                value=523.0,
                c_doc_sub='001'
            )
        ]
    )]


    assert actual_result == expected_result

def test_getting_two_company_from_source(tmp_path):
    discr_path = tmp_path / "company_description.csv"
    metrics_path = tmp_path / "fin_metrics.csv"

    discr_path.write_text(
        'tax_id,name,kved,opf_code,katottg,region_code,local_code,num_workers\n'
        '00236903,"АКЦІОНЕРНЕ ТОВАРИСТВО ""ГОЛОВНИЙ ІНСТИТУТ ПО ПРОЕКТУВАННЮ ЗАВОДІВ ТРАКТОРНОГО, АВТОМОБІЛЬНОГО ТА СІЛЬСЬКОГОСПОДАРСЬКОГО МАШИНОБУДУВАННЯ\"\"\",71.12,,UA63120270010948820,63,012,0\n'
        '00292379,"ПРИВАТНЕ АКЦІОНЕРНЕ ТОВАРИСТВО ""ЖЕЖЕЛІВСЬКИЙ КАР\'ЄР""",08.11,,UA05120010090086645,05,012,0',
        encoding="utf-8"
    )
    metrics_path.write_text(
        'tax_id,my_date,code,value,c_doc_sub\n'
        '00236903,2020-12-31,1011,523.0,001\n'
        '00292379,2022-12-31,1012,1023.0,002',
        encoding = "utf-8"
    )

    source = CSVCompanySource(discr_path, metrics_path)
    actual_result = source.get_companies()

    expected_result = [Company(
        tax_id='00236903',
        name='АКЦІОНЕРНЕ ТОВАРИСТВО "ГОЛОВНИЙ ІНСТИТУТ ПО ПРОЕКТУВАННЮ ЗАВОДІВ ТРАКТОРНОГО, АВТОМОБІЛЬНОГО ТА СІЛЬСЬКОГОСПОДАРСЬКОГО МАШИНОБУДУВАННЯ"',
        kved='71.12',
        opf_code='',
        katottg='UA63120270010948820',
        region_code='63',
        local_code='012',
        num_workers=0,
        financial_metrics=[
            FinancialMetric(
                tax_id='00236903',
                date=datetime(2020, 12, 31, 0, 0),
                code=1011,
                value=523.0,
                c_doc_sub='001'
            )
        ]
                       ),
        Company(tax_id='00292379',
                name='ПРИВАТНЕ АКЦІОНЕРНЕ ТОВАРИСТВО "ЖЕЖЕЛІВСЬКИЙ КАР\'ЄР"',
                kved='08.11',
                opf_code='',
                katottg='UA05120010090086645',
                region_code='05', local_code='012',
                num_workers=0,
                financial_metrics=[
                    FinancialMetric(tax_id='00292379',
                                    date=datetime(2022, 12, 31, 0, 0),
                                    code=1012,
                                    value=1023.0,
                                    c_doc_sub='002')
                ]
                )
    ]



    assert actual_result == expected_result

def test_getting_companies_from_empty_source(tmp_path):
    discr_path = tmp_path / "company_description.csv"
    metrics_path = tmp_path / "fin_metrics.csv"

    discr_path.write_text(
        '',
        encoding="utf-8"
    )
    metrics_path.write_text(
        '',
        encoding="utf-8"
    )

    source = CSVCompanySource(discr_path, metrics_path)
    actual_result = source.get_companies()
    expected_result = []

    assert actual_result == expected_result
