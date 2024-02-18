# RUN_THIS_ONE_FOR_LEAGUE_DATA
# 
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
from sheets_client import writeToGoogleSheets

load_dotenv(".env")

sgt_base_url = os.environ['sgt_base_url']
sgt_id = os.environ['sgt_id']
sgt_scores_endpoint = os.environ['sgt_scores_endpoint']

api_url = f'{sgt_base_url}/{sgt_id}{sgt_scores_endpoint}'
response = requests.get(api_url)

if response.status_code == 200:
    api_data = response.json()

    columns = [
        'player_name', 
        'tourneyName', 
        'round', 
        'activeHole', 
        'total_gross', 
        'toPar_gross', 
        'courseName', 
        'teetype', 
        'PAR', 
        'rating', 
        'slope'
        ]

    # Create a DataFrame from the API data
    df = pd.DataFrame(api_data, columns=columns)

     # Convert relevant columns to numeric types
    df['total_gross'] = pd.to_numeric(df['total_gross'], errors='coerce')
    df['toPar_gross'] = pd.to_numeric(df['toPar_gross'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['slope'] = pd.to_numeric(df['slope'], errors='coerce')
    df['activeHole'] = pd.to_numeric(df['activeHole'], errors='coerce')
    
   

    # Calculate the handicap based on the average total_net score for each player
    #df['handicap'] = df.groupby('player_name')['total_net'].transform('mean')
    
    #df['differential'] = ((df['total_gross'] - df['rating']) * 113) / df['slope'] 
    #df['handicap'] = df.groupby('player_name')['differential'].transform('mean')

    #Create new field called new_total_gross that cleans up q-school rounds
    df['new_total_gross'] = np.where((df['activeHole'] > 18) & df['tourneyName'].str.contains('Q-School ', case=False),
                                 df['total_gross'] - 37,
                                 df['total_gross'])
    # Create a condition for activeHole less than 18
    condition = df['activeHole'] < 18

    # Exclude rows where 'activeHole' is less than 18
    df_filtered = df[df['activeHole'] >= 18]

   # Assuming 'qschool' rounds are identified in the 'round_type' column
    condition = df['tourneyName'] != 'Q-School (9-hole)'
   


   # Create a new column 'difference'
    df['PAR'] = df['total_gross'] - df['toPar_gross']

    print(df)

    # Set options to display all columns and rows
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    if not os.path.exists('output'):
        os.makedirs('output')
    
    df.to_csv(f'output/24_league_output.csv', index=False) 

    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Construct the output file name with the current date and time
    output_file_name = f'24_league_output_{current_date}.csv'

    # Save the DataFrame to the CSV file
    df.to_csv(f'output/{output_file_name}', index=False)

    writeToGoogleSheets(os.environ["spreadsheet_id"], os.environ["sheet_name"], "A1", df.values.tolist())

    # Display the DataFrame
    print(df)

    # Optionally, check the data types and structure of the DataFrame
    print(df.info())
    print(df.head())
    
else:
    print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
