from os import makedirs
import requests
import pandas as pd
from io import BytesIO
from pathlib import Path
from datetime import date, timedelta
import time

def krx_crawling2(tdate):
    data_path = Path(f'STK/{tdate[:4]}/{tdate[4:6]}/{tdate[6:]}.csv')
    if data_path.exists():
        return -1
    data_path.parent.mkdir(parents=True, exist_ok=True)
    generate_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    query_str_parms = {
            'mktId': 'STK', # KOSPI : STK, KOSDAQ : KSQ
            'trdDd': str(tdate),
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
            'name': 'fileDown',
            'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
    }

    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' #generate.cmd에서 찾아서 입력하세요
    }

    r = requests.get(generate_req_url, query_str_parms, headers=headers)

    download_req_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    form_data ={
        'code' : r.content
    }
    
    r= requests.post(download_req_url, form_data, headers=headers)
    df = pd.read_csv(BytesIO(r.content), encoding='euc-kr')
    df['date'] = tdate
    df.to_csv(data_path, index=False, index_label=None)
    
# krx_crawling2('20220905') 
delta_1day = timedelta(days=1)
target_date = date.today()
max_date = date(2000, 1, 1)

while True:
    if target_date < max_date:
        break
    tdate = target_date.strftime('%Y%m%d')
    target_date -= delta_1day
    
    if krx_crawling2(tdate) == -1:
        continue
    time.sleep(0.1)