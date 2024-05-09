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

#v_r_pvt['color'] = v_r_pvt['utm_source'].apply(lambda x: source_to_num(x))
#print(v_r_pvt)

#-------------------------------------------AXVSPAN----------------------------------------------
#------------------------------------------------------------------------------------------------
#axvspan - preparing limits:

axvs = v_r_pvt.reset_index().sort_values(['utm_source', 'date_group'])
axvs['prev_date'] = axvs.date_group.shift(1)
axvs['next_date'] = axvs.date_group.shift(-1)
axvs = axvs[['prev_date', 'date_group', 'next_date', 'utm_source']]

def get_start_end(a, B, c):
    if a == None or c == None:
        return True
    elif abs(B - a) > pd.Timedelta('1D') or abs(B - c) > pd.Timedelta('1D'):
        return True
    else:
        return False

axvs['flag'] = axvs.apply(lambda x: get_start_end(x.prev_date,
                                                  x.date_group,
                                                  x.next_date),
                          axis=1)

axvs.drop(['prev_date', 'next_date'], axis=1, inplace=True)
axvs = axvs[axvs.flag == True].drop('flag', axis=1).sort_values('date_group').reset_index(drop=True)
print(axvs)#.to_string())

axvs.utm_source.replace([None], 'no ads', inplace=True)

def get_color(x):
    match x:
        case 'google':
            return 'pink'
        case 'yandex':
            return 'lightblue'
        case 'vk':
            return 'palegoldenrod'
        case 'no ads':
            return 'white'

axvs['color'] = axvs.utm_source.apply(lambda x: get_color(x))
color_label = axvs.iloc[::2, 1:].reset_index(drop=True)
print(color_label)

axvs_4_fig = pd.DataFrame(axvs.date_group.values.reshape(-1, 2))
axvs_4_fig.columns = ['start', 'stop']
axvs_4_fig.reset_index(drop=True)
print(axvs_4_fig)
axvs_4_fig = axvs_4_fig.join(color_label)
print(axvs_4_fig)
axvs_4_fig = axvs_4_fig.iloc[::2, :].reset_index(drop=True)
print(axvs_4_fig)

#------------------------------------------------------------------------------------------------

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
#-------------------------------------------------------------------------------------------
#------------------------------------------PCOLORMESH---------------------------------------
'''
bckg = ax[0].pcolormesh(v_r_pvt.index,
                 ax[0].get_ylim(),
                 v_r_pvt['color'].values[:-1][np.newaxis],
                 cmap=ListedColormap(['white', 'pink', 'lightblue', 'lightyellow']), alpha=0.5)
'''
#-------------------------------------------------------------------------------------------

#Average line:
avg = ax[0].axhline(v_r_pvt['visits'].agg('mean'),
                    color='black',
                    linewidth=0.5,
                    ls='dashed',
                    dashes=(15, 5),
                    label='Average Number of Visits')

#-------------------------------------------------------------------------------------------
#-------------------------------------------AXVSPAN-----------------------------------------
for i, row in axvs_4_fig.iterrows():
    ax[0].axvspan(row.iloc[0],
                  row.iloc[1],
                  edgecolor='white',
                  facecolor=axvs_4_fig.color[i],
                  label=axvs_4_fig.utm_source[i].title() + ' ADS' if i in [0, 1, 4] else '')
#-------------------------------------------------------------------------------------------

#Registrations:
regs = ax[1].plot(v_r_pvt['registrations'],
           color='blue',
           linewidth=0.5,                       
           label='Registrations')
#Text labels:
for x, y in zip(v_r_pvt.index, v_r_pvt.registrations):
    ax[1].text(x, y, int(y),             
               fontsize=7)
#Color background:
#-------------------------------------------------------------------------------------------
#------------------------------------------PCOLORMESH---------------------------------------
'''
bckg = ax[1].pcolormesh(v_r_pvt.index,                       
                 ax[1].get_ylim(),                       
                 v_r_pvt['color'].values[:-1][np.newaxis],                       
                 cmap=ListedColormap(['white', 'pink', 'lightblue', 'lightyellow']),                                    alpha=0.5)
'''
#-------------------------------------------------------------------------------------------

#Average line:
avg = ax[1].axhline(v_r_pvt['registrations'].agg('mean'),
                    color='black',
                    linewidth=0.5,
                    ls='dashed',
                    dashes=(15, 5),
                    label='Average Number of Registrations')

#-------------------------------------------------------------------------------------------
#-------------------------------------------AXVSPAN-----------------------------------------
for i, row in axvs_4_fig.iterrows():
    ax[1].axvspan(row.iloc[0],
                  row.iloc[1],
                  edgecolor='white',
                  facecolor=axvs_4_fig.color[i],
                  label=axvs_4_fig.utm_source[i].title() + ' ADS' if i in [0, 1, 4] else '')
#-------------------------------------------------------------------------------------------

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

    ax[i].legend(loc='upper center', ncol=2)

#---------------------------------------PCOLORMESH----------------------------------
#Setting up colorbar:
'''
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
'''
#-----------------------------------------------------------------------------------


fig.tight_layout()
#plt.subplots_adjust(bottom=0.1, top=0.95, left=0.05, right=0.935, hspace=0.4)

plt.show()
