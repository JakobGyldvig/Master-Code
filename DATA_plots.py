# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 12:44:44 2022

@author: jakob
"""
import pandas as pd
import matplotlib.pyplot as plt
dfesg= pd.read_csv("SP500/clean_data/esg_clean.csv")
dfe = pd.read_csv("SP500/clean_data/e_clean.csv")
dfs = pd.read_csv("SP500/clean_data/s_clean.csv")
dfg = pd.read_csv("SP500/clean_data/g_clean.csv")

dfe=dfe['VZ']
dfs=dfs['VZ']
dfg=dfg['VZ']

#beskrivelse af transformation af data.
dfesg.plot(x='Unnamed: 0',y='VZ', xlabel = "Date",ylabel = "Score", title = "Transformed data for Ticker: VZ", marker='.', label='ESG-Score' )
dfe.plot(linestyle='-.', label='E-Score')
dfs.plot(linestyle='-.', label='S-Score')
dfg.plot(linestyle='-.', label='G-Score')
plt.xlim(108,132)
plt.ylim(25, 95)
plt.legend()
plt.show()


df = pd.read_csv("SP500/clean_data/adj_data.csv")
# monthly return

df.plot(x='Unnamed: 0',y='VZ',linestyle=':',marker='.', label='VZ', ylabel='Monthly Return', xlabel='Date', title='Transformed daily prices to monthly return')
plt.xlim(815,839)
plt.ylim(-0.12,0.1)
plt.legend()
plt.show()




plt.plot(dfesg["Unnamed: 0"], dfesg["VZ"])
dfesg=dfesg.tail(24)


df['month_year'] = pd.to_datetime(dfesg['Unnamed: 0']).dt.to_period('M')
df.head()

dfesg=dfesg.set_index('Unnamed: 0')
plt.plot(dfesg["VZ"])


# Define plot space
fig, ax = plt.subplots(figsize=(10, 6))

# Define x and y axes
ax.scatter( use_index=True,
        dfesg["VZ"],
        marker = ',')
ax.set(title = "ESG-Score for Ticker: VZ transformed",
       xlabel = "Date",
       ylabel = "ESG-Score")
plt.show()

