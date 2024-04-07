import streamlit as st
import pandas as pd
import base64
from src.models.model import DataImputer

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return None

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="imputed_data.csv">Download imputed data as CSV</a>'
    return href

st.write(""" ## Growth Rate Imputations for Time Series Data""")
st.write("""
##### Directions
This application is designed to impute missing values in datasets across time series data based on implied growth rates. 
The directions are clearly outlined on the sidebar. """)

st.write("""
First, upload your data in csv or xlsx format. Next, select your start and end periods (ie. years). 
Then, select how you would like to impute null values. 
Then, select either linear or exponential interpolation for filling these missing values. 
Finally, click the 'Impute Data' button to see the imputed data. Scroll down the page to preview the imputed data.
You can also click the 'Download imputed data as CSV' link to download the imputed data.""")

st.write("""
As the imputations are based on the implied growth rates between selected periods 
(or the average rates of all or some records), 
not all records need to have non-null values for the start and end periods, 
however each record must have data for either the start or end periods in order to complete the imputations. 
The application will impute the missing values based on the average growth rate of the available data.
""")

with st.sidebar:
    st.write("### 1.) Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=['csv', 'xlsx'])

df = None

if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.write("### Uploaded Data Preview")
        st.dataframe(df.head())

        # Sidebar for inputs
        with st.sidebar:
            st.write("### 2.) Column Selection")
            column_names = df.columns.tolist()
            start_year = st.selectbox("Select the Start Year Column:", column_names, key='start_year')
            end_year = st.selectbox("Select the End Year Column:", column_names, key='end_year')

            # Check if the selected columns contain non-numerical non-null data
            if not pd.to_numeric(df[start_year].dropna(), errors='coerce').notnull().all() or \
               not pd.to_numeric(df[end_year].dropna(), errors='coerce').notnull().all():
                st.error("Selected start or end year columns contain non-numerical, non-null data. "
                         "Please select different columns.")
                df = None  # Prevent further processing

            # Continue with other inputs if the data checks are passed
            if df is not None:
                st.write("### 3.) Missing Data Handling")
                option = st.radio(
                    "For years without any clear growth rates, "
                    "would you like their growth rates to be calculated using:",
                    ('An average of ALL rows', 'An average of rows with a SHARED CATEGORY'),
                    key='data_handling_option'
                )

                category_col = None
                if option == 'An average of rows with a SHARED CATEGORY':
                    category_col = st.selectbox("Select the column to categorize by:", column_names,
                                                index=0,
                                                key='category_column')

                st.sidebar.write("### 4.) Interpolation Method")
                interpolation_method = st.selectbox("Select the interpolation method:", ["Linear", "Exponential"],
                                                    key='interpolation_method')

                if st.button("Impute Data", key='impute_data'):
                    st.session_state['impute'] = True
                else:
                    st.session_state['impute'] = st.session_state.get('impute', False)

# Outside the sidebar, check if the button was pressed and display the imputed data
if 'impute' in st.session_state and st.session_state['impute'] and df is not None:
    # Check if df is defined and the impute button has been pressed
    imputer = DataImputer(df, start_year, end_year, category_col, interpolation_method)
    imputed_df = imputer.impute_data()

    if imputed_df is not None and not imputed_df.empty:
        st.write("### Imputed Data Preview")
        st.dataframe(imputed_df.head())
        st.markdown(get_table_download_link(imputed_df), unsafe_allow_html=True)
    else:
        st.error("Data imputation failed or no data to display.")
