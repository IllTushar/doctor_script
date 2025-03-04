import pandas as pd
import requests as rq
import os
import json
import time
from model.doctor_details_response import Model
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# API URL
URL = "https://www.nmc.org.in/MCIRest/open/getDataFromService?service=getDoctorDetailsByIdImr"

# Headers for the request
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def fetch_doctor_data(row):
    """Function to fetch doctor data for a single row."""
    registration_value = str(row["registration_number"]).strip()
    doctor_id = str(int(float(row["doctor_id"])))  # Convert to integer if it has a decimal

    # Ensure the registration number has at least 6 characters
    registration_value = registration_value.zfill(6)

    payload = {
        "doctorId": doctor_id,
        "regdNoValue": registration_value
    }

    try:
        response = rq.post(URL, json=payload, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if not json_data:
                    print(f"⚠ Warning: Empty JSON response for Doctor ID {doctor_id}")
                    return None

                # Convert JSON response to Model instance
                return Model(**json_data)

            except json.JSONDecodeError:
                print(f"❌ JSON decoding failed for Doctor ID {doctor_id}. Response: {response.text}")
                return None

        else:
            print(f"❌ Failed for Doctor ID {doctor_id}, HTTP Status: {response.status_code}")
            return None

    except rq.exceptions.RequestException as e:
        print(f"❌ Request error for Doctor ID {doctor_id}: {e}")
        return None


def process_yearly_data(year):
    """Process doctor data for a given year using multithreading."""
    file_path = fr'C:\Users\gtush\Desktop\DoctorsData\Data\doctor_data_{year}.csv'
    output_path = fr'C:\Users\gtush\Desktop\DoctorsData\Processed\doctor_data_{year}.csv'

    if not os.path.exists(file_path):
        print(f"⚠ File not found: {file_path}")
        return

    # Read CSV file
    read_file = pd.read_csv(file_path)

    # Using ThreadPoolExecutor with 12 threads
    doctor_data_list = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_row = {executor.submit(fetch_doctor_data, row): row for _, row in read_file.iterrows()}

        for future in as_completed(future_to_row):
            result = future.result()
            if result:
                doctor_data_list.append(result)

    if doctor_data_list:
        df = pd.DataFrame([asdict(d) for d in doctor_data_list])
        df.to_csv(output_path, index=False)
        print(f"✅ Data saved for year {year} at {output_path}")
    else:
        print(f"⚠ No data fetched for year {year}")


if __name__ == '__main__':
    # Process data for each year using multithreading
    with ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(process_yearly_data, range(1970, 2018))

    print("🎉 Data fetching complete!")
