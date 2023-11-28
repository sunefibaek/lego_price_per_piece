import requests
import pandas as pd
import os
from lib.get_sets import get_sets

def get_sets(theme, year): 
    """
    Retrieves LEGO sets data based on the specified theme and year.

    Args:
        theme (str): The theme of the LEGO sets to retrieve.
        year (str): The year of the LEGO sets to retrieve.

    Returns:
        pandas.DataFrame: A DataFrame containing the retrieved LEGO sets data.
            The DataFrame includes columns such as set number, name, theme, year,
            and retail prices in different regions.
    """

    sets_url = 'https://brickset.com/api/v3.asmx/getSets'
    sets_params = {
        'params': f"{{'theme':'{theme}','year':'{year}'}}",
        'apiKey': os.environ.get('BRICKLINK_APIKEY'),
        'userHash': os.environ.get('BRICKLINK_USERHASH')
    }

    sets_response = requests.get(sets_url, params=sets_params)

    if sets_response.status_code == 200:
        data = sets_response.json()
        df = pd.DataFrame(data['sets'])

        columns_to_drop = ["rating", "reviewCount", "packagingType", "availability", "instructionsCount", 
                           "additionalImageCount", "ageRange", "dimensions", "barcode", "reviewCount",
                           "extendedData", "lastUpdated", "themeGroup", "subtheme", "category", "instructionsCount",
                           "additionalImageCount", "released", "collection", "collections", "lastUpdated", "extendedData"]
        df_clean = df.drop(columns=columns_to_drop)

        df_clean['us_retail_price'] = df_clean['LEGOCom'].apply(lambda x: x.get('US', {}).get('retailPrice', None))  
        df_clean['uk_retail_price'] = df_clean['LEGOCom'].apply(lambda x: x.get('UK', {}).get('retailPrice', None))  
        df_clean['ca_retail_price'] = df_clean['LEGOCom'].apply(lambda x: x.get('CA', {}).get('retailPrice', None))  
        df_clean['de_retail_price'] = df_clean['LEGOCom'].apply(lambda x: x.get('DE', {}).get('retailPrice', None))  

        df_clean = df_clean.drop(columns=['LEGOCom'])

        #df_clean = df_clean.append(df_clean, ignore_index=True)

        return df_clean
    
    else:
        print('Error:', sets_response.status_code)
        return None

df_final = pd.DataFrame()
theme_url = 'https://brickset.com/api/v3.asmx/getThemes'
theme_params = {
    'apiKey': os.environ.get('BRICKLINK_APIKEY'),
}
theme_response = requests.get(theme_url, params=theme_params)

if theme_response.status_code == 200:

    data = theme_response.json()

    themes_df = pd.DataFrame(data['themes'])
    
    themes_df = themes_df.loc[themes_df['yearTo'] >= 2023]
    themes_df = themes_df.loc[themes_df['yearFrom'] < 2024]

    for index, row in themes_df.iterrows():
        theme = row['theme']
        year = row['yearFrom']
        result = get_sets(theme, 2023)
        df_final = df_final.append(result, ignore_index=True)

df_final.to_csv('df_final.csv', index=False)

no_of_sets = df_final.shape[0]
no_of_themes = themes_df.shape[0]
print(f'Extracted {no_of_sets} LEGO sets from {no_of_themes} themes.')

print(df_final.head())