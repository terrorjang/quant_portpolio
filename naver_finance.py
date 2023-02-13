import requests
from pathlib import Path
import pandas as pd
from datetime import date, timedelta

# 삼성전자
# symbol: 005930
# requestType: 1
# startTime: 20201223
# endTime: 20210907
# timeframe: day
# url = 'https://api.finance.naver.com/siseJson.naver?symbol=005930&requestType=1&startTime=20201223&endTime=20210907&timeframe=day'

def get_KOR_ticker():
    data_file = Path('./data/2023/02/12.csv')
    data = pd.read_csv(data_file)
    return data[['종목코드', '종목명']]


def get_naver_finance_data(symbol:str, start_date:str, end_date:str):
    print(symbol, start_date, end_date)
    url = f'https://api.finance.naver.com/siseJson.naver?symbol={symbol}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day'
    print(url)
    r = requests.get(url)
    print(r.text)
    
    

if __name__ == '__main__':
    delta_1day = timedelta(days=1)
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')
    
    KOR_ticker = get_KOR_ticker()
    for i, row in KOR_ticker.iterrows():
        print(i, row[0], row[1])
        get_naver_finance_data(row[0], start_date_str, end_date_str)
