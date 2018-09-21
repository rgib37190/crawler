
# coding: utf-8
import pandas as pd
import datetime as dt
import requests
import time

result = pd.read_html('https://btc.com/block?date=2016-01-01')
result = pd.DataFrame(result[0])
result = result.rename({0:'Height',1:'Relayed By',2:'Tx Count',3:'Stripped Size(B)',4:'Size(B)',5:'Weight',
                       6:'Avg Fee Per Tx',7:'Reward',8:'Time',9:'Block Version'},axis=1)
result = result.drop(0,axis=0)

date = []
for i in range(0,991):
    day_time = (dt.datetime(2016,1,2)+dt.timedelta(days=i)).strftime('%Y-%m-%d')
    date.append(day_time)

for datetime in date:
    try:
        url = 'https://btc.com/block?date='+datetime
        data = pd.read_html(requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}).text)
        blockchain_data = pd.DataFrame(data[0])
        blockchain_data = blockchain_data.rename({0:'Height',1:'Relayed By',2:'Tx Count',3:'Stripped Size(B)',4:'Size(B)',5:'Weight',
                       6:'Avg Fee Per Tx',7:'Reward',8:'Time',9:'Block Version'},axis=1)
        blockchain_data = blockchain_data.drop(0,axis=0)
        result = pd.merge(result,blockchain_data,how='outer')
        print('finish:%s' %datetime)
    except:
        print('No table found time is:%s' %datetime)
    time.sleep(60)

result.to_csv('blockchain_data.csv')





