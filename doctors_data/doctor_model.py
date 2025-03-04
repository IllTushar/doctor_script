# Define the model class
from dataclasses import dataclass


@dataclass
class Doctor:
    id: int
    year: int
    reg_date: str
    doctor_id: int
    salutation: str
    first_name: str
    middle_name: str
    last_name: str
    phone_no: str
    email_id: str
    gender: str
    blood_group: str
    parent_name: str
    birth_date: str
    birth_date_str: str
    doctor_degree: str
    university: str
    year_of_passing: str
    registration_number: str
    smc_name: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    additional_qualification_1: str
    additional_qualification_year_1: str
    additional_qualification_university_1: str
    additional_qualification_2: str
    additional_qualification_year_2: str
    additional_qualification_university_2: str
    additional_qualification_3: str
    additional_qualification_year_3: str
    additional_qualification_university_3: str
