from datetime import datetime
from unittest.mock import Mock

from src.domain.models import FinancialMetric, Company, CompanyProfile
from src.domain.service import CompanyService
from src.domain.storage import CompanyStorage


def test_that_company_exists():
    storage = Mock(spec=CompanyStorage)
    storage.exists.return_value = True

    service = CompanyService(storage)
    assert service.company_exists("12345678") == True

def test_that_company_not_exists():
    storage = Mock(spec=CompanyStorage)
    storage.exists.return_value = False

    service = CompanyService(storage)
    assert service.company_exists("12345678") == False

def test_get_profile():
    storage = Mock(spec=CompanyStorage)
    storage.get.return_value = Company(
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
    )

    service = CompanyService(storage)

    actual_result = service.get_profile("00236903")

    expected_result = CompanyProfile(
        tax_id='00236903',
        name='АКЦІОНЕРНЕ ТОВАРИСТВО "ГОЛОВНИЙ ІНСТИТУТ ПО ПРОЕКТУВАННЮ ЗАВОДІВ ТРАКТОРНОГО, АВТОМОБІЛЬНОГО ТА СІЛЬСЬКОГОСПОДАРСЬКОГО МАШИНОБУДУВАННЯ"',
        kved='71.12',
        opf_code='',
        katottg='UA63120270010948820',
        region_code='63',
        local_code='012'
    )

    assert actual_result == expected_result
