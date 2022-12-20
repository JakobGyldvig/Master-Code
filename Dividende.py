# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 11:06:58 2022

@author: jakob
"""


import yfinance as yf
import datetime
import pandas as pd
import numpy as np





liste = pd.read_csv("SP500/clean_data/adj_data.csv")
ticker=liste.drop('Unnamed: 0', axis=1)
ticker= liste.columns.values.tolist()

stocks = ['AAPL', 'MSFT', 'AMD']
div= []
newstock=[]
wrong=[]
i=1
N=len(ticker)

for stock in ticker:
    try:
        div.append(yf.Ticker(stock).history(start='2011-01-01', end='2021-12-31')['Dividends'])
        newstock.append(stock)
    except:
        wrong.append(stock)
    print('iteration: \t', i,'/',N)
    i+=1
        
   
   
div =pd.concat(div,axis=1)
div.columns=newstock

div1=div

div1.index = pd.to_datetime(div1.index)
div1=div1.resample('3M').sum()

div1.to_csv('SP500/clean_data/div.csv', index=True)

#%%Gruppering af de 50 bedste aktier til hver periode SP500
import matplotlib.pyplot as plt
esg_quantile = 0.9


afkast = pd.read_csv("SP500/clean_data/Year/adj_data.csv")
afkast.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
afkast=afkast.tail(21)


liste = pd.read_csv("SP500/clean_data/g_clean.csv")
liste.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

liste=liste.tail(21)



n,N = liste.shape
return_lst = []
for i in range(n):
    esg_original = liste.iloc[i].values[1:]
    return_row = afkast.iloc[i].values[1:]
    quantile_const = np.quantile(esg_original, 1-esg_quantile)
    return_high = return_row[esg_original<=quantile_const]
    return_lst.append(np.mean(return_high))
   # print(esg_original[esg_original>=quantile_const])
    
return_lst1 = np.stack(return_lst) 


n,N = liste.shape
return_lst = []
for i in range(n):
    esg_original = liste.iloc[i].values[1:]
    return_row = afkast.iloc[i].values[1:]
    quantile_const = np.quantile(esg_original, esg_quantile)
    return_high = return_row[esg_original>=quantile_const]
    return_lst.append(np.mean(return_high))
   # print(esg_original[esg_original>=quantile_const])
    

return_lst = np.stack(return_lst)

#dif1=return_lst-return_lst1

plt.figure(figsize=(8,6))
#plt.plot(np.cumprod(return_lst+1)-1), label='dif')
plt.plot(np.cumprod(return_lst+1)-1, label='10% highest E score')
plt.plot(np.cumprod(return_lst1+1)-1,label='10% lowestest E score')
plt.xlabel('Months form 2017-01-31')
plt.ylabel('Total return since 2017-01-31 ')
plt.legend()
plt.show()

#%%
import matplotlib.pyplot as plt
esg_quantile = 0.0


afkast = pd.read_csv("CAC40/clean_data/adj_data.csv")
afkast.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
afkast=afkast.tail(100)
afkast.set_index('Date', inplace=True)


liste = pd.read_csv("CAC40/clean_data/s_clean.csv")
liste.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
liste.set_index('Date', inplace=True)

liste=liste.tail(100)



n,N = liste.shape
return_lst = []
for i in range(n):
    esg_original = liste.iloc[i].values[1:]
    return_row = afkast.iloc[i].values[1:]
    quantile_const = np.quantile(esg_original, 1-esg_quantile)
    return_high = return_row[esg_original<=quantile_const]
    return_lst.append(np.mean(return_high))
   # print(esg_original[esg_original>=quantile_const])
    
return_lst1 = np.stack(return_lst) 


n,N = liste.shape
return_lst = []
for i in range(n):
    esg_original = liste.iloc[i].values[1:]
    return_row = afkast.iloc[i].values[1:]
    quantile_const = np.quantile(esg_original, esg_quantile)
    return_high = return_row[esg_original>=quantile_const]
    return_lst.append(np.mean(return_high))
   # print(esg_original[esg_original>=quantile_const])
    

return_lst = np.stack(return_lst)

#dif1=return_lst-return_lst1

plt.figure(figsize=(8,6))
#plt.plot(np.cumprod(return_lst+1)-1), label='dif')
plt.plot(np.cumprod(return_lst+1)-1, label='10% highest ESG score')
plt.plot(np.cumprod(return_lst1+1)-1,label='10% lowestest ESG score')
plt.xlabel('Months form 2017-01-31')
plt.ylabel('Total return since 2017-01-31 ')
plt.legend()
plt.show()


