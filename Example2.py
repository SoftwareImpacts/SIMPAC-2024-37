
#Example 2: Analysis of simple supported beam with uniformly distributed loads (UDL) using :class:`StrucPy.RCFA.RCF`.


from PyRCD import RCbeam
import pandas as pd
import plotly

#First adjust the values of contraints function as per requirement

# r2= RCbeam(width=300, depth=450, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])
# r2.dsgbeam()



#Example 3
r2= RCbeam(width=200, depth=550, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])
r2.dsgbeam()
