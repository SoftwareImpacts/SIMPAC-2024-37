Overview of PyRCD
====================

**PyRCD** is a powerful python library for design and multi-objective design optimization of reinforced concrete(RC) elements. PyRCD is originally developed for the students and researchers working in field of civil engineering. It will be highly helpful for research in design optimization, designing, and visualizing the detailing of RC beam. It is also highly beneficial for the learning process of graduate students. 

The uniqueness of *PyRCD* is that, it's a first generalized package for design and optimization of RC elements. Its simple functions can be adjusted as per any guidelines. It's flexible and versatile functions allows user to complete design and optimization in just few lines of codes. Its output is coupled with market practices which makes it ready to be deployed in actual construction. 

-------------------

Project Objectives
-------------------
Objective of **PyRCD** is to provide an easy to use open-source library for the upliftment of civil/structural engineering students and researchers.

*Validity*: PyRCD are continuously monitored to remove any bugs and errors. Users are requested to report any issue/error encountered while using PyRCD.

*User Friendly*: PyRCD provides a user-friendly approach for the design and optimization of RC elements without the use of extensive coding. In order to operate and visualize results user needs basic knowledge of python and some libraries like Pandas and Numpy.

*Improvement*: PyRCD intents to provide open source solution to every aspect of reinforced concrete structural design. The codes are often checked for improvements.

*Freedom*: PyRCD believes in the freedom of imagination and application. Thus, PyRCD gives full access to its users. Users can use those data's as per their requirement and research.

----------------

Dependencies
----------------
Required Dependencies

* **numpy**
* **pandas**
* **plotly**

------------------------------------------------------

Modules 
------------------------------------------------------
* **RCbeam** - Structural design and multi-objective optimization of reinforced concrete beams 
* **RCcolumn** (Under Development)


----------------

RCbeam
----------------
**RCbeam** provides solution to design and multi-objective optimization of reinforced concrete beams.

**Current Capabilities of RCbeam**

* Performs design checks on a designed RC beam.
* Performs designing of RC beam. 
* Perform multi-objective design optimization on RC beam.
* Provides pareto front in the form of dataframe. 
* Generates complete 2D and 3D detailing of RC beam. 
* Capable of handling both continuous and non-continuous beams.

**Speciality of RCbeam**

* Performs design and optimization considering detailed constructability function which includes market practice.
* Considers three objective function for optimization: Weight, Cost, and Environmental Impact (kgCO2emission) 
* Generalized package, and functions (objective function, constraints, constructability etc.) can be modified as per any design guidelines. 
* Ready to use design output.
* Considers development length and stirrups details in optimization.
* Suggest improvement during design checks.

----------------------------------------------------------

License
--------

[MIT] 
----------------------------------------------------------

