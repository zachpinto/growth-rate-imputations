import streamlit as st
import pandas as pd


def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None


st.title('ChronoFill: Data Imputation Tool')

st.write("""
### About
This is an application designed to impute missing values in datasets across time series data based on growth or 
degrowth rates. 
Users can upload their data, select relevant columns for analysis, and choose how to handle missing data points.
""")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is not None:
        st.write("### File Uploaded Successfully!")
        st.write("Please select the beginning and end year columns.")

        # Display column headers for selection
        column_names = df.columns.tolist()
        start_year = st.selectbox("Select the Start Year Column:", column_names)
        end_year = st.selectbox("Select the End Year Column:", column_names)

        st.write("### Growth Rate Calculation for Missing Years")
        option = st.radio(
            "For years without any clear growth rates, would you like their growth rates to be calculated using:",
            ('An average of ALL rows', 'An average of rows with a SHARED CATEGORY'))

        if option == 'An average of rows with a SHARED CATEGORY':
            category_column = st.selectbox("Select the column to categorize by:", column_names, index=0)
            st.write(f"You've chosen to categorize by: {category_column}")
