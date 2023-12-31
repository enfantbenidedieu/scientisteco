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
    
    # Fill between
    p = p + gg.geom_ribbon(gg.aes(ymin = 0, ymax = bound2,where = "x<y"),fill = "blue", alpha = 0.4)

    # Add Text
    p = p + gg.annotate("text",x=self.optimo_[0]-0.5,y=self.optimo_[1]+0.5,label="(%s, %s)"%(round(self.optimo_[0],2),round(self.optimo_[1],2)))
    
    # Add Line for Optimal point
    p = p + gg.geom_segment(gg.aes(x=[self.optimo_[0],0],y=[0,self.optimo_[1]],xend=[self.optimo_[0],self.optimo_[0]],yend=[self.optimo_[1],self.optimo_[1]]),linetype= "dashed")

    # Add text
    
    
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