import pandas as pd
import requests
import io

SPREADSHEET_URL = 'https://docs.google.com/spreadsheet/ccc?key=131pXI2LJht5g3otZO81oLts8w-K0dlrErg6xcPlbS6o&output=csv'
NON_VOTER_COLUMNS = ('Accommodation',	'Location',
                     '# guests', 'Price', 'Price/14', 'Perks', 'Mean ranking', 'Aggregated \nMean\nRank')


def download_csv(url):
    response = requests.get(url)
    assert response.status_code == 200, 'Unable to download csv'
    csv_string = response.content
    return pd.read_csv(io.StringIO(csv_string.decode('utf-8')), index_col='Accommodation')


def load_input_data(participants=None):
    data = download_csv(SPREADSHEET_URL)
    participants = [col for col in data.columns if
                    col not in NON_VOTER_COLUMNS] if participants is None else participants
    df = data[participants]
    return df
