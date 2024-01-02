RCbeam Examples
=============


Example 1: Design check on already designed RC beam using :class:`PyRCD.RCbeam`.
---------------------------------------------------------------------------------------------

.. code-block:: python

    from PyRCD import RCbeam
    import pandas as pd
    import plotly

    #First adjust the values of constraints, rebar_config and constructability functions as per requirement

    # Example 1
    r1= RCbeam(width=300, depth=450, length=4, bending_moment=157, shear_force=130, ast_provided= 950)
    r1.check_beam()

    r1.beam_status

Example 2: Design of RC beam using :class:`PyRCD.RCbeam`.
------------------------------------------------------------------------------------------------------------------
.. code-block:: python

    from PyRCD import RCbeam
    import pandas as pd
    import plotly

    #First adjust the values of constraints, rebar_config and constructability functions as per requirement

    # Creating r2 object to represent RC beam
    r2= RCbeam(width=300, depth=450, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])

    r2.dsgbeam()                    # performing the design of RC beam

    rd= r2.rebar_detail             # Getting detail of reinforcement bars of RC beam
    sd= r2.shear_detail             # Getting detail of stirrup bars of RC beam

    r2.plotting()                   # Performing the detailing of RC beam
    d_3D= r2.detailing3D            # Getting 3D detailing of RC beam
    d_2D= r2.detailing2D            # Getting 2D detailing of RC beam



Example 3: Design optimization of RC beam using :class:`PyRCD.RCbeam`.
-------------------------------------------------------------------------------------------------------------------

.. code-block:: python

    from PyRCD import RCbeam
    import pandas as pd
    import plotly

    #First adjust the values of constraints, rebar_config and constructability functions as per requirement

    r3= RCbeam(width=300, depth=450, length=4, bending_moment=[187, 157, 105], shear_force=[125, 40, 98])     #Creating beam object
    r3.beam_optimization(nearest_value=25)              #Performing multiobjective optimization

    df= r3.optimization_result                          #Storing Pareto front results

    min_weight_index= df["Weight (Kg)"].idxmin()             #Getting index of minimum weight

    rd= r3.rd_list[min_weight_index]                    #Rebar detail for minimum weight
    sd= r3.sd_list[min_weight_index]                    #Shear detail for minimum weight
    r3.plotting(index= min_weight_index)                #Performing detailing

    fig= r3.detailing3D                                 #Storing 3D detailing
    fig1= r3.detailing2D                                #Storing 2D detailing

    fig.write_html("./3D_detailing.html")
    fig1.write_html("./2D_detailing.html")