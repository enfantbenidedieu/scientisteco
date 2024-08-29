# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import plotnine as gg

def fviz_consumption(self,
                     x_label = "Good 1",
                     y_label = "Good 2",
                     title = "Flexible Demand Systems",
                     color="blue",
                     theme=gg.theme_minimal()) -> gg:
    """
    Visualize consumption function
    ------------------------------

    Usage
    -----
    ```
    >>>
    ```

    Parameters
    ----------
    `self` : an object of class CONSUMPTION

    `x_label` : a string

    `y_label` : a string
    
    
    Author(s)
    ---------
    Duvérier DJIFACK ZEBAZE djifacklab@gmail.com
    """
    

    if self.model_ != "consumption":
        raise ValueError("'self' must be an object of class CONSUMPTION.")
    

    bound1, bound2 = self.R/self.p1, self.R/self.p2
    data = pd.DataFrame({"x" :[bound1,0], "y":[0,bound2]})
    p = (gg.ggplot(data,gg.aes(x="x",y="y"))+gg.geom_line(color=color)+
            gg.geom_hline(yintercept = 0)+gg.geom_vline(xintercept = 0))
    
    # Fill between
    #p = p + gg.geom_ribbon(gg.aes(ymin = 0, ymax = bound2,where = "x<y"),fill = "blue", alpha = 0.4)

    # Add Text
    p = p + gg.annotate("text",x=self.optimo_["x1"]-0.5,y=self.optimo_["y1"]+0.5,
                        label="(%s, %s)"%(round(self.optimo_["x1"],2),round(self.optimo_["y1"],2)))
    
    # Add Line for Optimal point
    p = p + gg.geom_segment(gg.aes(x=[self.optimo_["x1"],0],y=[0,self.optimo_["y1"]],
                                   xend=[self.optimo_["x1"],self.optimo_["x1"]],yend=[self.optimo_["y1"],self.optimo_["y1"]]),linetype= "dashed")

    # Add text
    
    
    if x_label is None:
        x_label = "Good 1"
    if y_label is None:
        y_label = "Good 2"
    if title is None:
        title = "Flexible Demand Systems"
    
    p = p + gg.labs(x=x_label,y=y_label,title=title)

    # Add theme
    p = p + theme
    return p