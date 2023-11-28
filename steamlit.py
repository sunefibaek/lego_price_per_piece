import streamlit as st  
import pandas as pd  
import numpy as np  
import io
  
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

# Add a button to convert the DataFrame to Excel  
if st.button('Convert to Excel'):  
    towrite = io.BytesIO()  
    df[columns].to_excel(towrite, index=False)  
    towrite.seek(0)  
    st.download_button(  
        label="Download Excel File",  
        data=towrite,  
        file_name='dataframe.xlsx',  
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  
    ) 
# Add a multiselect dropdown to select which columns are visible  
columns = st.multiselect("Select the columns to display", df.columns.tolist(), default=df.columns.tolist())  
st.dataframe(df[columns])  
