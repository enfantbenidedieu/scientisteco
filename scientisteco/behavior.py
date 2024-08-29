# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import optimize as optim
from sklearn.base import BaseEstimator, TransformerMixin

##########################################################################################################
# Consumption Analysis
##########################################################################################################
# https://data88e.org/textbook/content/00-intro/index.html
# https://search.r-project.org/CRAN/refmans/Recon/html/cournot_solver.html
# https://janboone.github.io/competition_policy_and_regulation/Collusion_Cournot/Collusion_Cournot.html
# https://search.r-project.org/CRAN/refmans/Recon/html/cobb_douglas.html
# https://www.worldscientific.com/doi/pdf/10.1142/9789811256189_0001
# https://rpubs.com/dtkaplan/543
# https://rdrr.io/cran/micEcon/
# https://www.r-bloggers.com/2014/11/interactive-cobb-douglas-web-app-with-r/
# https://datascience.quantecon.org/python_fundamentals/functions.html
# https://ccamilocristian.github.io/posts/optimation-consumer-english/
# https://numeconcopenhagen.netlify.app/lectures/Optimize_print_and_plot
# https://deepnote.com/@gaby-galvan/Edgeworth-Box-5c892517-cb51-4f3f-b20d-8e5dd8b5ac46
# https://www.oreilly.com/library/view/financial-theory-with/9781098104344/ch04.html
# https://macroeconomics.github.io/tag/notebooks.html
# https://python.quantecon.org/cass_koopmans_2.html
# https://ie.pubpub.org/pub/python-packages-for-economics/release/2

class CONSUMPTION(BaseEstimator,TransformerMixin):
    """
    Consumption analysis
    --------------------
    This class inherits from sklearn BaseEstimator and TransformerMixin class

    Description
    -----------
    This function performs consumption analysis used in case of microeconomics analysis.

    Usage
    -----
    ```
    >>> 
    ```

    Parameters
    -----------
    u :

    R :
    p1 :
    p2 :
    new_p1 :
    new_p2 :
    new_R :

    Attributes
    ----------
    
    
    
    """
    def __init__(self,
                 alpha=None,
                 beta=None,
                 R=None,
                 p1=None,
                 p2=None,
                 new_p1=None,
                 new_p2=None,
                 new_R=None):
        self.alpha = alpha
        self.beta = beta
        self.R = R
        self.p1 = p1
        self.p2 = p2
        self.new_R = new_R
        self.new_p1 = new_p1
        self.new_p2 = new_p2
    
    def fit(self):
        """
        
        
        """

        # Init
        self.new_optimo_ = None

        # Function to minimize v = -u
        def objectif(X):
            x, y = X
            alpha = self.alpha
            beta = self.beta
            return -(x**(alpha)*y**(beta))

        # Constraint : x*p1 + y*p2 - R
        const = {'type': 'eq','fun' : lambda x : -self.R+x[0]*self.p1+x[1]*self.p2}
        
        # Bounds
        bnds = (((0,None)),(0,None))

        # Optimization
        opt = optim.minimize(objectif,x0=(0,0),method="SLSQP",constraints=const,bounds=bnds)

        # Add attributes
        self.objective_ = objectif
        self.optimo_ = {"x1" : opt.x[0], "y1" : opt.x[1], "u1" : -opt.fun}

        # Add modification
        if self.new_p1 is not None:
            self.new_optimo_ = self.transform(X=self.new_p1,new="first-price")
        elif self.new_p2 is not None:
            self.new_optimo_ = self.transform(X=self.new_p2,new="second-price")
        elif self.new_R is not None:
            self.new_optimo_ = self.transform(X=self.new_R,new="income")

        # Model Name
        self.model_ = "consumption"
        
        return self
    
    def transform(self,X,new="first"):
        """
        
        
        """
        if not isinstance(X,float):
            raise ValueError("Error : 'X' must be float.")
        
        if new=="first-price":
            # New constraint
            new_const = {'type': 'eq', 'fun' : lambda x: x[0]*X + x[1]*self.p2 - self.R}
            # Intermediate Income
            R_bis = X*self.optimo_["x1"] + self.p2*self.optimo_["y1"] 
            # Intermediate constraint
            inter_const = {'type': 'eq', 'fun' : lambda x: x[0]*X + x[1]*self.p2 - R_bis}         
        elif new == "second-price":
            # New constraint
            new_const = {'type': 'eq', 'fun' : lambda x: x[0]*self.p1 + x[1]*X - self.R}
            # Intermediate Income
            R_bis = self.optimo_['x1']*self.p1 + self.optimo_['y1']*X
            # Intermediate constraint
            inter_const = {'type': 'eq', 'fun' : lambda x : x[0]*self.p1 + x[1]*X - R_bis}
        elif new == "income":
            new_const = {'type': 'eq', 'fun' : lambda x: x[0]*self.p1 + x[1]*self.p2 - X}
        else:
            raise ValueError("Error : ")
        
        # Bounds
        bnds = ((0,None),(0,None))
        # New optimisation problem
        opt = optim.minimize(self.objective_,x0=(0,0),method="SLSQP",constraints=new_const,bounds=bnds)

        # Store optimal Result
        res = {"x2" : opt.x[0], "y2" : opt.x[1], "u2" : -opt.fun}

        # Effet de Substitution - Effet Revenu
        if new in ["first-price","second-price"]:
            inter_opt =  optim.minimize(self.objective_,x0=(0,0),method="SLSQP",constraints=inter_const,bounds=bnds)
            # Extract result
            inter_res = {"x3" : inter_opt.x[0],"y3" : inter_opt.x[1],"u3" : -inter_opt.fun, "R3" : R_bis}
            res.update(inter_res)
        
        return res


#####################################################################################################
#   Production Analysis
######################################################################################################

class PRODUCTION(BaseEstimator,TransformerMixin):
    """Production Analysis
    
    
    """
    def __init__(self,
                 alpha=None,
                 beta=None,
                 A = None,
                 pk = None,
                 pl = None,
                 C = None,
                 new_pk = None,
                 new_pl = None,
                 new_C = None):
        self.alpha = alpha
        self.beta = beta
        self.A = A
        self.pk = pk
        self.pl = pl
        self.C = C
        self.new_pk = new_pk
        self.new_pl = new_pl
        self.new_C = new_C
    
    def fit(self):
        """
        
        
        """

        self.new_optim_ = None

        # Progres technique
        if self.A is None:
            self.A = 1

        # Function to minimize v = -u
        def objectif(X):
            x, y = X
            alpha = self.alpha
            beta = self.beta
            return -self.A*(x**(alpha)*y**(beta))
        
        # Constraint : x*p1 + y*p2 - R
        const = {'type': 'eq','fun' : lambda x : -self.C+x[0]*self.pk+x[1]*self.pl}
        
        # Bounds
        bnds = (((0,None)),(0,None))

        # Optimization
        opt = optim.minimize(objectif,x0=(0,0),method="SLSQP",constraints=const,bounds=bnds)

        # Add attributes
        self.objective_ = objectif
        self.optimo_ = {"k1" : opt.x[0], "l1" : opt.x[1], "y" : -opt.fun}

        # Model Name
        self.model_ = "production"
        
        return self



class GENERALEQUILIBRIUM(BaseEstimator,TransformerMixin):


    def __init__(self):
        pass






