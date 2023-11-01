# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotCONS(self,
             xlabel="Good 1",
             ylabel="Good 2", 
             title="Flexible demand systems",
             xlim=None,
             ylim=(0,300),
             addgrid=True,
             ax=None):
    
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

