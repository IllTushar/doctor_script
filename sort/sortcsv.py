import pandas as pd
if __name__ == '__main__':
    # Path to your CSV file
    csv_file = r"C:\Users\gtush\Desktop\DoctorsData\Data\records_total.csv"

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert "Year" column to integers for proper sorting
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # Sort by "Year"
    df = df.sort_values(by="Year")

    # Save the sorted CSV file
    df.to_csv(csv_file, index=False)

    print("CSV file sorted successfully!")


