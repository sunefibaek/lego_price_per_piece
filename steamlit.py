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

# Add a button to convert the DataFrame to Excel  
if st.button('Convert to Excel'):  
    towrite = io.BytesIO()  
    downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)  
    towrite.seek(0)  # reset pointer  
    b64 = base64.b64encode(towrite.read()).decode()  # some strings  
    linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download Excel File</a>'  
    st.markdown(linko, unsafe_allow_html=True)

# Add a multiselect dropdown to select which columns are visible  
columns = st.multiselect("Select the columns to display", df.columns.tolist(), default=df.columns.tolist())  
st.dataframe(df[columns])  
