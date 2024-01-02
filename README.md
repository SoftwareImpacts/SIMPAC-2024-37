# PyRCD

**PyRCD** is a powerful python library for design and multiobjective design optimization of reinforced concrete(RC) elements. PyRCD is originally developed for the students and researchers working in field of civil engineering. It will be highly helpful for research in design optimization, designing, and visualizing the detailing of RC beam. It is also highly beneficial for the learning process of graduate students. 

------------------------------------------------------------------------------------------------------------
## Modules 

* **RCbeam** - Structural analysis module for Reinforced Concrete Framed Structures 
* **RCcolumn** - (Under Development)

------------------------------------------------------------------------------------------------------------

## Project Objectives

Objective of **PyRCD** is to provide an easy to use open-source library for the upliftment of civil/structural engineering students and researchers.

*Validity*: PyRCD are continuously monitored to remove any bugs and errors. Users are requested to report any issue/error encountered while using PyRCD.

*User Friendly*: PyRCD provides a user-friendly approach for the design and optimization of RC elements without the use of extensive coding. In order to operate and visualize results user needs basic knowledge of python and some libraries like Pandas and Numpy.

*Improvement*: PyRCD intents to provide open source solution to every aspect of reinforced concrete structural design. The codes are often checked for improvements.

*Freedom*: PyRCD believes in the freedom of imagination and application. Thus, PyRCD gives full access to its users. Users can use those data's as per their requirement and research.

------------------------------------------------------------------------------------------------------------

## Dependencies

Required Dependencies

* **numpy**
* **pandas**
* **plotly**

------------------------------------------------------------------------------------------------------------

## "RCbeam" Module
----------------
**RCbeam** provides solution to design and multi-objective design optimization of reinforced concrete beams.

**Current Capabilities of RCbeam**

* Performs design checks on a designed RC beam.
* Performs designing of RC beam. 
* Perform multiobjective design optimization on RC beam.
* Provides pareto front in the form of dataframe. 
* Generates complete 2D and 3D detailing of RC beam. 
* Capable of handling both continous and non-continous beams.

**Specialty of RCbeam**

* Performs design and optimization considering detailed constructability function which includes market practice.
* Considers three objective function for optimization: Weight, Cost, and Environmental Impact (kgCO2emission) 
* Generalized package, and functions (objective function, constraints, constructability etc.) can be modified as per any design guidelines. 
* Ready to use design output.
* Considers development length and stirrups details in optimization.
* Suggest improvement during design checks.
* Capable of handling both continuous and noncontinuous beams.
 

------------------------------------------------------------------------------------------------------------

## PyRCD Documentation

https://pyrcd.readthedocs.io/

------------------------------------------------------------------------------------------------------------

## Installation (from Git repository)

1) Clone the repository using **https://github.com/TabishIzhar/PyRCD.git**

2) Form a virtual environment using 
```
    $ py -3 -m venv venv
```

3) Activate virtual environment from cmd
```
    .\venv\Scripts\activate.bat
```

4) Install every dependency using requirement.txt
```
    (.venv) $ pip install -r requirements.txt
```
------------------------------------------------------------------------------------------------------------

## Preferred Integrated Development Environment (IDE)

For proper visualization of graphs and models.

* Jupyter Notebook
* VS Code 

-----------------------------------------------------------------------------------------------------------

## Usage

```python

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
```
------------------------------------------------------------------------------------------------------------
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

------------------------------------------------------------------------------------------------------------

## License

[MIT]