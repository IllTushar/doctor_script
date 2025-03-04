from dataclasses import dataclass
from typing import List


@dataclass
class DoctorYearlyData:
    id: int
    year: int
    registration_number: str
    council_name: str
    doctor_name: str
    doctor_id: str


@dataclass
class ResponseModel:
    records_filtered: int
    data: List[DoctorYearlyData]
