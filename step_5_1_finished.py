import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
df.date_group = pd.to_datetime(df.date_group).dt.date

#Setup figure and 'axe':
fig, pic = plt.subplots(figsize=(18, 6))

#Data set for the Picture:
pict_01_bars = df.groupby('date_group').agg(visits=('visits', 'sum')).reset_index()

#Picture creation:
sns.barplot(data=pict_01_bars,
            x=pict_01_bars.date_group,
            y=pict_01_bars.visits,
            color='orange').set(xlabel='Date',
                                ylabel='Quantity of visitors',
                                title='Picture 01 - Total Visits')

#Settin up grids and ticks:
plt.grid(axis='both', ls=':', color='grey')
plt.yticks(np.arange(300, 1600, 100))

#Rotate xlabels to 90 deg:
pic.tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
pic.tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)

#Auto set of figure's margins
fig.tight_layout()

#Setting up limits for x an y axes:
pic.set_ylim(300, 1500)
x, y = pic.get_xlim(), pic.get_ylim()
xmargin = 0.01 * (x[1] - x[0])
pic.set_xlim(x[0] - xmargin, x[1] + xmargin)

#X-ticks - each 8th date instead of all set:
pic.set_xticks(pic.get_xticks()[::3])

#X-ticks - set alignment of rotated labels:
plt.setp(pic.get_xticklabels(), ha='right')

#Bar labels show with 90deg rotation, color, size..:
pic.bar_label(pic.containers[0], rotation=90, fontsize=7, color='black')

plt.show()


