import pandas as pd
import time

# List of CSV files
csv_files = ['insurance_data_2020.csv', 'insurance_data_2021.csv', 'insurance_data_2022.csv', 'insurance_data_2023.csv', 'insurance_data_2024.csv']

# Variable to hold the total row count
total_row_count = 0

start_time=time.time()
# Define the chunk size (e.g., 1 million rows at a time)
chunk_size = 1000000  # You can adjust this size based on your system's memory capacity

# Loop through each CSV file and read in chunks
for file in csv_files:
    # Read each chunk from the CSV file
    for chunk in pd.read_csv(file, chunksize=chunk_size):
        # Add the number of rows in the current chunk to the total count
        print("cc:", chunk)
        total_row_count += len(chunk)

print("total time:", time.time()-start_time)

# Print the total row count
print(f"Total number of rows: {total_row_count}")
