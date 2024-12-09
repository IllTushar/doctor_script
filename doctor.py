import pandas as pd
import requests as rq
from concurrent.futures import ThreadPoolExecutor
from doctor_info.doctor_info_class import DoctorData
from dataclasses import asdict
import threading
import csv

# Thread-safe lock for writing to the CSV file
write_lock = threading.Lock()


def fetch_doctor_data(row, output_file, index, year):
    """Fetch doctor data for a single row and write it to the output file."""
    url = 'https://www.nmc.org.in/MCIRest/open/getDataFromService?service=getDoctorDetailsByIdImr'

    # Ensure correct types for data fields
    registration_value = str(row["registration_number"]).strip()
    doctor_id = str(int(float(row["doctor_id"])))  # Convert to integer if it has a decimal

    # Ensure the registration number has at least 6 characters
    if len(registration_value) < 6:
        registration_value = registration_value.zfill(6)  # Pad with leading zeros

    # Prepare the payload
    data = {
        "doctorId": doctor_id,
        "regdNoValue": registration_value
    }

    try:
        print(f"Year: {year}, Index: {index}, Sending payload: {data}")
        # Send the POST request with JSON payload
        response = rq.post(url, json=data, timeout=10)

        # Check and handle the response
        if response.status_code == 200:
            try:
                # Parse the JSON response
                response_json = response.json()

                # Map API response to the dataclass
                doctor = DoctorData(
                    doctorId=doctor_id,
                    doctorName=response_json.get("firstName", ""),
                    university=response_json.get("university", ""),
                    degree=response_json.get("doctorDegree", ""),
                    yearOfPassing=response_json.get("yearOfPassing", ""),
                    yearOfInfo=response_json.get("yearInfo", ""),
                    smcName=response_json.get("smcName", ""),
                    parentName=response_json.get("parentName", ""),
                    emailId=response_json.get("emailId", ""),
                    gender=response_json.get("gender", ""),
                    birthDateStr=response_json.get("birthDateStr", ""),
                    address=response_json.get("address", ""),
                    adharNo=response_json.get("adharNo", "")
                )

                # Write to the file
                with write_lock:
                    with open(output_file, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=asdict(doctor).keys())
                        writer.writerow(asdict(doctor))

            except ValueError:
                print(f"Error: Invalid JSON response for doctorId {doctor_id}")
        else:
            print(f"Error: Received status code {response.status_code} for doctorId {doctor_id}")

    except rq.exceptions.RequestException as e:
        print(f"Error: Request failed for doctorId {doctor_id} with exception {e}")


def doctor_details_multithreaded(read_file, output_file, year):
    """Process doctor details using multithreading and write each response immediately."""
    # Initialize the output file with headers
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=DoctorData.__annotations__.keys())
        writer.writeheader()

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit tasks to the executor
        for index, row in read_file.iterrows():
            executor.submit(fetch_doctor_data, row, output_file, index, year)


if __name__ == '__main__':
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    for year in years:
        file_path = fr'C:\Users\gtush\Desktop\DoctorsData\Data\doctors_{year}.csv'
        output_file = fr'C:\Users\gtush\Desktop\DoctorsData\Doctor\doctor_{year}.csv'
        try:
            # Read the CSV file
            read_file = pd.read_csv(file_path)

            # Validate the DataFrame
            if read_file.empty:
                print(f"Error: File for year {year} is empty or invalid")
                continue

            # Process the DataFrame with multithreading
            doctor_details_multithreaded(read_file, output_file, year)

        except FileNotFoundError:
            print(f"Error: File not found for year {year}")
        except pd.errors.EmptyDataError:
            print(f"Error: File for year {year} is empty or invalid")
