import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator
import seaborn as sns


df = pd.read_json('/home/kostya/data-analytics-project-100/ads.json')
print(df)
df.date_group = pd.to_datetime(df.date_group).dt.date
print(df)
#print(df.date_group[::10])

fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Picture 01\nTotal Visits')

pict_01_bars = df.groupby('date_group').agg(visits=('visits', 'sum')).reset_index()
#print(pict_01_bars)

pict_01 = ax.bar(pict_01_bars.date_group, pict_01_bars.visits, align='edge', width=0.7)
#pict_01 = sns.barplot(x=pict_01_bars.date_group, y=pict_01_bars.visits)#, align='edge', width=0.7)

x_dates = pd.date_range(df.date_group.min(), df.date_group.max(), freq='7D')
#print(x_dates)

fig.subplots_adjust(bottom=0.2)

plt.xticks(x_dates, rotation=90)
plt.tick_params(direction='in')
ax.bar_label(pict_01, rotation=90, fontsize=7)

#fig.autofmt_xdate()

plt.show()


