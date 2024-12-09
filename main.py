import requests as rq
import pandas as pd
from doctors_data.doctor_model import Doctor
from typing import List
import re
from dataclasses import asdict
from doctors_data.doctor_data import YearlyDoctorData


def getDoctorData(url, year):
    response = rq.get(url)
    if response.status_code == 200:
        api_data = response.json()
        records_filtered = api_data.get("recordsFiltered", 0)
        print(records_filtered)
        data = api_data.get("data", [])

        # Parse the API response data
        doctors = parse_data(data)

        # Generate a filename based on the year
        filename = fr"C:\Users\gtush\Desktop\DoctorsData\Data\doctors_{year}.csv"

        # Save the data to CSV
        save_to_csv_with_pandas(doctors, filename)
        print(f"Year {year}: Processed {len(doctors)} records and saved to {filename}")
    else:
        print(f"Failed to fetch data for year {year}. HTTP Status Code: {response.status_code}")


# Function to parse and extract details from the provided JSON
def parse_data(data: List[List]) -> List[Doctor]:
    doctors = []
    for record in data:
        # Extract doctorId and regdNoValue from the 'onclick' attribute
        onclick_match = re.search(r"openDoctorDetailsnew\('(\d+)', '([\w\s]+)'\)", record[6])
        if onclick_match:
            doctor_id = onclick_match.group(1)  # Extract doctorId
        else:
            doctor_id = None

        # Create a Doctor instance
        doctor = Doctor(
            id=record[0],
            year=record[1],
            medical_council=record[3],
            doctor_name=record[4],
            relation=record[5],
            doctor_id=doctor_id,
            registration_number=str(record[2]),  # Convert registration_number to string
        )
        doctors.append(doctor)
    return doctors


# Save to CSV using pandas
def save_to_csv_with_pandas(doctors: List[Doctor], filename: str):
    # Convert list of dataclass objects to a list of dictionaries
    data_dicts = [asdict(doctor) for doctor in doctors]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_dicts)

    # Save DataFrame to CSV
    df.to_csv(filename, index=False, encoding='utf-8')


if __name__ == '__main__':
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    lengths = [58341, 61607, 44978, 31854, 20077, 7751]
    # Create a list of YearlyDoctorData objects
    yearly_data = [YearlyDoctorData(year=year, doctor_count=length) for year, length in zip(years, lengths)]

    for item in yearly_data:
        url = f'https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={item.doctor_count}&search%5Bvalue%5D=&search%5Bregex%5D=false&name=&registrationNo=&smcId=&year={item.year}&_=1733728970660'
        getDoctorData(url, item.year)

