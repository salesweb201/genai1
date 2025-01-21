import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="Insurance Data Dashboard", layout="wide")


# Load the dataset using Streamlit caching
@st.cache_data  # Streamlit's updated method for caching data
def load_data():
    # Load the CSV files for all years into one DataFrame
    all_files = ['insurance_data_xl2_2020.csv', 'insurance_data_xl2_2021.csv', 'insurance_data_xl2_2022.csv']
    df = pd.concat((pd.read_csv(file) for file in all_files), ignore_index=True)

    # Clean loss_ratio column if necessary (remove '%' and convert to float)
    df['loss_ratio'] = df['loss_ratio'].str.replace('%', '').astype(float)

    return df


# Load data
df = load_data()

# Show basic information about the dataset
st.title("Insurance Data Dashboard")
st.write("This is the interactive dashboard for visualizing and filtering the insurance data.")
st.write(f"Total Rows: {df.shape[0]}")

# Filter options in the sidebar
st.sidebar.header("Filter Data")

# Filter by Year (with search and multi-select)
years = df['year'].unique().tolist()
year_filter = st.sidebar.multiselect('Select Year(s):', years, default=years)

# Filter by Insured Type (with search and multi-select)
insured_types = df['insured_type'].unique().tolist()
insured_type_filter = st.sidebar.multiselect('Select Insured Type(s):', insured_types, default=insured_types)

# Filter by Loss Ratio Range (using a slider for range selection)
loss_ratio_min, loss_ratio_max = df['loss_ratio'].min(), df['loss_ratio'].max()
loss_ratio_filter = st.sidebar.slider('Select Loss Ratio Range:', loss_ratio_min, loss_ratio_max,
                                      (loss_ratio_min, loss_ratio_max))

# Apply filters to the DataFrame
filtered_df = df[
    (df['year'].isin(year_filter)) &
    (df['insured_type'].isin(insured_type_filter)) &
    (df['loss_ratio'] >= loss_ratio_filter[0]) &
    (df['loss_ratio'] <= loss_ratio_filter[1])
    ]

# Display filtered data
st.write(f"Filtered Data (Rows: {filtered_df.shape[0]})")
st.dataframe(filtered_df.head())

# --- Calculating Key Metrics ---
total_insured = filtered_df['insured'].sum()  # Sum of insured
total_profit = filtered_df['profit'].sum()  # Sum of profit
total_loss = filtered_df[filtered_df['profit'] < 0]['profit'].sum()  # Total loss (negative profit)
total_insured_profit = filtered_df[filtered_df['profit'] > 0]['profit'].sum()  # Total insured profit

# Pie Chart Data
metrics = {
    "Total Insured": total_insured,
    "Total Profit": total_profit,
    "Total Loss": total_loss,
    "Total Insured Profit": total_insured_profit
}

# --- Pie Chart Visualization for GWP and Loss Ratio ---
st.subheader("Year-wise GWP and Loss Ratio")

# Create a 2-column layout to display the charts side by side
col1, col2 = st.columns(2)

# Plot Pie Chart for 'GWP'
with col1:
    st.write("### Year-wise GWP")
    yearly_gwp = filtered_df.groupby('year')['gwp'].sum()
    fig, ax = plt.subplots()
    ax.pie(yearly_gwp, labels=yearly_gwp.index, autopct='%1.1f%%', startangle=90,
           colors=sns.color_palette("Set3", len(yearly_gwp)))
    ax.set_title("Year-wise GWP")
    st.pyplot(fig)

# Plot Pie Chart for 'Loss Ratio'
with col2:
    st.write("### Year-wise Loss Ratio")
    yearly_loss_ratio = filtered_df.groupby('year')['loss_ratio'].mean()

    # Ensure loss_ratio is formatted correctly for the pie chart
    yearly_loss_ratio = yearly_loss_ratio.round(1)  # Optional: round to 1 decimal place
    yearly_loss_ratio_str = yearly_loss_ratio.astype(str) + " %"

    fig, ax = plt.subplots()
    ax.pie(yearly_loss_ratio, labels=yearly_loss_ratio_str.index, autopct='%1.1f%%', startangle=90,
           colors=sns.color_palette("Set3", len(yearly_loss_ratio)))
    ax.set_title("Year-wise Loss Ratio")
    st.pyplot(fig)

# --- Table for Total GWP and Loss Ratio ---
st.subheader("Total GWP and Loss Ratio")

# Calculate total GWP and average loss ratio based on the selected filters
total_gwp = filtered_df['gwp'].sum()
average_loss_ratio = filtered_df['loss_ratio'].mean()

# Create a DataFrame for displaying the results
table_data = {
    "Metric": ["Total GWP", "Average Loss Ratio"],
    "Value": [f"${total_gwp:,.2f}", f"{average_loss_ratio:.2f} %"]
}

table_df = pd.DataFrame(table_data)

# Display the table
st.table(table_df)

# --- New Table: GWP and Loss Ratio by Year ---
st.subheader("Total GWP and Loss Ratio by Year")

# Calculate total GWP and average loss ratio for each year
yearly_summary = filtered_df.groupby('year').agg(
    total_gwp=('gwp', 'sum'),
    average_loss_ratio=('loss_ratio', 'mean')
).reset_index()

# Format the average loss ratio to 2 decimal places and append "%" symbol
yearly_summary['average_loss_ratio'] = yearly_summary['average_loss_ratio'].round(2).astype(str) + " %"

# Display the table for year-wise GWP and loss ratio
st.table(yearly_summary)

# --- Profit and Loss Grouped Bar Chart ---
st.subheader("Profit and Loss by Insured Type (Grouped Bar Chart)")

# Separate profit and loss data
profit_data = filtered_df[filtered_df['profit'] > 0]
loss_data = filtered_df[filtered_df['profit'] < 0]

# Calculate total profit and loss by insured type, applying abs() before groupby for losses
profit_by_type = profit_data.groupby('insured_type')['profit'].sum()
loss_by_type = loss_data.groupby('insured_type')['profit'].apply(
    lambda x: x.abs().sum())  # Apply abs() here before groupby

# Combine profit and loss data into one DataFrame
profit_loss_by_type = pd.DataFrame({
    'Profit': profit_by_type,
    'Loss': loss_by_type
}).fillna(0)  # Fill NaN with 0 for types without profit or loss

# Define width for each bar
bar_width = 0.35

# Define position for each bar group
r1 = range(len(profit_loss_by_type))  # Positions for profit bars
r2 = [x + bar_width for x in r1]  # Positions for loss bars (offset)

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

# --- Adding a Text Box for User Query ---
st.subheader("Ask a Question")

# Text box for the user to type their query
user_query = st.text_input("Enter your question (e.g., 'total gwp year wise in pie chart'): ")

# Handling the query for "total gwp year wise in pie chart"
if user_query and 'total gwp year wise in pie chart' in user_query.lower():
    st.write("### Total GWP Year-wise (Pie Chart)")

    # Plot Pie Chart for 'GWP'
    yearly_gwp = filtered_df.groupby('year')['gwp'].sum()
    fig, ax = plt.subplots()
    ax.pie(yearly_gwp, labels=yearly_gwp.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3", len(yearly_gwp)))
    ax.set_title("Year-wise GWP")
    st.pyplot(fig)
