# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 01:29:26 2022

@author: jakob
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 17:53:13 2022

@author: Jakob
"""

#%% Modules

import pandas as pd
import numpy as np

import os

#%% Clean ESG

def clean_esg_scores(sheet_name, header_idx, adj_close_df):
    
    load_path = "CAC40/raw_data/data_esg.xlsx"
    esg_data = pd.read_excel(load_path, sheet_name=sheet_name, header=header_idx)
    esg_data.columns = esg_data.columns.str.replace(" FP Equity", "")
    #esg_data.columns = esg_data.columns.str.replace(" UW Equity", "")
    #esg_data = esg_data.drop(columns=['CEG', 'OGN'])
    esg_data = esg_data.iloc[:-1 , :]
    esg_data.rename(columns={'Dates': 'Date'}, inplace=True)

    esg_data = esg_data.drop('Unnamed: 0', axis=1)
    esg_data.set_index('Date', inplace=True)

    esg_data = esg_data.interpolate(method = 'linear', axis = 0)
    esg_data = esg_data.fillna(method='bfill')

    esg_new_data = pd.DataFrame()
    col = esg_data.columns
    esg_new_data[col[0]] = adj_close_df['Date'].dt.date.map(esg_data.set_index(esg_data.index.date)[col[0]])
    for i in range(1, len(col)):
        esg_new_data[col[i]] = adj_close_df['Date'].dt.date.map(esg_data.set_index(esg_data.index.date)[col[i]])

    esg_new_data = esg_new_data.interpolate(method = 'linear', axis = 0)
    #esg_new_data = esg_new_data.dropna(axis=1)

    return esg_new_data.dropna(axis=0)

#%% SP500

adj_close_df =  pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\SP500\raw_data\Jakob_Gyldvig.xlsx', sheet_name='Prices Copy', header=7)

adj_close_df.columns= adj_close_df.columns.str.replace(" UN Equity", "")
adj_close_df.columns =adj_close_df.columns.str.replace(" UW Equity", "")


adj_close_df = adj_close_df.drop(columns=['CEG', 'OGN'])
adj_close_df = adj_close_df.iloc[:-1 , :]
adj_close_df.rename(columns={'Dates': 'Date'}, inplace=True)

adj_close_df = adj_close_df.drop('Unnamed: 0', axis=1)
adj_close_df.set_index('Date', inplace=True)
adj_close_df.index = pd.to_datetime(adj_close_df.index)
adj_close_df = adj_close_df.pct_change().resample('BM').agg(lambda x: (x+1).prod()-1)
adj_close_df= adj_close_df.loc[:'2021-12-31']

adj_close_df=adj_close_df.fillna(method='bfill')
adj_close_df= adj_close_df.fillna(method='ffill')

for col in adj_close_df.columns:
    if adj_close_df[col].isnull().all():

        print(col)


download_path = 'SP500/clean_data/Year/adj_data.csv'
adj_close_df.to_csv(download_path, index=True)

#%%
load_path = "CAC40/raw_data/market.csv"

raw_data = pd.read_csv(os.path.join(os.getcwd(), load_path), header=[0,1], index_col=0)

adj_close_df = raw_data['Adj Close']
adj_close_df = adj_close_df.interpolate(method = 'linear', axis = 0)
adj_close_df.index = pd.to_datetime(adj_close_df.index)
adj_close_df = adj_close_df.pct_change().resample('BYS').agg(lambda x: (x+1).prod()-1)
adj_close_df = adj_close_df.loc[:'2021-12-31']
#adj_close_df = adj_close_df.drop(columns=['CEG', 'OGN'])

download_path = 'CAC40/clean_data/Year/market.csv'
adj_close_df.to_csv(download_path, index=True)

#%% ESG Clean

adj_close_df['Date'] = adj_close_df.index
esg_overall = clean_esg_scores('ESG Copy', 7, adj_close_df)
e_score = clean_esg_scores('E (2)', 7, adj_close_df)
s_score = clean_esg_scores('S (2)', 7, adj_close_df)
g_score = clean_esg_scores('G (2)', 7, adj_close_df)

esg_overall.to_csv('CAC40/clean_data/Year/esg_clean.csv', index=True)
e_score.to_csv('CAC40/clean_data/Year/e_clean.csv', index=True)
s_score.to_csv('CAC40/clean_data/Year/s_clean.csv', index=True)
g_score.to_csv('CAC40/clean_data/Year/g_clean.csv', index=True)

#%% Farma-French

load_path = "SP500/raw_data/farma_french_3factor.csv"
farma_french = pd.read_csv(load_path, skiprows = 3)
farma_french = farma_french.iloc[:1146]

download_path = 'SP500/clean_data/farma_french.csv'
farma_french.to_csv(download_path, index=True)


#%%5 factor
load_path = "SP500/raw_data/5 factor.csv"
f5 = pd.read_csv(load_path, skiprows = 3)
f5= f5.iloc[:702]

download_path = 'SP500/clean_data/5fac.csv'
f5.to_csv(download_path, index=True)



#%% Trades

Trades= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\CAC40\raw_data\data_esg.xlsx', sheet_name='TRADES ON A DAY', header=7)

Trades.columns= Trades.columns.str.replace(" FP Equity", "")
#Trades.columns =Trades.columns.str.replace(" UW Equity", "")

#Trades = Trades.drop(columns=['CEG', 'OGN'])
Trades = Trades.iloc[:-1 , :]
Trades.rename(columns={'DATES': 'Date'}, inplace=True)

Trades = Trades.drop('Unnamed: 0', axis=1)
Trades.set_index('Date', inplace=True)
Trades.index = pd.to_datetime(Trades.index)
Trades=Trades.resample('BYS').sum()
Trades= Trades.loc[:'2021-12-31']

Trades=Trades.fillna(method='bfill')
Trades= Trades.fillna(method='ffill')
Trades.to_csv('CAC40/clean_data/Year/Trades.csv', index=True)

#%%P/B
pb= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\CAC40\raw_data\data_esg.xlsx', sheet_name='Book_ratio', header=7)

pb.columns= pb.columns.str.replace(" FP Equity", "")
#pb.columns =pb.columns.str.replace(" UW Equity", "")

#pb = pb.drop(columns=['CEG', 'OGN'])
pb = pb.iloc[:-1 , :]
pb.rename(columns={'DATES': 'Date'}, inplace=True)

pb = pb.drop('Unnamed: 0', axis=1)

pb=pb.groupby([pb['Date'].dt.year, pb['Date'].dt.year], as_index=False).last()
pb.set_index('Date', inplace=True)
pb= pb.loc[:'2021-12-31']
pb= pb.fillna(method='bfill')
pb= pb.fillna(method='ffill')

for col in pb.columns:
    if pb[col].isnull().all():

        print(col)



pb.to_csv('CAC40/clean_data/Year/PB.csv', index=True)

#%%PE værdier

pe= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\CAC40\raw_data\data_esg.xlsx', sheet_name='PE', header=7)

pe.columns= pe.columns.str.replace(" FP Equity", "")
#pe.columns =pe.columns.str.replace(" UW Equity", "")

#pe = pe.drop(columns=['CEG', 'OGN', ])
pe = pe.iloc[:-1 , :]
pe.rename(columns={'DATES': 'Date'}, inplace=True)

pe = pe.drop('Unnamed: 0', axis=1)
#pe = pe.drop('Unnamed: 1', axis=1)

pe=pe.groupby([pe['Date'].dt.year, pe['Date'].dt.year], as_index=False).last()
pe.set_index('Date', inplace=True)
pe= pe.loc[:'2021-12-31']
pe= pe.fillna(method='bfill')
pe= pe.fillna(method='ffill')


for col in pe.columns:
    if pe[col].isnull().all():

        print(col)



pe=pe.dropna(axis=0)

pe.to_csv('CAC40/clean_data/Year/PE.csv', index=True)
#%%Return on assets
GP= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\CAC40\raw_data\data_esg.xlsx', sheet_name='Return on Assets', header=7)

GP.columns= GP.columns.str.replace(" FP Equity", "")
#GP.columns =GP.columns.str.replace(" UW Equity", "")

#GP = GP.drop(columns=['CEG', 'OGN'])
GP = GP.iloc[:-1 , :]
GP.rename(columns={'DATES': 'Date'}, inplace=True)

GP = GP.drop('Unnamed: 0', axis=1)
#GP = GP.drop('Unnamed: 1', axis=1)

GP=GP.groupby([GP['Date'].dt.year, GP['Date'].dt.year], as_index=False).last()
GP.set_index('Date', inplace=True)
GP= GP.loc[:'2021-12-31']
GP= GP.fillna(method='bfill')
GP= GP.fillna(method='ffill')
for col in GP.columns:
    if GP[col].isnull().all():

        print(col)

GP.to_csv('CAC40/clean_data/Year/ROA.csv', index=True)

#%%Market CAP


MC= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\CAC40\raw_data\data_esg.xlsx', sheet_name='Market_cap', header=7)

MC.columns= MC.columns.str.replace(" FP Equity", "")
#MC.columns =MC.columns.str.replace(" UW Equity", "")

#MC = MC.drop(columns=['CEG', 'OGN'])
MC = MC.iloc[:-1 , :]
MC.rename(columns={'DATES': 'Date'}, inplace=True)

MC = MC.drop('Unnamed: 0', axis=1)
#MC = MC.drop('Unnamed: 1', axis=1)

MC=MC.groupby([MC['Date'].dt.year, MC['Date'].dt.year], as_index=False).last()
MC.set_index('Date', inplace=True)
MC= MC.loc[:'2021-12-31']
MC= MC.fillna(method='bfill')
MC= MC.fillna(method='ffill')

for col in MC.columns:
    if MC[col].isnull().all():

        print(col)


MC.to_csv('CAC40/clean_data/Year/MC.csv', index=True)
#%%EBITDA

EB= pd.read_excel(r'C:\Users\jakob\OneDrive\Skrivebord\DATA\david\SP500\raw_data\Jakob_Gyldvig.xlsx', sheet_name='operating margins', header=7)

EB.columns= EB.columns.str.replace(" UN Equity", "")
EB.columns =EB.columns.str.replace(" UW Equity", "")

EB = EB.drop(columns=['CEG', 'OGN'])
EB = EB.iloc[:-1 , :]
EB.rename(columns={'Dates': 'Date'}, inplace=True)

EB = EB.drop('Unnamed: 0', axis=1)
#EB= EB.drop('Unnamed: 1', axis=1)

EB=EB.groupby([EB['Date'].dt.year, EB['Date'].dt.month], as_index=False).last()
EB.set_index('Date', inplace=True)
EB= EB.loc['2012-12-31':'2021-12-31']
EB= EB.fillna(method='bfill')
EB= EB.fillna(method='ffill')

for col in EB.columns:
    if EB[col].isnull().all():

        print(col)


EB.to_csv('SP500/clean_data/OM.csv', index=True)