import pandas as pd
from genderize import Genderize
from unidecode import unidecode


import time

# Function to get gender for a batch of names with retries
def get_gender_for_batch_with_retry(names, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            result = genderize.get(names)
            genders = [res['gender'] if 'gender' in res else 'Unknown' for res in result]
            return genders
        except Exception as e:
            print(f"Error processing batch. Retrying... Retry count: {retries + 1}")
            retries += 1
            time.sleep(60)  # Wait for a minute before retrying
    print("Max retries reached. Unable to process the batch.")
    return ['Unknown'] * len(names)


# Load the Excel file
file_path = r'E:\IESE Business School\Task 7_Portugese Database\Name_Gender_Database.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Extract names from Column "E" and remove accents
names = df['Name'].tolist()
names_without_accents = [unidecode(name) for name in names]

# Split names into batches (adjust batch size as needed)
batch_size = 10
name_batches = [names_without_accents[i:i + batch_size] for i in range(0, len(names_without_accents), batch_size)]
# Classify genders for each batch of names with retries
all_genders = []
for batch in name_batches:
    genders_batch = get_gender_for_batch_with_retry(batch)
    all_genders.extend(genders_batch)
# Initialize Genderize
genderize = Genderize()

# Function to get gender for a batch of names
def get_gender_for_batch(names):
    try:
        result = genderize.get(names)
        genders = [res['gender'] if 'gender' in res else 'Unknown' for res in result]
        return genders
    except Exception as e:
        print(f"Error processing batch: {e}")
        return ['Unknown'] * len(names)

# Classify genders for each batch of names
all_genders = []
for batch in name_batches:
    genders_batch = get_gender_for_batch(batch)
    all_genders.extend(genders_batch)

# Create a new column "Gender" with the predicted genders
df['Gender'] = all_genders

# Save the modified Excel file
output_file_path = 'E:\IESE Business School\Task 7_Portugese Database\Try and Fail\Trial_Database.xlsx'  # Replace with your desired output file path
df.to_excel(output_file_path, index=False)



# Classify genders for each batch of names with retries
all_genders = []
for batch in name_batches:
    genders_batch = get_gender_for_batch_with_retry(batch)
    all_genders.extend(genders_batch)

# Continue with the rest of the code...
