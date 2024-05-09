import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

fig, ax = plt.subplots(3, 1, figsize=(18, 9.6))

pltfrms = conv_pltf.columns.to_list()[1:4]
rolls = conv_pltf.columns.to_list()[4:]
colors = ['lightgreen', 'lightblue', 'orange']

for i, pltfrm in enumerate(pltfrms):
    ax[i].plot(conv_pltf['date_group'],
                  conv_pltf[pltfrm],
                  color=colors[i],
                  label=pltfrm)
    ax[i].plot(conv_pltf['date_group'],
                  conv_pltf[rolls[i]],
                  color='blue',
                  ls='--',
                  label='rolling average (30 days)')
    
    for x, y in zip(conv_pltf['date_group'], conv_pltf[pltfrm]):
        ax[i].text(x, y, int(y), fontsize=7, fontweight='normal', rotation=0, ha='center', va='center')

    ax[i].set(xlabel='Date',
              ylabel='Conversion, %',
              title=f'Picture 0{i+6} - Total Conversion - {pltfrm.title()}')

    #Settin up grids and ticks:
    ax[i].grid(axis='both', ls=':', color='grey')
    plt.sca(ax[i])
    plt.xticks(conv_pltf.date_group[::3])

    #Rotate xlabels to 45 deg:
    ax[i].tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
    ax[i].tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)

    #Setting up limits for x an y axes:
    xmargin = pd.Timedelta('3D') 
    ax[i].set_xlim(conv_pltf.date_group.min() - xmargin,
                   conv_pltf.date_group.max() + xmargin)

    #X-ticks - set alignment of rotated labels:
    plt.setp(ax[i].get_xticklabels(), ha='right')


fig.tight_layout()

plt.show()


