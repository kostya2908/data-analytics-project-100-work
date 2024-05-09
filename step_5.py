import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns


df = pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
df.date_group = pd.to_datetime(df.date_group).dt.date

#Setup figure and 'axe':
fig, pic = plt.subplots(figsize=(18, 6))

#Data set for the Picture:
pict_01_bars = df.groupby('date_group').agg(visits=('visits', 'sum')).reset_index()

#Adding rolling value:
pict_01_bars['rolling'] = pict_01_bars[['visits']].rolling(30, 1, center=True).mean().round(0)
print(pict_01_bars)


#Picture creation (PYPLOT):
barchart = plt.bar(pict_01_bars['date_group'],
                   pict_01_bars['visits'],
                   color='orange',
                   label='visits count')

pic.set(xlabel='Date',
        ylabel='Quantity of visitors',
        title='Picture 01 - Total Visits')
       

linechart = plt.plot(pict_01_bars['date_group'],
                     pict_01_bars['rolling'],
                     color='blue',
                     linestyle='dashed',
                     label='rolling average (30 days)')
                     

#Settin up grids and ticks:
plt.grid(axis='both', ls=':', color='grey')
plt.yticks(np.arange(300, 1600, 100))
plt.xticks(pict_01_bars.date_group[::3])

#Rotate xlabels to 90 deg:
pic.tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
pic.tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)

#Auto set of figure's margins
fig.tight_layout()

#Setting up limits for x an y axes:
pic.set_ylim(300, 1500)
xmargin = pd.Timedelta('3D') 
pic.set_xlim(pict_01_bars.date_group.min() - xmargin,
             pict_01_bars.date_group.max() + xmargin)

#X-ticks - set alignment of rotated labels:
plt.setp(pic.get_xticklabels(), ha='right')

#Bar labels show with 90deg rotation, color, size..:
pic.bar_label(pic.containers[0], rotation=90, fontsize=7, color='black')

plt.legend(loc='upper center')
plt.show()


