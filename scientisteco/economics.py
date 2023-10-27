# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import optimize as opt
from sklearn.base import BaseEstimator, TransformerMixin
import matplotlib.pyplot as plt

##########################################################################################################
# Consumption Analysis
##########################################################################################################

class CONSUMPTION(BaseEstimator,TransformerMixin):
    """
    Consumption analysis

    This function performs consumption analysis used in case of microeconomics analysis.

    Parameters:
    -----------
    u :
    R :
    p1 :
    p2 :
    new_p1 :
    new_p2 :
    new_R :

    Returns:
    -------
    
    
    
    """
    def __init__(self,u=None,R=None,p1=None,p2=None,new_p1=None,new_p2=None,new_R=None):
        self.u = u
        self.R = R
        self.p1 = p1
        self.p2 = p2
        self.new_R = new_R
        self.new_p1 = new_p1
        self.new_p2 = new_p2
    
    def fit(self):
        """
        
        
        """

        # Constraint : R - x*p1 - y*p2
        const = {'type': 'eq',
                 'fun' : lambda x: np.array([x[0]*self.p1 + x[1]*self.p2 - self.R]),
                 'jac' : lambda x: np.array([self.p1,self.p2])}
        
        # Function to minimize v = -u
        def v(x):
            x, y = x[0], x[0]
            return -self.u(x,y)
        
        print(v([2,2]))

        # Optimization
        res = opt.minimize(v,x0=np.array([0,0]),constraints=const)

        self.res_ = res

        self.model_ = "consumption"
        
        return self
    
    def transform(self,X,new="first"):
        """
        
        
        """
        if not isinstance(X,float):
            raise ValueError("Error : 'X' must be float.")
        
        if new=="first":
            new_const = {'type': 'eq',
                         'fun' : lambda x: np.array([x[0]*X + x[1]*self.p2 - self.R]),
                         'jac' : lambda x: np.array([X,self.p2])}
        elif new == "second":
            new_const = {'type': 'eq',
                         'fun' : lambda x: np.array([x[0]*self.p1 + x[1]*X - self.R]),
                         'jac' : lambda x: np.array([self.p1,X])}
        else:
            new_const = {'type': 'eq',
                         'fun' : lambda x: np.array([x[0]*self.p1 + x[1]*self.p2 - X]),
                         'jac' : lambda x: np.array([self.p1,self.p2])}
        
        # New problem using new constraint
        # Function to minimize v = -u
        def v(x):
            x, y = x[0], x[0]
            return -self.u(x,y)

        # Optimization
        res = opt.minimize(v,x0=np.array([0,0]),constraints=new_const)
    
    def plot(self,
             color="black",
             xlabel="Good 1",
             ylabel="Good 2", 
             title="Flexible demand systems",
             addgrid=True,ax=None):
        if ax is None:
            ax = plt.gca()
        
        # Bound
        bound1, bound2 = self.R/self.p1, self.R/self.p2
        ax.plot([bound1,0],[0,bound2],color=color)
        ax.axhline(y=0,color="black",linestyle="-")
        ax.axvline(x=0,color="black",linestyle="-")
        ax.grid(visible=addgrid)
        ax.set(xlabel=xlabel,ylabel=ylabel,title=title)


#####################################################################################################
#   Production Analysis
######################################################################################################

class PRODUCTION(BaseEstimator,TransformerMixin):
    def __init__(self,f=None,C=None,p1=None,p2=None):
        pass
