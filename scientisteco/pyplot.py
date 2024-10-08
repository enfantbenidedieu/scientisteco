# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize as optim

def plotCONS(self,
             xlabel="Good 1",
             ylabel="Good 2", 
             title="Flexible demand systems",
             xlim=None,
             ylim=(0,300),
             addgrid=True,
             ax=None) -> plt:
    
    if ax is None:
        ax = plt.gca()

    def func_(u,x):
        return (u**(1/self.beta))/(x)**(self.alpha/self.beta)

        
    # Initial plot
    ax.plot([self.R/self.p1,0],[0,self.R/self.p2],color="blue")
    # Add optimal point
    ax.plot(self.optimo_["x1"],self.optimo_["y1"],marker="o",color="blue")
    ax.plot([self.optimo_["x1"],self.optimo_["x1"]],[0,self.optimo_["y1"]],linestyle="dashed",color="blue")
    ax.plot([0,self.optimo_["x1"]],[self.optimo_["y1"],self.optimo_['y1']],linestyle="dashed",color="blue")
    # Add Text
    ax.text(self.optimo_['x1'], self.optimo_['y1'], "(%.2f, %.2f)"%(self.optimo_['x1'],self.optimo_['y1']),color="blue")
    # Add Indifference curve
    x1 = np.arange(1,self.R/self.p1)
    y1 = func_(self.optimo_["u1"],x1)
    ax.plot(x1,y1,color="blue",label=r"$\hat{U}_{0}$ = "+str(round(self.optimo_['u1'],2))+" (initial state)")


    # Add New Price - First price
    if self.new_p1 is not None:
        ax.plot([self.R/self.new_p1,0],[0,self.R/self.p2],color="red")
        ax.plot(self.new_optimo_["x2"],self.new_optimo_["y2"],marker="o",color="red")
        ax.plot([self.new_optimo_["x2"],self.new_optimo_["x2"]],[0,self.new_optimo_["y2"]],linestyle="dashed",color="red")
        ax.plot([0,self.new_optimo_["x2"]],[self.new_optimo_["y2"],self.new_optimo_['y2']],linestyle="dashed",color="red")
        # Add Text
        ax.text(self.new_optimo_['x2'], self.new_optimo_['y2'], "(%.2f, %.2f)"%(self.new_optimo_['x2'],self.new_optimo_['y2']),color="red")

        # Add Indifference curve
        x2 = np.arange(1,self.R/self.new_p1)
        y2 = func_(u=self.new_optimo_["u2"],x=x2)
        ax.plot(x2,y2,color="red",label=r"$\hat{U}_{1}$ = "+str(round(self.new_optimo_['u2'],2))+" (final state)")

        ## Add Intermediaire analysis
        ax.plot([self.new_optimo_["R3"]/self.new_p1,0],[0,self.new_optimo_["R3"]/self.p2],linestyle="dashed",color="black")
        ax.plot(self.new_optimo_["x3"],self.new_optimo_["y3"],marker="o",color="black")
        ax.plot([self.new_optimo_["x3"],self.new_optimo_["x3"]],[0,self.new_optimo_["y3"]],linestyle="dashed",color="black")
        ax.plot([0,self.new_optimo_["x3"]],[self.new_optimo_["y3"],self.new_optimo_['y3']],linestyle="dashed",color="black")
        # Add Text
        ax.text(self.new_optimo_['x3'], self.new_optimo_['y3'], "(%.2f, %.2f)"%(self.new_optimo_['x3'],self.new_optimo_['y3']),color="black")

        # Add Indifference curve
        x3 = np.arange(1,self.new_optimo_["R3"]/self.new_p1) 
        y3 = func_(self.new_optimo_["u3"],x3)
        ax.plot(x3,y3,color="black",linestyle="dashed",label=r"$\hat{U}_{2}$ = "+str(round(self.new_optimo_['u3'],2))+" (intermediate state)")
    # Second price
    elif self.new_p2 is not None:
        ax.plot([self.R/self.p1,0],[0,self.R/self.new_p2],color="red")
        ax.plot(self.new_optimo_["x2"],self.new_optimo_["y2"],marker="o",color="red")
        ax.plot([self.new_optimo_["x2"],self.new_optimo_["x2"]],[0,self.new_optimo_["y2"]],linestyle="dashed",color="red")
        ax.plot([0,self.new_optimo_["x2"]],[self.new_optimo_["y2"],self.new_optimo_['y2']],linestyle="dashed",color="red")
        # Add Text
        ax.text(self.new_optimo_['x2'], self.new_optimo_['y2'], "(%.2f, %.2f)"%(self.new_optimo_['x2'],self.new_optimo_['y2']),color="red")

        # Add Indifference curve
        x2 = np.arange(1,self.R/self.p1)
        y2 = func_(self.new_optimo_["u2"],x2)
        ax.plot(x2,y2,color="red",label=r"$\hat{U}_{1}$ = "+str(round(self.new_optimo_['u2'],2))+" (final state)")

        ## Add Intermediaire analysis
        ax.plot([self.new_optimo_["R3"]/self.p1,0],[0,self.new_optimo_["R3"]/self.new_p2],linestyle="dashed",color="black")
        ax.plot(self.new_optimo_["x3"],self.new_optimo_["y3"],marker="o",color="black")
        ax.plot([self.new_optimo_["x3"],self.new_optimo_["x3"]],[0,self.new_optimo_["y3"]],linestyle="dashed",color="black")
        ax.plot([0,self.new_optimo_["x3"]],[self.new_optimo_["y3"],self.new_optimo_['y3']],linestyle="dashed",color="black")
        # Add Text
        ax.text(self.new_optimo_['x3'], self.new_optimo_['y3'], "(%.2f, %.2f)"%(self.new_optimo_['x3'],self.new_optimo_['y3']),color="black")

        # Add Indifference curve
        x3 = np.arange(1,self.new_optimo_["R3"]/self.p1) 
        y3 = func_(self.new_optimo_["u3"],x3)
        ax.plot(x3,y3,color="black",linestyle="dashed",label=r"$\hat{U}_{2}$ = "+str(round(self.new_optimo_['u3'],2))+" (intermediate state)")
    # income
    elif self.new_R  is not None:
        ax.plot([self.new_R/self.p1,0],[0,self.new_R/self.p2],color="red")
        ax.plot(self.new_optimo_["x2"],self.new_optimo_["y2"],marker="o",color="red")
        ax.plot([self.new_optimo_["x2"],self.new_optimo_["x2"]],[0,self.new_optimo_["y2"]],linestyle="dashed",color="red")
        ax.plot([0,self.new_optimo_["x2"]],[self.new_optimo_["y2"],self.new_optimo_['y2']],linestyle="dashed",color="red")
        # Add Text
        ax.text(self.new_optimo_['x2'], self.new_optimo_['y2'], "(%.2f, %.2f)"%(self.new_optimo_['x2'],self.new_optimo_['y2']),color="red")

        # Add Indifference curve
        x2 = np.arange(1,self.new_R/self.p1)
        y2 = func_(self.new_optimo_["u2"],x2)
        ax.plot(x2,y2,color="red",label=r"$\hat{U}_{1}$ = "+str(round(self.new_optimo_['u2'],2))+" (final state)")

    # Add Legend
    legend = ax.legend()
    color = ["blue","red","black"]
    for i, text in enumerate(legend.get_texts()):
        text.set_color(color[i])
    ax.axhline(y=0,color="black",linestyle="-")
    ax.axvline(x=0,color="black",linestyle="-")
    ax.grid(visible=addgrid)
    ax.set(xlabel=xlabel,ylabel=ylabel,title=title,xlim=xlim,ylim=ylim)





############################################################################################
#       DUOPOLY
############################################################################################
    
def plotDUOPOLE(self,
                xlim = (0,120),
                ylim = (0,120),
                xlabel = None,
                ylabel = None,
                title  = None,
                point_size=100,
                color1 = "blue",
                color2 = "red",
                label1 = "Firm 1's Reaction Curve",
                label2 = "Firm 2's Reaction Curve",
                delta = 0.5,
                add_grid = True,
                ax=None) -> plt:
    """
    
    """

    if self.model_ != "duopole":
        raise ValueError("Error : ")

    if ax is None:
        ax = plt.gca()

    # Firm 1 profit
    profit1 = lambda x1, x2 : self.demand(x1,x2)*x1 - self.cost1(x1)
    # Firm 2 profit
    profit2 = lambda x1, x2 : self.demand(x1,x2)*x2 - self.cost2(x2)

    if self.method == "cournot":

        def reaction1(x2):
            x1 = optim.brute(lambda x: -profit1(x,x2),((0,1,),))                                          
            return x1[0]

        def reaction2(x1):
            x2 = optim.brute(lambda x: -profit2(x1,x),((0,1,),))                                                   
            return x2[0]
        
        # Firm 1' reactive curve
        x2 = np.linspace(ylim[0],ylim[1])
        xx = np.array([reaction1(x) for x in x2])
        # Firm 2 reactive curve
        x1 = np.linspace(xlim[0],xlim[1])
        yy = np.array([reaction2(x) for x in x1])

        ax.plot(xx,x2,color=color1,label=label1+" ("+r"$\hat{\pi}_{1}$ = "+str(round(self.profit_["profit1"],2))+")")
        ax.plot(x1,yy,color=color2,label=label2+" ("+r"$\hat{\pi}_{2}$ = "+str(round(self.profit_["profit2"],2))+")")
        ax.plot([0,self.optimo_["x1"]],[self.optimo_["x2"],self.optimo_["x2"]],linestyle="--",color="red")
        ax.plot([self.optimo_["x1"],self.optimo_["x1"]],[0,self.optimo_["x2"]],linestyle="--",color="blue")
        ax.scatter(x=self.optimo_["x1"],y=self.optimo_["x2"],color="black",s=point_size,marker="o",label="Cournot Equilibrium point")
        ax.text(x=self.optimo_["x1"]+delta,y=self.optimo_["x2"]+delta,
                s="("+str(round(self.optimo_["x1"],2))+","+str(round(self.optimo_["x2"],2))+")",
                fontsize=12,color="black",weight='bold')
        ax.axvline(x=0,color="black")
        ax.axhline(y=0,color="black")

        # Set x - label
        if xlabel is None:
            xlabel = "output of firm 1"
        # Set y - label
        if ylabel is None:
            ylabel = "output of firm 2"
        # Set title
        if title is None:
            title = "Cournot - Nash Duopoly Equilibrium"

        # 
        ax.grid(visible=add_grid)
        ax.set(xlabel=xlabel,ylabel=ylabel,title=title)
        ax.legend()



        


    