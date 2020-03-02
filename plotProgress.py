from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys
import numpy as np
import seaborn as sns
savedir = os.getcwd()+"/"
output_format = ".png"

df = pd.read_csv(os.getcwd()+"/"+sys.argv[1])
df['timestamp_fixed'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d %H:%M:%S")
df = df.set_index('timestamp_fixed')

current_pagecount = df["pagecount"].iloc[-1]
current_wordcount = df["wordcount"].iloc[-1]

wc_color="orangered"
pc_color="royalblue"

# Plot with Combined progress
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every day
date_fmt = mdates.DateFormatter('%m-%d')

fig, ax = plt.figure(), plt.gca()
ax2= ax.twinx()
df.plot(y='pagecount',legend=None, ax=ax, color=pc_color)
df.plot(y='wordcount', legend=None, ax=ax2, color=wc_color)

ax.set_ylabel("Page Count", fontsize=16, color=pc_color)
ax2.set_ylabel("Word Count", fontsize=16,color=wc_color)
ax.set_xlabel('Date',fontsize=16)
ax.set_ylim(ymin=0)
ax2.set_ylim(ymin=0)

plt.annotate("{:,d} Pages".format(current_pagecount), xy=(.05,.88), xycoords="axes fraction",color=pc_color, fontsize=14)
plt.annotate("{:,d} Words".format(current_wordcount), xy=(.05,.8), xycoords="axes fraction",color=wc_color, fontsize=14)

#ax.xaxis.set_major_locator(months) Uncomment if you want month-level updates
ax.xaxis.set_minor_locator(days)
ax.xaxis.set_major_formatter(date_fmt)

# Uncomment if you want vertical lines at important points
"""
dates = {}
dates["Detector chapter \nsent for edits "] = "2019-09-22 15:30:00"
dates["Theory chapter \nsent for edits "] = "2019-10-20 21:57:00"

for title,dt in dates.items():
    xloc = pd.to_datetime(dt)
    ax.axvline(x=xloc, color='firebrick', linestyle='--',)
    plt.annotate(title, xy=(xloc, 100), color="firebrick", fontsize=10, ha="right")
"""

ax.tick_params(labelsize=12)
ax2.tick_params(labelsize=12)
plt.tight_layout()
plt.savefig(savedir+"progress"+output_format)

# Twitter-friendly
fig = plt.gcf()
fig.set_size_inches(2*fig.get_figheight(),fig.get_figheight(),forward=True)
plt.savefig(savedir+"progress_twitter"+output_format)
plt.close()

##### Time Delta Plot ####
def make_pages_plot(axis):
    df.plot(y='pagecount',legend=None, color=pc_color, ax=axis,label="Raw Data")
    done_resample_df =  df.resample('w').max()
    done_resample_df['pagecount'].plot(figsize=(12,8), color='salmon',label="Rolling 7-day Max", ax=axis)
    slope = pd.Series(np.gradient(done_resample_df["pagecount"].values), done_resample_df.index, name='slope')
    plt.sca(axis)
    plt.plot(done_resample_df['pagecount'].diff(), color="forestgreen",label="Rolling 7-Day Change")
    plt.ylabel("Pages",fontsize=14)

def make_words_plot(axis):
    df.plot(y='wordcount',legend=None, color=pc_color, ax=axis,label="Raw Data")
    done_resample_df =  df.resample('w').max()
    done_resample_df['wordcount'].plot(figsize=(12,8), color='salmon',label="Rolling 7-day Max",ax=axis)
    slope = pd.Series(np.gradient(done_resample_df["wordcount"].values), done_resample_df.index, name='slope')
    plt.sca(axis)
    plt.plot(done_resample_df['wordcount'].diff(), color="forestgreen",label="Rolling 7-Day Change")
    plt.ylabel("Words",fontsize=14)

def make_format():
    sns.despine()
    plt.ylim(bottom=0)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

fig, (ax1,ax2) = plt.subplots(ncols=1, nrows=2, sharex=True)
make_pages_plot(ax1)
make_format()
make_words_plot(ax2)
make_format()
plt.xlabel("Date",fontsize=14)
plt.legend(bbox_to_anchor=(1.2,1), loc="center",frameon=False,fontsize=14)

days = mdates.DayLocator()
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%b %Y')
ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(years_fmt)
plt.minorticks_off()
plt.tight_layout()
plt.savefig(savedir+"delta_plots"+output_format)
