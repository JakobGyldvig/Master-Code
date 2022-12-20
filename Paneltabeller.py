# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 16:28:42 2022

@author: jakob
"""

#%% Modules

import numpy as np
import pandas as pd

from ols_cls import factmod

#%% Hyper-parameters

back_time = 120
forward_time = 1
esg_quantile = 0.0

#%% Load Data
drop_lst=['OTIS',
'FOX',
'NLOK',
'MTCH',
'DPZ',
'WBD',
'APA',
'GOOG',
'BRK/B']

drop_lst1=['OTIS',
'FOX',
'NLOK',
'MTCH',
'DPZ',
'WBD',
'APA',
'GOOG']
#'BRK/B',
df1= pd.read_csv("SP500/clean_data/adj_data.csv").drop(columns=drop_lst1)
df = pd.read_csv("SP500/clean_data/Year/adj_data.csv").drop(columns=drop_lst)
dfe = pd.read_csv("SP500/clean_data/e_clean.csv").drop(columns=drop_lst)
dfs = pd.read_csv("SP500/clean_data/s_clean.csv").drop(columns=drop_lst)
dfg = pd.read_csv("SP500/clean_data/g_clean.csv").drop(columns=drop_lst)
dfesg= pd.read_csv("SP500/clean_data/esg_clean.csv").drop(columns=drop_lst)
df_farma_french = pd.read_csv("SP500/clean_data/farma_french.csv")
df5=pd.read_csv("SP500/clean_data/5fac.csv")
ROA=pd.read_csv("SP500/clean_data/ROA.csv").drop(columns=drop_lst)
PB=pd.read_csv("SP500/clean_data/PB.csv").drop(columns=drop_lst)#1
#PE=pd.read_csv("SP500/clean_data/Year/PE.csv").drop(columns=drop_lst)
Trades=pd.read_csv("SP500/clean_data/Trades.csv",).drop(columns=drop_lst)
MC=pd.read_csv("SP500/clean_data/MC.csv",).drop(columns=drop_lst)#1
OM=pd.read_csv("SP500/clean_data/OM.csv",).drop(columns=drop_lst)
#div=pd.read_csv("SP500/clean_data/Year/div.csv",).drop(columns=drop_lst)
#div=div.drop('%5EGSPC', axis=1)



#%% Reforming Data

df1 = df1.rename(columns={'Unnamed: 0': 'Date'})
df1.set_index('Date', inplace=True)

dfe = dfe.rename(columns={'Unnamed: 0': 'Date'})
dfe.set_index('Date', inplace=True)

dfs = dfs.rename(columns={'Unnamed: 0': 'Date'})
dfs.set_index('Date', inplace=True)

dfg = dfg.rename(columns={'Unnamed: 0': 'Date'})
dfg.set_index('Date', inplace=True)

dfesg = dfesg.rename(columns={'Unnamed: 0': 'Date'})
dfesg.set_index('Date', inplace=True)

df.set_index('Date', inplace=True)
ROA.set_index('Date', inplace=True)
PB.set_index('Date', inplace=True)
#PE.set_index('Date', inplace=True)
Trades.set_index('Date', inplace=True)
MC.set_index('Date', inplace=True)
OM.set_index('Date', inplace=True)
#div.set_index('Date', inplace=True)

for col in PB.columns:
    if PB[col].isnull().all():

        print(col)


if forward_time == 0:
    esg_original = dfesg.to_numpy()[-back_time:][-1]
    quantile_const = np.quantile(esg_original, esg_quantile)
    
    esg_now = esg_original[esg_original>=quantile_const]
    e_now = dfe.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    s_now = dfs.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    g_now = dfg.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    
    r_return=np.log(PB.to_numpy())[-back_time:]
    r_return=r_return[:,esg_original>=quantile_const]

    
    #r_return = df.loc[:, df.columns != '%5EGSPC'].to_numpy()[-back_time:]
    #r_return = r_return[:,esg_original>=quantile_const]
    
    r_market = df1['%5EGSPC'].to_numpy()[-back_time:] #SP500 (weird yahoo name)
    #r_mktrf = df_farma_french['Mkt-RF'].to_numpy()[-back_time:]
    #r_smb = df_farma_french['SMB'].to_numpy()[-back_time:]
    #r_hml = df_farma_french['HML'].to_numpy()[-back_time:]
    
    r_market = np.tile(r_market.reshape(-1,1), r_return.shape[-1])
    #r_mktrf = np.tile(r_mktrf.reshape(-1,1), r_return.shape[-1])
    #r_smb = np.tile(r_smb.reshape(-1,1), r_return.shape[-1])
    #r_hml = np.tile(r_hml.reshape(-1,1), r_return.shape[-1])
    
    const_fac = np.ones_like(r_market)
    #indsæt faktorer til hver model.
    factor = [const_fac,
              r_market, 
              #dfe.to_numpy()[-back_time:][:,esg_original>=quantile_const], 
              #dfs.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #dfg.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #dfesg.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #ROA.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #PB.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #dfe.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #r_mktrf,
              #r_smb,
              #r_hml,
              np.log(MC.to_numpy())[-back_time:][:,esg_original>=quantile_const],
              ]
        
    factor = np.stack(factor)
else:
    esg_original = dfesg.to_numpy()[-(back_time+forward_time):-forward_time][-1]
    quantile_const = np.quantile(esg_original, esg_quantile)
    
    esg_now = esg_original[esg_original>=quantile_const]
    e_now = dfe.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    s_now = dfs.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    g_now = dfg.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    
    r_return=df.to_numpy()[-back_time:]
    r_return=r_return[:,esg_original>=quantile_const]

    
    #r_return = df.loc[:, df.columns != '%5EGSPC'].to_numpy()[-back_time:]
    #r_return = r_return[:,esg_original>=quantile_const]
    
    r_market = df1['%5EGSPC'].to_numpy()[-(back_time+forward_time):-forward_time] #SP500 (weird yahoo name)
    r_mktrf = df_farma_french['Mkt-RF'].to_numpy()[-(back_time+forward_time):-forward_time]
    r_smb = df_farma_french['SMB'].to_numpy()[-(back_time+forward_time):-forward_time]
    r_hml = df_farma_french['HML'].to_numpy()[-(back_time+forward_time):-forward_time]
    
    
    r_rmw = df5['RMW'].to_numpy()[-(back_time+forward_time):-forward_time]
    r_cma = df5['CMA'].to_numpy()[-(back_time+forward_time):-forward_time]
    
    r_market = np.tile(r_market.reshape(-1,1), r_return.shape[-1])
    r_mktrf = np.tile(r_mktrf.reshape(-1,1), r_return.shape[-1])
    r_smb = np.tile(r_smb.reshape(-1,1), r_return.shape[-1])
    r_hml = np.tile(r_hml.reshape(-1,1), r_return.shape[-1])
    
    r_rmw = np.tile(r_rmw.reshape(-1,1), r_return.shape[-1])
    r_cma = np.tile(r_cma.reshape(-1,1), r_return.shape[-1])
    
    const_fac = np.ones_like(r_market)
    #indsæt faktorer til hver model.
    factor = [const_fac,
              r_market, 
             #dfe.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const], 
             #dfs.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
             dfg.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
             #dfesg.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
              #r_mktrf,
              r_smb,
              r_hml,
              r_rmw,
             r_cma,
       #np.log(PB.to_numpy())[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
      # np.log(MC.to_numpy())[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
       #ROA.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
       #Trades.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const]
              ]
        
    factor = np.stack(factor)

#%% Run FAMA-MacBeth and OLS

fac_cls =  factmod(r_return, factor, model_type = "Pooled")
dummy,ER= fac_cls.ols()
print('\n\n Forventet afskast: ',ER*100, '\n\n')





#dummy = fac_cls.famamb()
EER=2.17605654-2.14635574
sER=2.21699463-2.07163337
gER=2.20276485-2.0562156
ESGER=2.20851523-2.12182369

EFM=1.9931736-1.97331629
SFM=2.00907502-1.90549994
GFM=2.01048422-1.8937335
ESGFM=2.0135525-1.95035001