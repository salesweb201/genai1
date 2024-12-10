import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import base64
import time

# Function to load data from CSV (for initial load only)
def load_data():
    try:
        df = pd.read_csv("insurance_data.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Category', 'Dr/Cr', 'CustomerId'])

# Function to generate random data
def generate_random_data():
    categories = ['Rent', 'Groceries', 'Restaurant', 'Bills', 'Health', 'Salary']
    category = np.random.choice(categories)
    amount = np.random.randint(1, 1000)
    dr_cr = np.random.choice(['Dr', 'Cr'])
    return {
        'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Description': 'Random Transaction',
        'Amount': amount,
        'Category': category,
        'Dr/Cr': dr_cr,
        'CustomerId': np.random.randint(1, 100)  # Simulating customer IDs
    }

# Function to encode a name in Base64
def encode_name(name):
    return base64.b64encode(name.encode()).decode()

# Add custom CSS for improved styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
    }
    .panel {
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        font-size: 26px;
        background-color: rgb(117 238 228 / 95%);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    button.st-emotion-cache-1vt4y43.ef3psqc16 {
    background: #e61212;
    color: #fff;
}
    button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    button:hover {
        background-color: #45a049;
    }
    .scrollable {
        height: 300px;
        overflow-y: auto;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main app
def main():
    st.title("Family Expenses Tracker")

    # Load initial data from CSV to display
    if 'df' not in st.session_state:
        st.session_state.df = load_data()

    # DataFrame to hold added expenses during the session
    if 'added_expenses' not in st.session_state:
        st.session_state.added_expenses = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Category', 'Dr/Cr', 'CustomerId'])

    # Live data state
    if 'live_data_running' not in st.session_state:
        st.session_state.live_data_running = False

    # Combine loaded data and manually added data for display
    combined_data = pd.concat([st.session_state.df, st.session_state.added_expenses], ignore_index=True)

    # First Row: Display Pie Chart, Bar Graph, Heatmap
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown('<div class="panel">Expenses Pie Chart</div>', unsafe_allow_html=True)
        if not combined_data.empty:
            fig = px.pie(combined_data, names='Category', values='Amount', title='Expenses Distribution')
            st.plotly_chart(fig)
        else:
            st.markdown('<div class="panel">Load expenses to see the pie chart.</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="panel">Expenses Bar Graph</div>', unsafe_allow_html=True)
        if not combined_data.empty:
            bar_fig = px.bar(
                combined_data,
                x='Category',
                y='Amount',
                title='Expenses by Category',
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(bar_fig)
        else:
            st.markdown('<div class="panel">Load expenses to see the bar graph.</div>', unsafe_allow_html=True)

    with col6:
        st.markdown('<div class="panel">Expenses Heatmap</div>', unsafe_allow_html=True)
        if not combined_data.empty:
            heatmap_data = combined_data.groupby(['Category', 'Description'])['Amount'].sum().unstack(fill_value=0)
            heatmap_fig = ff.create_annotated_heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns.tolist(),
                y=heatmap_data.index.tolist(),
                colorscale='Viridis'
            )
            st.plotly_chart(heatmap_fig)
        else:
            st.markdown('<div class="panel">Load expenses to see the heatmap.</div>', unsafe_allow_html=True)

    # Second Row: Income/Expense Pie Chart
    col7, col8 = st.columns(2)

    with col7:
        st.markdown('<div class="panel">Income vs Expenses</div>', unsafe_allow_html=True)
        if not combined_data.empty:
            income_expense_data = combined_data.groupby('Dr/Cr')['Amount'].sum().reset_index()
            fig_income_expense = px.pie(income_expense_data, names='Dr/Cr', values='Amount', title='Income vs Expenses', color_discrete_sequence=['#1f77b4', '#ff7f0e'])
            st.plotly_chart(fig_income_expense)
        else:
            st.markdown('<div class="panel">Load data to see the income vs expenses.</div>', unsafe_allow_html=True)

    with col8:
        st.markdown('<div class="panel">Mostly Expensed Category</div>', unsafe_allow_html=True)
        if not combined_data.empty:
            most_expensed = combined_data.groupby('Category')['Amount'].sum().reset_index()
            fig_most_expensed_bar = px.bar(
                most_expensed,
                x='Category',
                y='Amount',
                title='Mostly Expensed Category',
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_most_expensed_bar)
        else:
            st.markdown('<div class="panel">Load expenses to see the mostly expensed categories.</div>', unsafe_allow_html=True)

    # Display DataFrame
    st.markdown('<div class="panel">Expenses Data</div>', unsafe_allow_html=True)
    if not combined_data.empty:
        st.dataframe(combined_data)
    else:
        st.markdown('<div class="panel">No data available.</div>', unsafe_allow_html=True)

    # Manual Entry
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="panel">Add Expense Manually</div>', unsafe_allow_html=True)
        with st.form("Add Manual Expense"):
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.01)
            category = st.selectbox("Category", options=combined_data['Category'].unique())
            dr_cr = st.selectbox("Dr/Cr", options=['Dr', 'Cr'])
            customer_id = st.number_input("CustomerId", min_value=1)
            submitted = st.form_submit_button("Add Expense")
            if submitted and description and amount > 0:
                new_row = {
                    'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Description': description,
                    'Amount': amount,
                    'Category': category,
                    'Dr/Cr': dr_cr,
                    'CustomerId': customer_id
                }
                st.session_state.added_expenses = pd.concat([st.session_state.added_expenses, pd.DataFrame([new_row])],
                                                            ignore_index=True)
                st.success("Expense added!")

                st.markdown("""<script>
                    const tableDiv = document.getElementById('expense_table_div');
                    tableDiv.scrollTop = tableDiv.scrollHeight;
                    </script>
                    """, unsafe_allow_html=True)

            elif submitted:
                st.error("Please provide a valid description and amount.")

        if st.button("Delete Last Expense") and not st.session_state.added_expenses.empty:
            st.session_state.added_expenses = st.session_state.added_expenses[:-1]
            st.success("Last expense deleted!")

    with col2:
        st.markdown('<div class="panel">Add Random Expense</div>', unsafe_allow_html=True)
        if st.button("Add Live Data Expense"):
            new_row = generate_random_data()
            st.session_state.added_expenses = pd.concat([st.session_state.added_expenses, pd.DataFrame([new_row])],
                                                        ignore_index=True)
            st.success("Random expense added!")

            st.markdown("""<script>
                const tableDiv = document.getElementById('expense_table_div');
                tableDiv.scrollTop = tableDiv.scrollHeight;
                </script>
                """, unsafe_allow_html=True)

        if st.button("Live Stream Data"):
            st.session_state.live_data_running = not st.session_state.live_data_running
            if st.session_state.live_data_running:
                st.success("Live data collection started!")
            else:
                st.success("Live data collection stopped!")

    # Live data adding logic
    if st.session_state.live_data_running:
        new_row = generate_random_data()
        st.session_state.added_expenses = pd.concat([st.session_state.added_expenses, pd.DataFrame([new_row])],
                                                    ignore_index=True)
        time.sleep(1)  # Add a delay to control the speed of live data generation
        st.rerun()  # Rerun the app to show the new data

    # Footer with copyright
    name = "Developed By Deepanshu"  # Replace with your actual name
    encoded_name = "RGV2ZWxvcGVkIEJ5IERlZXBhbnNodQ=="
    decoded_name = base64.b64decode(encoded_name.encode()).decode()
    st.markdown(f'<div style="text-align: center; margin-top: 20px; color: #3498db;">&copy; {decoded_name}</div>',
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()
