
# -*- coding: utf-8 -*-

import numpy as np
from scipy import optimize as optim
from sklearn.base import BaseEstimator, TransformerMixin

# https://colab.research.google.com/github/QuantEcon/lecture-python-advanced.notebooks/blob/master/dyn_stack.ipynb
# https://courses.lumenlearning.com/suny-microeconomics/chapter/the-collusion-model/

class DUOPOLE(BaseEstimator,TransformerMixin):
    """
    DUOPOLY COMPETITION
    -------------------


    Description
    -----------



    Parameters
    ----------
    demand :
    cost1 :
    cost2 : 
    initial_state :
    method :
    """
    def __init__(self,
                 demand,
                 cost1,
                 cost2=None,
                 initial_state=None,
                 method="cournot",
                 leader=1):

        self.demand = demand
        self.cost1 = cost1
        self.cost2 = cost2
        self.initial_state = initial_state
        self.method = method
        self.leader = leader

    def fit(self):
        """
        
        
        
        """

        # Set cost2
        if self.cost2 is None:
            self.cost2 = self.cost1

        if self.method == "cournot":
            self._cournot()
        if self.method == "stackelberg":
            self._stackelberg()


        # Profit Firm 1
        opt_profit1 = self.demand(self.optimo_["x1"],self.optimo_["x2"])*self.optimo_["x1"] - self.cost1(self.optimo_["x1"])
        
        # Profit Firm 2
        opt_profit2 = self.demand(self.optimo_["x1"],self.optimo_["x2"])*self.optimo_["x2"] - self.cost2(self.optimo_["x2"])
        
        self.profit_ = {"profit1" : opt_profit1, "profit2" : opt_profit2}
        
        self.model_ = "duopole"

    def _cournot(self):
        """
        
        """

        # Profit of Firm 1
        def profit1(x1,x2):
            return self.demand(x1,x2)*x1 - self.cost1(x1)
        
        # Profit of Firm 2
        def profit2(x1,x2):
            return self.demand(x1,x2)*x2 - self.cost2(x2)
        
        # Reaction of Firm 1
        def reaction1(x2):
            x1 = optim.brute(lambda x: -profit1(x,x2),((0,1,),))                                             
            return x1[0]
        
        # Reaction of Firm 2
        def reaction2(x1):
            x2 = optim.brute(lambda x: -profit2(x1,x),((0,1,),))                                             
            return x2[0]

        # x* = f(x*) => x* - f(x*)
        def vector_reaction(x): 
            return np.array(x) - np.array([reaction1(x[1]),reaction2(x[0])])
        
        x0 = self.initial_state
        if x0 is None:
            x0 = [0,0]
        opt = optim.fsolve(vector_reaction, x0)

        # Optimum
        self.optimo_ = {"x1" : opt[0], "x2" : opt[1]}
    
    def _stackelberg(self):
        """
        
        
        """


        # Profit of Firm 1
        def profit1(x1,x2):
            return self.demand(x1,x2)*x1 - self.cost1(x1)
        
        # Profit of Firm 2
        def profit2(x1,x2):
            return self.demand(x1,x2)*x2 - self.cost2(x2)
        
        # Reaction of Firm 1
        def reaction1(x2):
            x1 = optim.brute(lambda x: -profit1(x,x2),((0,1,),))                                             
            return x1[0]
        
        # Reaction of Firm 2
        def reaction2(x1):
            x2 = optim.brute(lambda x: -profit2(x1,x),((0,1,),))                                             
            return x2[0]
        
        def vector_reaction1(x): 
            return np.array(x[0]) - np.array([reaction1(x[1]),reaction2(x[0])])
        
        def vector_reaction2(x): 
            return np.array(x) - np.array([reaction1(x[1]),reaction2(x[0])])
        
        if self.leader == 1:
            # Objective function
            def objectif(x):
                return  self.cost1(x[0]) - self.demand(x[0],x[1])*x[0]
            const = {'type': 'eq','fun' : lambda x : reaction2(x[0])}
        elif self.leader == 2:
            # Objective Function
            def objectif(x):
                return self.cost2(x[1]) - self.demand(x[0],x[1])*x[1]
            # 
            const = {'type': 'eq','fun' : lambda x : reaction1(x[1])}

        # Bounds
        bnds = (((0,None)),(0,None))
        # Optimization
        opt = optim.minimize(objectif,x0=self.initial_state,method="SLSQP",constraints=const,bounds=bnds)
        
        self.optimo_ = {"x1" : opt.x[0], "x2" : opt.x[1]}


       
    
    
   