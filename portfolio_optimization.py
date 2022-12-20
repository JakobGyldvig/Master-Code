# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 14:24:10 2022

@author: jakob
"""

#%% Modules

import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm

#%% Constants

TOL_VAL = 10e-5

#%% Functions

def factor_model(r_assets, r_signals, risk_free=0.0):
    
    er = []
    N_stocks = r_assets.shape[-1]
    for i in range(N_stocks):
        model = sm.OLS(r_assets[:,i], r_signals[i]).fit()
        er.append(model.predict(r_signals[i,-1]))
    er = np.stack(er).reshape(-1)
    
    return er-risk_free

def markowitz_optimization(r_assets, r_signals, risk_free = 0.0, f_fun = None, 
                           gamma = 1.0, esg_score = None, const = []):
    
    def sigma_fun(x):
        
        return x.dot(Sigma).dot(x)
    
    def mu_fun(x):
        
        return mu.dot(x)
    
    def sharp_ratio(x):
        
        return mu_fun(x)/np.sqrt(sigma_fun(x))
    
    def markowitz_lagrange_objective(x):
        
        return 0.5*gamma*sigma_fun(x)-mu_fun(x)-f_fun(x.dot(esg_score)/np.sum(x))-(1-np.sum(x))*risk_free
    
    N = r_assets.shape[-1]
    
    if f_fun is None:
        f_fun = lambda x: 0
        esg_score = np.zeros(N)

    Sigma = np.cov(r_assets.T, bias=True)
    mu = factor_model(r_assets, r_signals, risk_free)
    x_init = np.ones(N)
    
    single_bnds = (0.0, 1.0)
    bnds = [single_bnds]*N
    
    sol = minimize(markowitz_lagrange_objective, x_init,  method="SLSQP",
                   constraints=const, bounds=bnds, tol=TOL_VAL)
    x = sol.x
    
    mu_x = mu_fun(x)
    var_x = sigma_fun(x)
    sr_x = sharp_ratio(x)
    
    return x, mu_x, var_x, sr_x

def sr_optimization(r_assets, r_signals, esg_score, esg_bar, risk_free = 0.0, f_fun = None, 
                           gamma = 0.0, const=[]):
    
    def sigma_fun(x):
        
        return x.dot(Sigma).dot(x)
    
    def mu_fun(x):
        
        return mu.dot(x)
    
    def sharp_ratio(x):
        
        return mu_fun(x)/np.sqrt(sigma_fun(x))
    
    def sr_objective(x):
        
        return -2*gamma*f_fun(x.dot(esg_score))-sharp_ratio(x)**2
    
    N = r_assets.shape[-1]
    
    if f_fun is None:
        f_fun = lambda x: 0
        gamma = 0.0

    Sigma = np.cov(r_assets.T, bias=True)
    mu = factor_model(r_assets, r_signals, risk_free)
    x_init = np.ones(N)
    
    single_bnds = (0.0, 1.0)
    bnds = [single_bnds]*N
    
    const = const[:]
    const.append({'type':'eq', 'fun': lambda x: x.dot(esg_score)-esg_bar})
    const.append({'type':'eq', 'fun': lambda x: np.sum(x)-1.0})
    sol = minimize(sr_objective, x_init,  method="SLSQP",
                   constraints=const, bounds=bnds, tol=TOL_VAL)
    
    x = sol.x
    
    mu_x = mu_fun(x)
    var_x = sigma_fun(x)
    sr_x = sharp_ratio(x)
    
    return x, mu_x, var_x, sr_x
    