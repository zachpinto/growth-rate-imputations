import pandas as pd
import numpy as np

class DataImputer:
    def __init__(self, dataframe, start_year, end_year, category_col=None, interpolation_method="Linear"):
        # model parameters
        self.dataframe = dataframe
        self.start_year = start_year
        self.end_year = end_year
        self.category_col = category_col
        self.interpolation_method = interpolation_method

    def impute_data(self):
        if self.category_col:
            if self.interpolation_method == "Linear":
                return self.impute_based_on_category(self.linear_interpolate)
            else:  # Exponential interpolation
                return self.impute_based_on_category(self.exponential_interpolate)
        else:
            if self.interpolation_method == "Linear":
                return self.impute_across_all(self.linear_interpolate)
            else:  # Exponential interpolation
                return self.impute_across_all(self.exponential_interpolate)

    def impute_based_on_category(self, interpolation_func):
        # Apply interpolation to each category group
        return self.dataframe.groupby(self.category_col, group_keys=False).apply(interpolation_func)

    def impute_across_all(self, interpolation_func):
        # Apply interpolation to the whole dataset
        return interpolation_func(self.dataframe)

    def linear_interpolate(self, df):
        # Interpolation logic to handle "backward" filling from the end year
        start_idx = df.columns.get_loc(self.start_year)
        end_idx = df.columns.get_loc(self.end_year) + 1

        # Backward fill from the end year to handle rows with data only in the end year
        df.iloc[:, start_idx:end_idx] = df.iloc[:, start_idx:end_idx].bfill(axis=1)

        # Now apply linear interpolation
        df.iloc[:, start_idx:end_idx] = df.iloc[:, start_idx:end_idx].interpolate(method='linear', axis=1)

        return df

    def exponential_interpolate(self, df):
        start_idx = df.columns.get_loc(self.start_year)
        end_idx = df.columns.get_loc(self.end_year) + 1

        # Compute growth rates for rows with both start and end year data
        rates = []
        for i, row in df.iterrows():
            if not pd.isna(row[self.start_year]) and not pd.isna(row[self.end_year]):
                rate = (row[self.end_year] / row[self.start_year]) ** (1 / (end_idx - start_idx - 1)) - 1
                rates.append(rate)

        avg_rate = np.mean(rates) if rates else 0  # Calculate average rate

        # Apply growth rate to all rows
        for i, row in df.iterrows():
            if not pd.isna(row[self.start_year]):
                # If there's a start year value, apply the specific or average growth rate
                rate = rates.pop(0) if rates else avg_rate
                for j in range(start_idx + 1, end_idx):
                    df.at[i, df.columns[j]] = df.at[i, df.columns[j - 1]] * (1 + rate)
            else:
                # For rows with only end year data, apply the average rate backwards
                for j in range(end_idx - 2, start_idx - 1, -1):
                    df.at[i, df.columns[j]] = df.at[i, df.columns[j + 1]] / (1 + avg_rate)

        return df
