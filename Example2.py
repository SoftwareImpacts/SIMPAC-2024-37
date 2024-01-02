
#Example 2: Design of RC beam using :class:`PyRCD.RCbeam`.


from PyRCD.RCbeam import rcb
import pandas as pd
import plotly

#First adjust the values of contraints function as per requirement

#Example 2
r2= rcb(width=200, depth=550, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])
r2.dsgbeam()

rd= r2.rebar_detail             # Getting detail of reinforcement bars of RC beam
sd= r2.shear_detail             # Getting detail of stirrup bars of RC beam

r2.plotting()                   # Performing the detailing of RC beam
d_3D= r2.detailing3D            # Getting 3D detailing of RC beam
d_2D= r2.detailing2D            # Getting 2D detailing of RC beam