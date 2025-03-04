import pandas as pd

if __name__ == '__main__':
    file_path = r'C:\Users\gtush\Desktop\MusicProject\Semi_Final_Doctors_A 2 (1).csv'

    try:
        # Read the CSV file with proper encoding
        read_file = pd.read_csv(file_path, encoding='ISO-8859-1')  # You can also try 'ISO-8859-1' if utf-8 fails
        # Iterate over each row in the DataFrame
        for index, row in read_file.iterrows():
            if pd.notna(row["RDegree1"]) and ',' in row["RDegree1"]:  # Check if value contains a comma
                degrees = row["RDegree1"].split(',')  # Split by comma
                if len(degrees) > 1:
                    print("Degree", degrees) # Ensure there are multiple degrees
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except UnicodeDecodeError:
        print("Error: Encoding issue. Try changing 'utf-8' to 'ISO-8859-1' or 'latin1'.")
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
