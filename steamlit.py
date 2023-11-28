import streamlit as st
import pandas as pd
import numpy as np

# Create a dictionary with four keys (col1, col2, col3, col4)
# The value for each is a list of 8 random numbers

def create_dataframe():
    # Create a dictionary with four keys (col1, col2, col3, col4)
    # The value for each is a list of 8 random numbers
    data = {
        'col1': np.random.rand(8),
        'col2': np.random.rand(8),
        'col3': np.random.rand(8),
        'col4': np.random.rand(8),
    }

    # Create the DataFrame using the dictionary
    df = pd.DataFrame(data)
    return df

# Print the DataFrame

# print("Hello, World!")
st.dataframe(df)
