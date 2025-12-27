from dataclasses import dataclass

@dataclass
class Company:
    tax_id: str
    name: str
    kved: str
    opf_code: str
    katottg: str
    region_code: str
    local_code: str

