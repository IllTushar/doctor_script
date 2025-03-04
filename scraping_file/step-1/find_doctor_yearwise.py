import requests as rq
import pandas as pd
from typing import List
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from request.year_pages_request import RequestData
from model.doctor_data_response import DoctorYearlyData

# Output directory
file_path = r'C:\Users\gtush\Desktop\DoctorsData\Data\records_total.csv'
output_dir = r'C:\Users\gtush\Desktop\DoctorsData\Data'
os.makedirs(output_dir, exist_ok=True)

# Read CSV file
read_file = pd.read_csv(file_path)
years_data: List[RequestData] = [RequestData(row['Year'], row['RecordsTotal']) for _, row in read_file.iterrows()]


# Function to extract `doctorId` from HTML
def extract_doctor_id(html_str):
    match = re.search(r"openDoctorDetailsnew\('(\d+)',", html_str)
    return match.group(1) if match else None


# Function to fetch and save data for a given year
def fetch_and_save_data(item: RequestData):
    all_data: List[DoctorYearlyData] = []
    url = f'https://www.nmc.org.in/MCIRest/open/getPaginatedData?service=getPaginatedDoctor&draw=1&start=0&length={item.pages}&year={item.year}'

    response = rq.get(url)
    if response.status_code == 200:
        json_data = response.json()
        doctor_list = json_data.get("data", [])

        for doctor in doctor_list:
            doctor_id = extract_doctor_id(doctor[6])  # Extract doctorId from HTML

            doctor_data = DoctorYearlyData(
                id=doctor[0],
                year=doctor[1],
                registration_number=doctor[2],
                council_name=doctor[3],
                doctor_name=doctor[4],
                doctor_id=doctor_id  # Add extracted doctorId
            )
            all_data.append(doctor_data)

        # Save data for this year to CSV
        output_csv_path = os.path.join(output_dir, f'doctor_data_{item.year}.csv')
        df = pd.DataFrame([d.__dict__ for d in all_data])
        df.to_csv(output_csv_path, index=False, encoding='utf-8')

        print(f"✅ Data for year {item.year} saved to {output_csv_path}")
    else:
        print(f"❌ Failed to fetch data for year {item.year}, Status Code: {response.status_code}")


# Use ThreadPoolExecutor with 10 threads
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_year = {executor.submit(fetch_and_save_data, item): item.year for item in years_data}

        for future in as_completed(future_to_year):
            try:
                future.result()  # Raise exceptions if any occur
            except Exception as e:
                print(f"⚠ Error processing year {future_to_year[future]}: {e}")
