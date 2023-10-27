# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import plotnine as gg


def fviz_consumption(self,
                     xlabel = "Good 1",
                     ylabel = "Good 2",
                     title = "Flexible Demand Systems",
                     color="black",
                     theme=gg.theme_classic()):
    

    if self.model_ != "consumption":
        raise ValueError("Error : 'self' must be an object of class CONSUMPTION.")
    

    bound1, bound2 = self.R/self.p1, self.R/self.p2
    data = pd.DataFrame({"x" :[bound1,0], "y":[0,bound2]})
    p = (gg.ggplot(data,gg.aes(x="x",y="y"))+gg.geom_line(color=color)+
            gg.geom_hline(yintercept = 0)+gg.geom_vline(xintercept = 0))
    
    if xlabel is None:
        xlabel = "Good 1"
    if ylabel is None:
        ylabel = "Good 2"
    if title is None:
        title = "Flexible Demand Systems"
    
    p = p + gg.labs(x=xlabel,y=ylabel,title=title)

    # Add theme
    p = p + theme
    return p