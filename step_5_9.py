import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from matplotlib.colors import ListedColormap

df = pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
df.date_group = pd.to_datetime(df.date_group).dt.date

cost_pvt = pd.pivot_table(df,
                          values='cost',
                          index='date_group',
                          aggfunc='sum',
                          dropna=False).reset_index()
cost_pvt.cost = cost_pvt.cost.astype(int)

source_pvt = df[['date_group', 'utm_source']].groupby(df['date_group']).head(1).set_index('date_group')

cost_source = cost_pvt.set_index('date_group').join(source_pvt['utm_source'], on='date_group')

def source_to_num(x):
    if x == None:
        return 0
    elif x == 'google':
        return 1
    elif x == 'yandex':
        return 2
    elif x == 'vk':
        return 3
    else:
        return 4

cost_source['color'] = cost_source['utm_source'].apply(lambda x: source_to_num(x))

fig, ax = plt.subplots(figsize=(18, 6))
total = plt.plot(#cost_source['date_group'], <-- when 'date_group' is index
                 cost_source['cost'],
                 color='red',
                 linewidth=0.5,
                 label='ADS cost')

for x, y in zip(cost_pvt.date_group, cost_pvt.cost):
    plt.text(x,
             y,
             int(y) if y > 0 else '',
             fontsize=7,
             fontweight='normal',
             rotation=0,
             ha='center',
             va='center')
'''
ax.pcolorfast((dt.date2num(cost_source.index.min()),
               dt.date2num(cost_source.index.max())),
              ax.get_ylim(),
              cost_source['color'].values[np.newaxis],
              cmap=ListedColormap(['lightgrey', 'pink', 'lightblue', 'lightyellow']),
              alpha=0.5)

ads = ax.pcolormesh(cost_source.index,
                    ax.get_ylim(),
                    cost_source['color'].values[:-1][np.newaxis],
                    cmap=ListedColormap(['white', 'pink', 'lightblue', 'lightyellow']),
                    alpha=0.5)
'''
average = plt.axhline(cost_source['cost'].agg('mean'),
                      color='lightgrey',
                      ls='--',
                      label='average ADS cost')
'''
cbar = fig.colorbar(ads)
#yticks = np.linspace(*cbar.ax.get_ylim(), 
cbar.set_ticklabels(['noADS', 'google', 'yandex', 'vk'])
#cbar.ax_tick_params(length=0)
'''
ax.set(xlabel='Date',
       ylabel='Cost, RUB',
       title='Picture 09 - Total Ad Campaign Cost')

#Settin up grids and ticks:
plt.grid(axis='both', ls=':', color='grey')
plt.yticks(np.arange(0, 950, 100))
plt.xticks(cost_pvt.date_group[::3])

#Rotate xlabels to 45 deg:
ax.tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
ax.tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)

#Setting up limits for x an y axes:
ax.set_ylim(-50, 950)
xmargin = pd.Timedelta('3D') 
ax.set_xlim(cost_pvt.date_group.min() - xmargin,
            cost_pvt.date_group.max() + xmargin)

#X-ticks - set alignment of rotated labels:
plt.setp(ax.get_xticklabels(), ha='right')

#print(cost_source['color'].values[np.newaxis].reshape(184,-1)[:-1])


#Auto set of figure's margins
fig.tight_layout()

plt.legend()
plt.show()
