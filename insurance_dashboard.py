import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="Insurance Data Dashboard", layout="wide")

# Load the dataset using the new Streamlit caching mechanism
@st.cache_data  # Cache data for performance (Streamlit updated method)
def load_data():
    # Load the CSV files for all years into one DataFrame
    all_files = ['insurance_data_v2_2020.csv', 'insurance_data_v2_2021.csv', 'insurance_data_v2_2022.csv']
    df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)
    return df

# Load data
df = load_data()

# Show basic information about the dataset
st.title("Insurance Data Dashboard")
st.write("This is the interactive dashboard for visualizing and filtering the insurance data.")
st.write(f"Total Rows: {df.shape[0]}")

# Filtering options in the sidebar
st.sidebar.header("Filter Data")

# Filter by Year (with search and multi-select)
years = df['year'].unique().tolist()
year_filter = st.sidebar.multiselect('Select Year(s):', years, default=years)

# Filter by Insured Type (with search and multi-select)
insured_types = df['insured_type'].unique().tolist()
insured_type_filter = st.sidebar.multiselect('Select Insured Type(s):', insured_types, default=insured_types)

# Filter by Loss Ratio Range (using a slider for range selection)
loss_ratio_min, loss_ratio_max = float(df['loss_ratio'].min()), float(df['loss_ratio'].max())
loss_ratio_filter = st.sidebar.slider('Select Loss Ratio Range:', loss_ratio_min, loss_ratio_max, (loss_ratio_min, loss_ratio_max))

# Apply filters to the DataFrame
filtered_df = df[
    (df['year'].isin(year_filter)) &
    (df['insured_type'].isin(insured_type_filter)) &
    (df['loss_ratio'] >= loss_ratio_filter[0]) &
    (df['loss_ratio'] <= loss_ratio_filter[1])
]

# Display filtered data
st.write(f"Filtered Data (Rows: {filtered_df.shape[0]})")

# Show the filtered DataFrame (Optional)
st.dataframe(filtered_df.head())

# --- Calculating Key Metrics ---
total_insured = max(0, filtered_df['insured'].sum())  # Ensure no negative values
total_profit = max(0, filtered_df['profit'].sum())  # Ensure no negative values

# Calculate total loss, making sure to take absolute value for loss profits
total_loss = max(0, filtered_df[filtered_df['profit'] < 0]['profit'].abs().sum())  # Apply abs() before summing
total_insured_profit = max(0, filtered_df[filtered_df['profit'] > 0]['profit'].sum())  # Ensure no negative values

# Pie Chart Data
metrics = {
    "Total Insured": total_insured,
    "Total Profit": total_profit,
    "Total Loss": total_loss,
    "Total Insured Profit": total_insured_profit
}

# --- Pie Chart Visualization ---
st.subheader("Key Metrics (Pie Charts)")

# Create a 2-column layout to display the charts side by side
col1, col2 = st.columns(2)

# Plot Pie Chart for Total Insured
with col1:
    st.write("### Total Insured")
    fig, ax = plt.subplots()
    ax.pie([total_insured, 1], labels=["Total Insured", "Other"], autopct='%1.1f%%', startangle=90, colors=["#ff7f0e", "#f0f0f0"])
    ax.set_title("Total Insured")
    st.pyplot(fig)

# Plot Pie Chart for Total Profit
with col2:
    st.write("### Total Profit")
    fig, ax = plt.subplots()
    ax.pie([total_profit, 1], labels=["Total Profit", "Other"], autopct='%1.1f%%', startangle=90, colors=["#2ca02c", "#f0f0f0"])
    ax.set_title("Total Profit")
    st.pyplot(fig)

# --- Additional Pie Charts for Profit and Loss ---
# Pie Chart for Total Insured Profit
with col1:
    st.write("### Total Insured Profit")
    fig, ax = plt.subplots()
    ax.pie([total_insured_profit, 1], labels=["Total Insured Profit", "Other"], autopct='%1.1f%%', startangle=90, colors=["#2ca02c", "#f0f0f0"])
    ax.set_title("Total Insured Profit")
    st.pyplot(fig)

# Pie Chart for Total Loss
with col2:
    st.write("### Total Loss")
    fig, ax = plt.subplots()
    ax.pie([total_loss, 1], labels=["Total Loss", "Other"], autopct='%1.1f%%', startangle=90, colors=["#d62728", "#f0f0f0"])
    ax.set_title("Total Loss")
    st.pyplot(fig)

# --- Profit and Loss Grouped Bar Chart ---
st.subheader("Profit and Loss by Insured Type (Grouped Bar Chart)")

# Separate profit and loss data
profit_data = filtered_df[filtered_df['profit'] > 0]
loss_data = filtered_df[filtered_df['profit'] < 0]

# Calculate total profit and loss by insured type, applying abs() before groupby for losses
profit_by_type = profit_data.groupby('insured_type')['profit'].sum()
loss_by_type = loss_data.groupby('insured_type')['profit'].apply(lambda x: x.abs().sum())  # Apply abs() here before groupby

# Combine profit and loss data into one DataFrame
profit_loss_by_type = pd.DataFrame({
    'Profit': profit_by_type,
    'Loss': loss_by_type
}).fillna(0)  # Fill NaN with 0 for types without profit or loss

# Define width for each bar
bar_width = 0.35

# Define position for each bar group
r1 = range(len(profit_loss_by_type))  # Positions for profit bars
r2 = [x + bar_width for x in r1]     # Positions for loss bars (offset)

fig, ax = plt.subplots(figsize=(10, 6))

# Plot the profit and loss bars side-by-side
ax.bar(r1, profit_loss_by_type['Profit'], color='#2ca02c', width=bar_width, edgecolor='grey', label='Profit')
ax.bar(r2, profit_loss_by_type['Loss'], color='#d62728', width=bar_width, edgecolor='grey', label='Loss')

# Add x-ticks in the middle of the two bars
ax.set_xticks([r + bar_width / 2 for r in r1])
ax.set_xticklabels(profit_loss_by_type.index)

# Set chart title and labels
ax.set_title("Profit and Loss by Insured Type")
ax.set_ylabel("Amount")
ax.set_xlabel("Insured Type")

# Add value labels on bars
for i in range(len(profit_loss_by_type)):
    ax.annotate(f'${profit_loss_by_type["Profit"].iloc[i]:,.2f}',
                xy=(r1[i], profit_loss_by_type["Profit"].iloc[i]),
                xytext=(0, 5),  # 5 points vertical offset
                textcoords='offset points',
                ha='center', va='bottom', color='black')
    ax.annotate(f'${profit_loss_by_type["Loss"].iloc[i]:,.2f}',
                xy=(r2[i], profit_loss_by_type["Loss"].iloc[i]),
                xytext=(0, 5),  # 5 points vertical offset
                textcoords='offset points',
                ha='center', va='bottom', color='black')

# Show the plot
st.pyplot(fig)
