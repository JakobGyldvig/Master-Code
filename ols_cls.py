
"""
Created on Fri Nov 18 22:17:25 2022

@author: Jakob Gyldvig
"""

#%% Sources

#https://scipy-lectures.org/packages/statistics/auto_examples/plot_regression.html
#https://stackoverflow.com/questions/58957716/how-to-run-a-pooled-ols-regression-on-python
#https://en.wikipedia.org/wiki/Fama–MacBeth_regression
#https://stackoverflow.com/questions/24074481/fama-macbeth-regression-in-python-pandas-or-statsmodels
#https://www.kevinsheppard.com/teaching/python/notes/notebooks/example-fama-macbeth/


#%% Modules

import numpy as np
import statsmodels.api as sm

#%% Code

class factmod(object):
   
    def __init__(self, y, X, model_type = "OLS"):
       
        self.nfac = X.shape[0]
        if model_type == "OLS":
            self.X = X
            self.y = y
        else:
            self.y = y.reshape(-1)
            self.X = X.reshape(self.nfac,-1).T
            
        self.N = self.y.shape[0]
        
        return
   
    def ols(self, print_result = True):
       
        model = sm.OLS(self.y, self.X).fit()
       
        if print_result:
            print(model.summary())
       
        return model.params,model.predict(self.X[-1])
   
    def famamb(self, print_result = True):
       
        # Time series regressions
        ts_res = sm.OLS(self.y, self.X).fit()
        beta = ts_res.params[1:]
        #avgExcessReturns = np.mean(self.y, 0)
        # Cross-section regression
       
       
        if beta.ndim == 1:
            n_const = 1
        else:
            n_const = beta.shape[0]
       
        const = np.ones(n_const)
        beta = np.hstack((const, beta))
       
        beta = np.tile(beta.reshape(-1,1), self.N).T
       
        #cs_res = sm.OLS(avgExcessReturns, beta).fit()
        cs_res = sm.OLS(self.y, beta).fit()
       
        if print_result:
            print(cs_res.summary())
       
        return cs_res.params
 
#y = np.linspace(-1,1,100)
#x1 = y
#x2 = y**2
#x0 = np.ones_like(y)
#X = np.vstack((x0, x1, x2)).T

#fc_cls = factmod(y, X, "Pooled")
#fc_cls.ols()
#fc_cls.famamb()