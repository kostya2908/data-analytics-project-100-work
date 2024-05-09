import pandas as pd


conversion = pd.read_json('/home/kostya/data-analytics-project-100/conversion.json',
                          orient='table').reset_index()
conversion['date_group'] = pd.to_datetime(conversion['date_group']).dt.date
conversion.set_index(['date_group', 'platform'], inplace=True)
print(conversion)

url = 'https://drive.google.com/file/d/12vCtGhJlcK_CBcs8ES3BfEPbk6OJ45Qj/view'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
data = pd.read_csv(url)
data.date = pd.to_datetime(data.date).dt.date
data.rename(columns={'date': 'date_group'}, inplace=True)
data.set_index('date_group', inplace=True)
print(data)

result_4 = conversion.join(data[['cost', 'utm_source']], on='date_group')
print(result_4)
result_4.reset_index(inplace=True)
print(result_4)
result_4.date_group = pd.to_datetime(result_4.date_group).dt.strftime('%Y-%m-%d')
print(result_4)
result_4.to_json('/home/kostya/data-analytics-project-100/ads.json')


