import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = ':'
plt.rcParams['grid.alpha'] = 0.5

df=pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
print(df)
df.date_group = pd.to_datetime(df.date_group).dt.date
conv_pltf = pd.pivot_table(df,
                          values=['conversion'],
                          columns='platform',
                          index='date_group',
                          aggfunc='sum',
                          dropna=False).reset_index().round(2)
conv_pltf.columns = ['date_group', 'android', 'ios', 'web']
conv_pltf['roll_a'] = conv_pltf['android'].rolling(30, 1, center=True).mean().round(2)
conv_pltf['roll_i'] = conv_pltf['ios'].rolling(30, 1, center=True).mean().round(2)
conv_pltf['roll_w'] = conv_pltf['web'].rolling(30, 1, center=True).mean().round(2)

print(conv_pltf)

fig, (a, i, w) = plt.subplots(3, 1, figsize=(18, 9.6))
fig.tight_layout()

a.plot(conv_pltf['date_group'],
       conv_pltf['android'],
       color='lightgreen',
       label='android')
a.plot(conv_pltf['date_group'],
       conv_pltf['roll_a'],
       color='blue',
       ls='--',
       label='rolling average (30 days)')
i.plot(conv_pltf['date_group'],
       conv_pltf['ios'],
       color='lightblue',
       label='ios')
i.plot(conv_pltf['date_group'],
       conv_pltf['roll_i'],
       color='blue',
       ls='--',
       label='rolling average (30 days)')
w.plot(conv_pltf['date_group'],
       conv_pltf['web'],
       color='orange',
       label='web')
w.plot(conv_pltf['date_group'],
       conv_pltf['roll_w'],
       color='blue',
       ls='--',
       label='rolling average (30 days)')




plt.show()
