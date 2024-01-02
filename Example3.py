# Example 3: Design optimization of RC beam using :class:`PyRCD.RCbeam`.

from PyRCD.RCbeam import rcb
import pandas as pd
import plotly

#First adjust the values of contraints and constructability function as per requirement

r2= rcb(width=300, depth=450, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])     #Creating beam object
r2.beam_optimization(nearest_value=25)              #Performing multiobjective optimization

df= r2.optimization_result                          #Storing Pareto front results

min_weight_index= df["Weight (Kg)"].idxmin()             #Getting index of minimum weight

rd= r2.rd_list[min_weight_index]                    #Rebar detail for minimum weight
sd= r2.sd_list[min_weight_index]                    #Shear detail for minimum weight
# r2.plotting(index= min_weight_index)                #Performing detailing

d_3d= r2.detailing3D                                 #Storing 3D detailing
d_2d= r2.detailing2D                                #Storing 2D detailing

d_3d.write_html("./3D_detailing.html")              #saving detailing file
d_2d.write_html("./2D_detailing.html")              #saving detailing file