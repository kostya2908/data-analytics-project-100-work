import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


df=pd.read_json('/home/kostya/data-analytics-project-100/ads.json')

#Pivot table for representing platforms as separate columns:
regs_pvt = pd.pivot_table(df,
                          values=['registrations'],
                          columns=['platform'],
                          index=['date_group'],
                          aggfunc='sum',
                          dropna=False).reset_index()
regs_pvt.columns = ['date_group', 'android', 'ios', 'web']
regs_pvt['date_group'] = pd.to_datetime(regs_pvt['date_group']).dt.date

tmp = pd.Timedelta('30D')
regs_pvt = regs_pvt[regs_pvt.date_group < regs_pvt.date_group.min() + tmp]

print(regs_pvt)

#Converting 'date_group' to numerical format:
x = date2num(regs_pvt['date_group'])
print(x)
shift = 0.3

fig, ax = plt.subplots(figsize=(18, 6))

w = ax.bar(x - shift,
           regs_pvt.web,
           width=0.3,
           color='orange',
           label='web')

a = ax.bar(x,
           regs_pvt.android,
           width=0.3,
           color='blue',
           label='android')

i = ax.bar(x + shift,
           regs_pvt.ios,
           width=0.3,
           color='red',
           label='ios')

#Setting up title and labels of axes:
ax.set(xlabel='Date',
       ylabel='Quantity of registrations',
       title='Picture 04 - Registrations by Platform')

#Settin up grids and ticks:
plt.grid(axis='both', ls=':', color='grey')
plt.yticks(np.arange(0, 300, 50))



#plt.xticks(regs_pvt.date_group[::3])<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<



#Rotate xlabels to 45 deg:
ax.tick_params(axis='x', labelsize=8, labelrotation=45, grid_alpha=0.33)
ax.tick_params(axis='y', labelsize=8, labelright=True, right=True, grid_alpha=0.33)
 
#Auto set of figure's margins
fig.tight_layout()

#Setting up limits for x an y axes:
ax.set_ylim(0, 125)
xmargin = pd.Timedelta('3D') 
ax.set_xlim(regs_pvt.date_group.min() - xmargin,
            regs_pvt.date_group.max() + xmargin)

#X-ticks - set alignment of rotated labels:
plt.setp(ax.get_xticklabels(), ha='right')

#Bar labels show with 90deg rotation, color, size..
for r1, r2, r3 in zip(w, a, i):
    h1 = r1.get_height()
    h2 = r2.get_height()
    h3 = r3.get_height()
    plt.text(r1.get_x() + r1.get_width()/2.,
             h1/2.,
             h1,
             ha='center',
             va='bottom',
             color='white',
             fontsize=6,
             fontweight='bold',
             rotation=90)
    plt.text(r2.get_x() + r2.get_width()/2.,
             h2/2.,
             h2,
             ha='center',
             va='bottom',
             color='white',
             fontsize=6,
             fontweight='bold',
             rotation=90)
    plt.text(r3.get_x() + r3.get_width()/2.,
             h3/2.,
             h3,
             ha='center',
             va='bottom',
             color='white',
             fontsize=6,
             fontweight='bold',
             rotation=90)

plt.legend(loc='upper center')

#Converting X axis back to date:
ax.set_xticks(regs_pvt.date_group[::3])


plt.show()


