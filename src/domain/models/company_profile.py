from dataclasses import dataclass

@dataclass
class CompanyProfile:
    tax_id: str      # ЄДРПОУ
    name: str        # Назва
    kved: str        # КВЕД
    opf_code: str    # ОПФ
    katottg: str     # КАТОТТГ
    region_code: str # Код регіону
    local_code: str  # Код населеного пункту
