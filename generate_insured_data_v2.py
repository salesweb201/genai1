import pandas as pd
import numpy as np


# Function to generate a DataFrame with 10,000 rows for a specific year
def generate_data(year, num_rows=10000):
    # Columns
    sl = np.arange(1, num_rows + 1)  # Sequential 'sl' values
    insured_type = np.random.choice(['Health', 'Life', 'Auto', 'Property'], num_rows)
    insured_group = np.random.choice(['Group A', 'Group B', 'Group C', 'Group D'], num_rows)
    loss_ratio = np.random.uniform(0, 1, num_rows)  # Loss ratio between 0 and 1
    filter_loss_ratio = np.random.uniform(0, 1, num_rows)  # Same range for filtered loss ratio
    profit = np.random.uniform(-1000000, 1000000, num_rows)  # Profit can be negative or positive
    insured = np.random.randint(1, 1000, num_rows)  # Random insured values (between 1 and 1000)
    gwp = np.random.uniform(10000, 50000, num_rows)  # Gross written premium between 10k and 50k
    claim_count = np.random.randint(0, 100, num_rows)  # Claim count between 0 and 100

    # Create a DataFrame with all the generated data
    df = pd.DataFrame({
        'sl': sl,
        'insured_type': insured_type,
        'insured_group': insured_group,
        'year': np.full(num_rows, year),
        'loss_ratio': loss_ratio,
        'filter_loss_ratio': filter_loss_ratio,
        'profit': profit,
        'insured': insured,
        'gwp': gwp,
        'claim_count': claim_count
    })

    return df


# Generate data for each year and write to CSV files with updated filenames
years = [2020, 2021, 2022, 2023, 2024]
for year in years:
    # Generate 10,000 rows of data for the given year
    df = generate_data(year)

    # Save the data to a CSV file with a slight change in filename
    file_name = f'insurance_data_v2_{year}.csv'  # Modified filename
    df.to_csv(file_name, index=False)
    print(f"Generated CSV for year {year}: {file_name}")
