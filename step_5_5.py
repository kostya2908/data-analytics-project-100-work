import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
print(df)
df.date_group = pd.to_datetime(df.date_group).dt.date
conv_ttl = pd.pivot_table(df,
                          values=['visits', 'registrations'],
                          index='date_group',
                          aggfunc='sum',
                          dropna=False).reset_index().round(2)
conv_ttl['conv_ttl'] = (100 * conv_ttl.registrations / conv_ttl.visits).round(2)
conv_ttl['roll'] = conv_ttl['conv_ttl'].rolling(30, 1, center=True).mean().round(0)
print(conv_ttl)

fig, ax = plt.subplots(figsize=(18, 6))
plt.plot(conv_ttl['date_group'],
         conv_ttl['conv_ttl'],
         #marker='*',
         color='lightgreen',
         label='conversion total')

plt.plot(conv_ttl['date_group'],
         conv_ttl['roll'],
         color='blue',
         linestyle='dashed',
         label='rolling average (30 days)')

for x, y in zip(conv_ttl.date_group, conv_ttl.conv_ttl):
    plt.text(x, y, int(y), fontsize=7, fontweight='normal', rotation=0, ha='center', va='center')

ax.set(xlabel='Date',
       ylabel='Conversion, %',
       title='Picture 05 - Total Conversion')

#Settin up grids and ticks:
plt.grid(axis='both', ls=':', color='grey')
plt.yticks(np.arange(5, 35, 2.5))
plt.xticks(conv_ttl.date_group[::3])

#Rotate xlabels to 45 deg:
ax.tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
ax.tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)

#Auto set of figure's margins
fig.tight_layout()

#Setting up limits for x an y axes:
ax.set_ylim(5, 30)
xmargin = pd.Timedelta('3D') 
ax.set_xlim(conv_ttl.date_group.min() - xmargin,
            conv_ttl.date_group.max() + xmargin)

#X-ticks - set alignment of rotated labels:
plt.setp(ax.get_xticklabels(), ha='right')

plt.legend(loc='upper center')
plt.show()



