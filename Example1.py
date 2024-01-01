#Example 1: Analysis of fixed Beam With multiple point loads using :class:`StrucPy.RCFA.RCF`.

from PyRCD import RCbeam
import pandas as pd
import plotly

#First adjust the values of contraints function as per requirement

# Example 1
r1= RCbeam(width=300, depth=450, length=4, bending_moment=157, shear_force=130, ast_provided= 950)
r1.check_beam()


