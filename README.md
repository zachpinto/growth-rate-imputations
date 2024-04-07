Growth Rate Imputations for Time Series Data
==============================

This streamlit-based application is designed to impute missing values in datasets across time series data based on implied growth rates. 
It allows users to upload their data, select relevant columns for analysis, and choose how to handle missing data points with options for different interpolation methods.

## Features

- **Upload**: Users can upload their time series data in CSV or Excel formats.
- **Time Period Selection**: Users can specify which columns represent the start and end years for the imputation process.
- **Missing Data Handling**: The application provides options to calculate missing data points based on an average of all rows or an average of rows within the same category.
- **Interpolation Methods**: Users can choose between linear and exponential interpolation methods to fill in missing data points.
- **Download**: After imputation, users can download the resulting dataset directly from the application.


### Local Installation

#### Clone the repository:
```bash
git clone https://github.com/zachpinto/growth-rate-imputations.git
cd growth-rate-imputations
```

#### Install the required packages:
```bash
pip install -r requirements.txt
```

#### Run the Streamlit application:
```bash
streamlit run app.py
```

#### Demo:
As an example, you can use the `data/raw/demo.xlsx` file to test the application. 
The file contains sample time series data with missing values that can be imputed using the application.

The output data post-imputation is located in the `data/processed` folder as `imputed_data.csv`.

#### NOTE: The following packages are required for the Streamlit application to run properly:

- Python 3.6+
- Streamlit
- Pandas
- Numpy
- Openpyxl


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── models       
    │   │   │               
    │   │   ├── model.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

