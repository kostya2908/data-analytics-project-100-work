import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from matplotlib.colors import ListedColormap

df = pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
df.date_group = pd.to_datetime(df.date_group).dt.date
#print(df)

v_r_pvt = pd.pivot_table(df,
                         values=['visits', 'registrations', 'utm_source'],
                         index='date_group',
                         aggfunc={'visits': 'sum',
                                  'registrations': 'sum',
                                  'utm_source': 'first'},
                         dropna=False)#.reset_index()
v_r_pvt = v_r_pvt[['visits', 'registrations', 'utm_source']]
#print(v_r_pvt)

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

v_r_pvt['color'] = v_r_pvt['utm_source'].apply(lambda x: source_to_num(x))
print(v_r_pvt)

fig, ax = plt.subplots(2, 1, figsize=(18, 9))#, sharex=True)
#Visits:
vsts = ax[0].plot(v_r_pvt['visits'],
           color='blue',
           linewidth=0.5,
           label='Visits')
#Text labels:
for x, y in zip(v_r_pvt.index, v_r_pvt.visits):
    ax[0].text(x, y, int(y),
               fontsize=7)
#Color background:
bckg = ax[0].pcolormesh(v_r_pvt.index,
                 ax[0].get_ylim(),
                 v_r_pvt['color'].values[:-1][np.newaxis],
                 cmap=ListedColormap(['white', 'pink', 'lightblue', 'lightyellow']),
                 alpha=0.5)
#Average line:
avg = ax[0].axhline(v_r_pvt['visits'].agg('mean'),
              color='black',
              linewidth=0.5,
              ls='--',
              label='Average Number of Visits')
#Registrations:
regs = ax[1].plot(v_r_pvt['registrations'],
           color='green',
           linewidth=0.5,                       
           label='Registrations')
#Text labels:
for x, y in zip(v_r_pvt.index, v_r_pvt.registrations):
    ax[1].text(x, y, int(y),             
               fontsize=7)
#Color background:
bckg = ax[1].pcolormesh(v_r_pvt.index,                       
                 ax[1].get_ylim(),                       
                 v_r_pvt['color'].values[:-1][np.newaxis],                       
                 cmap=ListedColormap(['white', 'pink', 'lightblue', 'lightyellow']),                                    alpha=0.5)
#Average line:
avg = ax[1].axhline(v_r_pvt['registrations'].agg('mean'),            
              color='black',
              linewidth=0.5,
              ls='--',
              label='Average Number of Registrations')

#Appearance:
ax[0].set(xlabel='Date',
          ylabel='Unique Visits',
          title='Picture 10 - Visits During Marketing Active Days')
ax[1].set(xlabel='Date',
          ylabel='Unique Registrations',
          title='Picture 11 - Registrations During Marketing Active Days')
#Setting up grids and ticks:
for i in range(2):
    ax[i].grid(axis='both', ls=':', color='grey')
    ax[i].set_xticks(v_r_pvt.index[::3])
    #Rotate xlabels to 45 deg:
    ax[i].tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
    ax[i].tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)
    #Setting up limits for x an y axes:
    xmargin = pd.Timedelta('3D') 
    ax[i].set_xlim(v_r_pvt.index.min() - xmargin,
                   v_r_pvt.index.max() + xmargin)
    #X-ticks - set alignment of rotated labels:
    plt.setp(ax[i].get_xticklabels(), ha='right')
    ax[i].legend(loc='upper center')
#Setting up colorbar:
cbax = fig.add_axes((0.97, 0.1, 0.0175, 0.85))
cbar = plt.colorbar(bckg, cax=cbax)
cbar.ax.get_yaxis().set_ticks([])
for j, label in enumerate(['no ADS', 'google ADS', 'yandex ADS', 'vk ADS']):
    cbar.ax.text(0.55, (1.825 * j + 1) / 2.5,
                 label,
                 ha='center',
                 va='center',
                 rotation=90,
                 fontweight='medium')





#cax, kw = mpl.colorbar.make_axes([ax for ax in ax.flat])
#plt.colorbar(bckg, cax=cax, **kw)

#fig.tight_layout()
plt.subplots_adjust(bottom=0.1, top=0.95, left=0.05, right=0.935, hspace=0.4)

plt.show()
