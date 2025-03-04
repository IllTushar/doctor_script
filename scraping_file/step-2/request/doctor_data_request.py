from dataclasses import dataclass


@dataclass
class RequestClass:
    registration_id: int
    year: int
    medical_council: str
