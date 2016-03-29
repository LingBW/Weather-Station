# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:42:29 2016

@author: bling
"""

from pandas import *
from numpy import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 22})

sdf=read_csv('ARC-2016-03-18.txt',sep='\t',skiprows=2,parse_dates={'datet':[0]},header=None,index_col='datet') #skip_footer=1,
#print sdf#.index[:]
df=read_csv('weather-station1-output.txt',sep=',',skiprows=0,parse_dates={'datet':[1,2]},header=None,index_col='datet') #skip_footer=1,
#print df
#print df.index[0],df.index[-1]
ind = argwhere((sdf.index>=df.index[0]) & (sdf.index<=df.index[-1])); #print ind
# indexs
ids = []
for i in sdf.index[ind]:
    ids.append(int(argwhere(df.index==i)))#'''
#print ids
mwind = []; hwind = []; dics = []
for i in ids:
    if ids.index(i) == 0:
        fv = mean(df[3][:i+1])
        hv = max(df[3][:i+1])
        ds = mean(df[4][:i+1])
        mwind.append(fv);hwind.append(hv);dics.append(ds)
    else:
        fv = mean(df[3][i-9:i+1])
        hv = max(df[3][i-9:i+1])
        ds = mean(df[4][i-9:i+1])
        mwind.append(fv);hwind.append(hv);dics.append(ds)

#wind direction
print sdf[8][ind]
'''plt.title('Weather station wind direction comparision ')
plt.plot(sdf.index[ind],sdf[8][ind],label='WHOI-direction ave 354',linewidth=4) 
plt.plot(sdf.index[ind],dics,label='NOAA-direction ave %d'%mean(dics),linewidth=4) 
plt.legend(loc=0) 
plt.ylabel('Direction from')
plt.xlabel('March 18, 2016')#'''      
#print sdf.index[ind],sdf.index[196]
# wind speed
plt.title('Weather station wind speed comparision')
plt.plot(sdf.index[ind],sdf[6][ind]/0.514444,label='WHOI wind ave %.1f'%mean(sdf[6][ind]/0.514444),linewidth=4)
plt.plot(sdf.index[ind],sdf[7][ind]/0.514444,label='WHOI gust ave %.1f'%mean(sdf[7][ind]/0.514444),linewidth=4)
plt.plot(sdf.index[ind],mwind,label='NOAA wind ave %.1f'%mean(mwind),linewidth=4)
plt.plot(sdf.index[ind],hwind,label='NOAA gust ave %.1f'%mean(hwind),linewidth=4)
plt.legend(loc=0)
plt.ylabel('Wind speed(kts)')
plt.xlabel('March 18, 2016')
#plt.plot(df.index,df[3])#'''
plt.show()
