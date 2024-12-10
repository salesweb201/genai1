import pandas as pd
import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)

# List of possible values
insured_types = ['Health', 'Life', 'Property']
insured_groups = ['Individual', 'Family', 'Corporate']
years = list(range(2010, 2024))

# Generate random data
num_rows = 100  # You can change this number for more rows
data = []

for i in range(num_rows):
    sl = i + 1
    insured_type = random.choice(insured_types)
    insured_group = random.choice(insured_groups)
    year = random.choice(years)
    loss_ratio = round(random.uniform(0, 1) * 100, 2)  # Loss ratio in percentage
    filter_loss_ratio = round(random.uniform(0, 1) * 100, 2)
    profit = round(random.uniform(-10000, 50000), 2)
    insured = random.randint(100, 5000)
    gwp = random.randint(100000, 5000000)
    claim_count = random.randint(0, 200)

    # Append row to data list
    data.append(
        [sl, insured_type, insured_group, year, loss_ratio, filter_loss_ratio, profit, insured, gwp, claim_count])

# Create a DataFrame
df = pd.DataFrame(data,
                  columns=['sl', 'insured_type', 'insured_group', 'year', 'loss_ratio', 'filter_loss_ratio', 'profit',
                           'insured', 'gwp', 'claim_count'])

# Save to CSV
df.to_csv('insurance_data.csv', index=False)

# Show first few rows of the generated data
print(df.head())
