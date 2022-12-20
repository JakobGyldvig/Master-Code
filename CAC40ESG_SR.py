# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 01:57:40 2022

@author: jakob
"""


#%% Modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Own modules
import portfolio_optimization as po

#%% Functions

#ESG Function
def f_fun_esg(s):
    
    return s

#Markowitz Function
def f_fun_markowitz(s):
    
    return 0 #0

#%% Hyper-parameters

back_time = 60
forward_time = 1
rf = 0.000152

gamma_min = 0.1
gamma_max = 10
n_gamma = 10

n_esg = 15
esg_quantile = 0.0

#%% Load Data
df1= pd.read_csv("SP500/clean_data/adj_data.csv")
df = pd.read_csv("SP500/clean_data/Year/adj_data.csv")
dfe = pd.read_csv("SP500/clean_data/e_clean.csv")
dfs = pd.read_csv("SP500/clean_data/s_clean.csv")
dfg = pd.read_csv("SP500/clean_data/g_clean.csv")
dfesg= pd.read_csv("SP500/clean_data/esg_clean.csv")


#df = pd.read_csv("CAC40/clean_data/adj_data.csv")
#dfe = pd.read_csv("CAC40/clean_data/e_clean.csv")
#dfs = pd.read_csv("CAC40/clean_data/s_clean.csv")
#dfg = pd.read_csv("CAC40/clean_data/g_clean.csv")
#dfesg= pd.read_csv("CAC40/clean_data/esg_clean.csv")
#market= pd.read_csv("CAC40/clean_data/market.csv")
#df_farma_french = pd.read_csv("SP500/clean_data/farma_french.csv")
#ROA=pd.read_csv("SP500/clean_data/ROA.csv")
#PB=pd.read_csv("SP500/clean_data/PB.csv")
#PE=pd.read_csv("SP500/clean_data/PE.csv")
#Trades=pd.read_csv("SP500/clean_data/Trades.csv")

#%% Reforming Data

#df1 = df1.rename(columns={'Unnamed: 0': 'Date'})
#df1.set_index('Date', inplace=True)

df = df.rename(columns={'Unnamed: 0': 'Date'})
df.set_index('Date', inplace=True)

dfe = dfe.rename(columns={'Unnamed: 0': 'Date'})
dfe.set_index('Date', inplace=True)

dfs = dfs.rename(columns={'Unnamed: 0': 'Date'})
dfs.set_index('Date', inplace=True)

dfg = dfg.rename(columns={'Unnamed: 0': 'Date'})
dfg.set_index('Date', inplace=True)

dfesg = dfesg.rename(columns={'Unnamed: 0': 'Date'})
dfesg.set_index('Date', inplace=True)

#market = market.rename(columns={'Unnamed: 0': 'Date'})
#market.set_index('Date', inplace=True)

#ROA=ROA.set_index('Date', inplace=True)
#PB=PB.set_index('Date', inplace=True)
#PE=PE.set_index('Date', inplace=True)
#Trades=Trades.set_index('Date', inplace=True)


if forward_time == 0:
    esg_original = dfesg.to_numpy()[-back_time:][-1]
    quantile_const = np.quantile(esg_original, esg_quantile)
    
    esg_now = esg_original[esg_original>=quantile_const]
    e_now = dfe.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    s_now = dfs.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    g_now = dfg.to_numpy()[-back_time:][-1][esg_original>=quantile_const]
    
    r_return = df.loc[:, df.columns != '%5EGSPC'].to_numpy()[-back_time:]
    r_return = r_return[:,esg_original>=quantile_const]
    
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
             dfg.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #dfesg.to_numpy()[-back_time:][:,esg_original>=quantile_const],
              #r_mktrf,
              #r_smb,
              #r_hml
              ]
        
    factor = np.stack(factor).transpose(2,1,0)
else:
    esg_original = dfesg.to_numpy()[-(back_time+forward_time):-forward_time][-1]
    quantile_const = np.quantile(esg_original, esg_quantile)
    
    esg_now = esg_original[esg_original>=quantile_const]
    e_now = dfe.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    s_now = dfs.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    g_now = dfg.to_numpy()[-(back_time+forward_time):-forward_time][-1][esg_original>=quantile_const]
    
    r_return = df.loc[:, df.columns != '%5EGSPC'].to_numpy()[-back_time:]
    r_return = r_return[:,esg_original>=quantile_const]
    
    r_market = df1['%5EGSPC'].to_numpy()[-(back_time+forward_time):-forward_time]
    #r_market = market.to_numpy()[-(back_time+forward_time):-forward_time] #SP500 (weird yahoo name)
   # r_mktrf = df_farma_french['Mkt-RF'].to_numpy()[-(back_time+forward_time):-forward_time]
    #r_smb = df_farma_french['SMB'].to_numpy()[-(back_time+forward_time):-forward_time]
    #r_hml = df_farma_french['HML'].to_numpy()[-(back_time+forward_time):-forward_time]
    
    r_market = np.tile(r_market.reshape(-1,1), r_return.shape[-1])
    #r_mktrf = np.tile(r_mktrf.reshape(-1,1), r_return.shape[-1])
    #r_smb = np.tile(r_smb.reshape(-1,1), r_return.shape[-1])
    #r_hml = np.tile(r_hml.reshape(-1,1), r_return.shape[-1])
    
    const_fac = np.ones_like(r_market)
    #indsæt faktorer til hver model.
    factor = [const_fac,
              r_market, 
              #dfe.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const], 
              #dfs.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
           dfg.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
              #dfesg.to_numpy()[-(back_time+forward_time):-forward_time][:,esg_original>=quantile_const],
              #r_mktrf,
              #r_smb,
              #r_hml
              ]
        
    factor = np.stack(factor).transpose(2,1,0)

#%% Constraints

esg_bar =0.0 #min: 29.2325, max: 82.0139
e_bar = 0.0 #min: 0.0, max: 84.4156
s_bar = 0.0 #min: 0.0, max: 71.8561
g_bar = 85 #min: 68.1818, max: 100.0

const_mostly_long = {'type': 'ineq', 'fun': lambda x: np.sum(x)}
const_equal_weights = {'type':'eq', 'fun': lambda x: np.sum(x)-1.0}
const_less_weights = {'type':'ineq', 'fun': lambda x: 1.0-np.sum(x)}
const_esg = {'type':'ineq', 'fun': lambda x: x.dot(esg_now)-esg_bar}
const_e = {'type':'ineq', 'fun': lambda x: x.dot(e_now)-e_bar}
const_s = {'type':'ineq', 'fun': lambda x: x.dot(s_now)-s_bar}
const_g = {'type':'ineq', 'fun': lambda x: x.dot(g_now)-g_bar}

#%% Markowitz Optimization klassisk mark for unaware og Aware afhænger af måde de regner forventet afkast.

const = const_less_weights

gamma = np.linspace(gamma_min, gamma_max, n_gamma)

lst_x = []
lst_mu_x = []
lst_var_x = []
lst_sr_x = []

i = 1
print("\n \t\t Running Efficient Frontier for Markowitz Optimization \n")
for gam in gamma:
    print("Iteration number: \t", i, "/", n_gamma)
    x, mu_x, var_x, sr_x = po.markowitz_optimization(r_return, factor, risk_free = rf, f_fun = None, gamma=gam,
                                                     const = const)
    
    lst_x.append(x)
    lst_mu_x.append(mu_x)
    lst_var_x.append(var_x)
    lst_sr_x.append(sr_x)
    i += 1
    
x = np.stack(lst_x)
mu_x = np.stack(lst_mu_x)
fisse=np.mean(mu_x)
var_x = np.stack(lst_var_x)
sr_x = np.stack(lst_sr_x)
Snow=x.dot(s_now)


    
plt.figure(figsize=(8,6))
plt.scatter(np.sqrt(var_x), mu_x, c=sr_x, cmap="viridis")
plt.colorbar(label="Sharp Ratio")
plt.xlabel("Standard deviation of rate of return")
plt.ylabel("Expected Return")
plt.show()

#%% Markowitz Sharp Ratio Opimization

esg = np.linspace(np.min(esg_now), np.max(esg_now), n_esg)

lst_x = []
lst_mu_x = []
lst_var_x = []
lst_sr_x = []

i = 1
print("\n \t\t Running Sharp Ratio for Markowitz Optimization \n")
for s in esg:
    print("Iteration number: \t", i, "/", n_esg)
    x, mu_x, var_x, sr_x = po.sr_optimization(r_return, factor, esg_now, s, risk_free = rf, 
                                              f_fun = None, gamma=0.0)
    
    lst_x.append(x)
    lst_mu_x.append(mu_x)
    lst_var_x.append(var_x)
    lst_sr_x.append(sr_x)
    
    i += 1
    
x = np.stack(lst_x)
mu_x = np.stack(lst_mu_x)
var_x = np.stack(lst_var_x)

xa=x
sr_2 = np.stack(lst_sr_x)
Gnu=x.dot(g_now)
Snow=x.dot(s_now)
enu=x.dot(esg_now)

xu=x
sr_x = np.stack(lst_sr_x)
sr_u=sr_x
Gnow=x.dot(g_now)
Enow=x.dot(esg_now)

x25=x
E25=x.dot(esg_now)
sr_25=np.stack(lst_sr_x)

    
plt.figure(figsize=(8,6))
plt.plot(enu,sr_2,label='Type-A', linestyle=':', marker='.')
plt.plot(Enow, sr_u, label='Type-U', linestyle=':', marker='.')
#plt.plot(E25, sr_25, label='Type-A: 25 % screen', linestyle=':', marker='.')
plt.xlabel('Portfolio G-Score.')
plt.ylabel("Sharpe ratio")
plt.xlim()
plt.legend()
plt.show()

#%% ESG Optimization

const = const_equal_weights

gamma = np.linspace(gamma_min, gamma_max, n_gamma)

lst_x = []
lst_mu_x = []
lst_var_x = []
lst_sr_x = []

i = 1
print("\n \t\t Running Efficient Frontier for ESG Optimization \n")
for gam in gamma:
    print("Iteration number: \t", i, "/", n_gamma)
    x, mu_x, var_x, sr_x = po.markowitz_optimization(r_return, factor, risk_free = rf, f_fun = f_fun_esg, gamma=gam,
                                                     esg_score = esg_now, const = const)
    
    lst_x.append(x)
    lst_mu_x.append(mu_x)
    lst_var_x.append(var_x)
    lst_sr_x.append(sr_x)
    i += 1
    
x = np.stack(lst_x)
mu_x = np.stack(lst_mu_x)
var_x = np.stack(lst_var_x)
sr_x = np.stack(lst_sr_x)
    
plt.figure(figsize=(8,6))
plt.scatter(np.sqrt(var_x), mu_x, c=sr_x, cmap="viridis")
plt.colorbar(label="Sharp Ratio")

#%% ESG Sharp Ratio Opimization

esg = np.linspace(np.min(esg_now), np.max(esg_now), n_esg)

lst_x = []
lst_mu_x = []
lst_var_x = []
lst_sr_x = []

i = 1
print("\n \t\t Running Sharp Ratio for ESG Optimization \n")
for s in esg:
    print("Iteration number: \t", i, "/", n_esg)
    x, mu_x, var_x, sr_x = po.sr_optimization(r_return, factor, esg_now, s, risk_free = rf, 
                                              f_fun = f_fun_esg, gamma=1.0)
    
    lst_x.append(x)
    lst_mu_x.append(mu_x)
    lst_var_x.append(var_x)
    lst_sr_x.append(sr_x)
    
    i += 1
    
x = np.stack(lst_x)
mu_x = np.stack(lst_mu_x)
var_x = np.stack(lst_var_x)
sr_x = np.stack(lst_sr_x)
    
plt.figure(figsize=(8,6))
plt.scatter(esg, sr_x,)
#plt.title("")
plt.xlabel("ESG-Score")
plt.ylabel("Sharpe ratio")
plt.show()



#%% ESG Optimization - With Extra Constrains and no f function

const = [const_equal_weights, const_esg, const_e, const_s, const_g]

gamma = np.linspace(gamma_min, gamma_max, n_gamma)

lst_x = []
lst_mu_x = []
lst_var_x = []
lst_sr_x = []

i = 1
print("\n \t\t Running Efficient Frontier for ESG Optimization with constraints \n")
for gam in gamma:
    print("Iteration number: \t", i, "/", n_gamma)
    x, mu_x, var_x, sr_x = po.markowitz_optimization(r_return, factor, risk_free = rf, f_fun = None, gamma=gam,
                                                     const = const)
    
    lst_x.append(x)
    lst_mu_x.append(mu_x)
    lst_var_x.append(var_x)
    lst_sr_x.append(sr_x)
    i += 1
    
x = np.stack(lst_x)
mu_x = np.stack(lst_mu_x)
var_x = np.stack(lst_var_x)
sr_x = np.stack(lst_sr_x)
    
plt.figure(figsize=(8,6))
plt.scatter(np.sqrt(var_x), mu_x, c=sr_x, cmap="viridis")
plt.colorbar(label="Sharp Ratio")

x.dot(g_now).max()
