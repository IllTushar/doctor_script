import requests as rq
import pandas as pd
from doctors_data.doctor_model import Doctor
from typing import List
from dataclasses import asdict
from doctors_data.doctor_data import YearlyDoctorData


# Function to fetch doctor data
def getDoctorData(url, year):
    try:
        response = rq.get(url)
        if response.status_code == 200:
            api_data = response.json()

            records_filtered = api_data.get("recordsFiltered", 0)
            print(f"Year {year}: {records_filtered} records found.")

            # Ensure data is a list
            data = api_data.get("data", [])
            if not isinstance(data, list):
                print(f"Unexpected data format for year {year}. Skipping.")
                return

            doctors = parse_data(data)

            # Generate a filename based on the year
            filename = fr"C:\Users\gtush\Desktop\DoctorsData\Data\doctors_{year}.csv"

            # Save the data to CSV
            save_to_csv_with_pandas(doctors, filename)
            print(f"Year {year}: Processed {len(doctors)} records and saved to {filename}")

        else:
            print(f"Failed to fetch data for year {year}. HTTP Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error fetching data for year {year}: {str(e)}")


# Function to parse and extract details from the JSON response
def parse_data(data: List[List]) -> List[Doctor]:
    doctors = []
    for record in data:
        # Extract doctorId and registration number correctly from the list
        doctor = Doctor(
            id=record[0],  # doctorId
            year=record[1],  # Year
            reg_date=record[2],  # Registration Date
            doctor_id=record[0],  # Same as id
            salutation=None,  # No index for salutation
            first_name=record[4],  # Doctor Name
            middle_name=None,  # Not in dataset
            last_name=None,  # Not in dataset
            phone_no=None,  # Not in dataset
            email_id=None,  # Not in dataset
            gender=None,  # Not in dataset
            blood_group=None,  # Not in dataset
            parent_name=record[5],  # Parent Name
            birth_date=None,  # Not in dataset
            birth_date_str=None,  # Not in dataset
            doctor_degree=None,  # Not in dataset
            university=None,  # Not in dataset
            year_of_passing=None,  # Not in dataset
            registration_number=record[2],  # Registration Number
            smc_name=record[3],  # Medical Council Name
            address=None,  # Not in dataset
            city=None,  # Not in dataset
            state=None,  # Not in dataset
            country=None,  # Not in dataset
            pincode=None,  # Not in dataset
            additional_qualification_1=None,
            additional_qualification_year_1=None,
            additional_qualification_university_1=None,
            additional_qualification_2=None,
            additional_qualification_year_2=None,
            additional_qualification_university_2=None,
            additional_qualification_3=None,
            additional_qualification_year_3=None,
            additional_qualification_university_3=None
        )
        doctors.append(doctor)
    return doctors


# Save data to CSV using pandas
def save_to_csv_with_pandas(doctors: List[Doctor], filename: str):
    if not doctors:
        print(f"No valid doctor data to save for {filename}. Skipping.")
        return

    # Convert list of dataclass objects to dictionaries
    data_dicts = [asdict(doctor) for doctor in doctors]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_dicts)

    # Save DataFrame to CSV
    df.to_csv(filename, index=False, encoding='utf-8')


if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\DoctorsData\Data\records_total.csv'
    readFile = pd.read_csv(file_path)
    years = readFile['Year']
    lengths = readFile['RecordsTotal']

    # Create a list of YearlyDoctorData objects
    yearly_data = [YearlyDoctorData(year=year, doctor_count=length) for year, length in zip(years, lengths)]

    for item in yearly_data:
        url = f'https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw=1' \
              f'&start=0&length={item.doctor_count}&year={item.year}'
        getDoctorData(url, item.year)
