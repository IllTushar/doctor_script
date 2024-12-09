# Define the model class
from dataclasses import dataclass


@dataclass
class Doctor:
    id: int
    year: int
    medical_council: str
    doctor_name: str
    relation: str
    doctor_id: str
    registration_number: str
