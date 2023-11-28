import requests
import pandas as pd
import os

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

        df_clean = df_clean.append(df_clean, ignore_index=True)

        return df_clean
    
    else:
        print('Error:', sets_response.status_code)
        return None
    

def get_sets_all(year):   
    sets_url = 'https://brickset.com/api/v3.asmx/getSets'  
    page = 1  
    all_sets_df = pd.DataFrame()  
  
    while True:  
        sets_params = {  
            'params': f"{{'year':'{year}', 'pageNumber': '{page}', 'pageSize':'50'}}",  
            'apiKey': os.environ.get('BRICKLINK_APIKEY'),  
            'userHash': os.environ.get('BRICKLINK_USERHASH')  
        }  
  
        sets_response = requests.get(sets_url, params=sets_params)  
          
        if sets_response.status_code == 200:  
            data = sets_response.json()  
  
            # If no more data, break the loop  
            if not data['sets']:  
                break  
  
            df = pd.DataFrame(data['sets'])  
            # Drop unnecessary columns, add needed ones and append to the final DataFrame  
            all_sets_df = pd.concat([all_sets_df, df])  
  
            # Increment page for the next request  
            page += 1  
        else:  
            print('Error:', sets_response.status_code)  
            break  
  
    return all_sets_df  


import os
import requests
import pandas as pd

def get_all_sets(year):
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
    page = 1
    all_sets_df = pd.DataFrame()

    while True:
        sets_params = {
            'params': f"{{'year':'{year}', 'pageNumber': '{page}', 'pageSize':'50'}}",
            'apiKey': os.environ.get('BRICKLINK_APIKEY'),
            'userHash': os.environ.get('BRICKLINK_USERHASH')
        }

        sets_response = requests.get(sets_url, params=sets_params)
        
        if sets_response.status_code == 200:
            data = sets_response.json()
            print(data)

            # If no more data, break the loop
            if not data['sets']:
                break

            df = pd.DataFrame(data['sets'])

            columns_to_drop = ["rating", "reviewCount", "packagingType", "availability", "instructionsCount",
                           "additionalImageCount", "ageRange", "dimensions", "barcode", "reviewCount",
                           "extendedData", "lastUpdated", "themeGroup", "subtheme", "category", "instructionsCount",
                           "additionalImageCount", "released", "collection", "collections", "lastUpdated", "extendedData"]
            df = df.drop(columns=columns_to_drop)

            df['us_retail_price'] = df['LEGOCom'].apply(lambda x: x.get('US', {}).get('retailPrice', None))
            df['uk_retail_price'] = df['LEGOCom'].apply(lambda x: x.get('UK', {}).get('retailPrice', None))
            df['ca_retail_price'] = df['LEGOCom'].apply(lambda x: x.get('CA', {}).get('retailPrice', None))
            df['de_retail_price'] = df['LEGOCom'].apply(lambda x: x.get('DE', {}).get('retailPrice', None))
            df = df.drop(columns=['LEGOCom'])

            df['us_price_per_piece'] = df['us_retail_price'] / df['pieces']
            df['uk_price_per_piece'] = df['uk_retail_price'] / df['pieces']
            df['ca_price_per_piece'] = df['ca_retail_price'] / df['pieces']
            df['de_price_per_piece'] = df['de_retail_price'] / df['pieces']
            
            all_sets_df = pd.concat([all_sets_df, df])

            #page += 1
        else:
            print('Error:', sets_response.status_code)
            break

    return all_sets_df


test_df = get_all_sets(2023)
print(test_df.columns)
shape = test_df.shape
print(shape)

