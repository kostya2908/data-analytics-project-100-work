import requests
import pandas as pd

r_v = requests.get('https://data-charts-api.hexlet.app/visits?begin=2023-03-01&end=2023-09-01')
visits = pd.DataFrame(r_v.json())

def get_humans(x):
    if 'bot' in x.lower():
        return 'bot'
    else:
        return 'human'

visits['human_or_bot'] = visits['user_agent'].apply(lambda x: get_humans(x))
visits = visits[visits['human_or_bot'] == 'human'].drop(['human_or_bot'], axis=1)
visits.head()
visits['datetime'] = pd.to_datetime(visits['datetime'])#.dt.date
visits['visit_no'] = visits.groupby('visit_id').ngroup()

visits = visits.sort_values(by=['visit_id', 'datetime'], ascending=[True, False]).reset_index(drop=True)

visits = visits.groupby(['visit_id']).head(1).reset_index(drop=True)
visits.head(100)

visits['datetime'] = visits['datetime'].dt.date

visits = visits.sort_values(by='datetime', ascending=True).reset_index(drop=True)
#print(visits)

result = visits.groupby(['datetime', 'platform'], as_index=False).agg(visits=('visit_id', 'count'))
result.rename(columns={'datetime': 'date_group'}, inplace=True)
result.set_index(['date_group', 'platform'], inplace=True)

#result['join_id'] = result.groupby(['date_group', 'platform']).ngroup()
#print(result)



r_r = requests.get('https://data-charts-api.hexlet.app/registrations?begin=2023-03-01&end=2023-09-01')
regs = pd.DataFrame(r_r.json())
regs['datetime'] = pd.to_datetime(regs['datetime']).dt.date
regs_grouped = regs.groupby(['datetime', 'platform'], as_index=False).agg(registrations=('email', 'count'))
regs_grouped.rename(columns={'datetime': 'date_group'}, inplace=True)
regs_grouped.set_index(['date_group', 'platform'], inplace=True)
#regs_grouped['join_id'] = regs_grouped.groupby(['datetime', 'platform']).ngroup()
#print(regs_grouped)
#result['registrations'] = result['join_id'].map(regs_grouped.set_index('join_id')['registrations'])
#result.drop('join_id', axis=1, inplace=True)

result = result.join(regs_grouped, on=['date_group', 'platform'])
result['conversion'] = 100 * result['registrations'] / result['visits']
print(result)
result.to_json('/home/kostya/data-analytics-project-100/conversion.json', orient='table')

