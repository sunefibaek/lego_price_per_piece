import streamlit as st  
import pandas as pd  
import numpy as np  
  
def create_dataframe():  
    data = {  
        'col1': np.random.rand(8),  
        'col2': np.random.rand(8),  
        'col3': np.random.rand(8),  
        'col4': np.random.rand(8),  
    }  
    df = pd.DataFrame(data)  
    return df  
  
df = create_dataframe()  
  
# Add a button to refresh the page  
if st.button('Refresh Data'):  
    df = create_dataframe()  
  
# Add a multiselect dropdown to select which columns are visible  
columns = st.multiselect("Select the columns to display", df.columns.tolist(), default=df.columns.tolist())  
st.dataframe(df[columns])  
