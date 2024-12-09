from dataclasses import dataclass


@dataclass
class DoctorData:
    doctorId: str
    doctorName: str
    degree: str
    university: str
    yearOfPassing: str
    yearOfInfo: str
    smcName: str
    parentName: str
    emailId: str
    gender: str
    birthDateStr: str
    address: str
    adharNo: str
