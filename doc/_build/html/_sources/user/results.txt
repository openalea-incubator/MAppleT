
############################
Results and Code validation
############################

.. contents::

Results
#######
Here below are some pictures of the simulation. For instance, after two years 
and a half, we obtained this visual results:

.. image:: stocatree_june_1996.jpg
.. image:: stocatree_sept_1996.jpg

============== ============
============== ============
|im1|          |im2|
============== ============

.. |im1| image:: stocatree_nov_1996.jpg 
    :width: 200pt
    :height: 200pt
    :align: middle
.. |im2| image:: stocatree_sept_1996.jpg 
    :width: 200pt
    :height: 200pt
    :align: middle


Code validation
###############

Here below are some numbers that can be compared


counts
=========================

Results from MAppleT (3 years)
::
    
    #shorts  longs florals mediums len_16_to_25    len_26_to_40    len_over_40 fruits

    0    0   0   0   0   0   0   0   0
    1    6   1   0   1   1   0   5   0
    73   34  43  0   23  22  11  1   0


:: 

    0   0   0   0   0   0   0   0
    0   7   1   0   1   1   2   4
    49  33  72  0   31  17  14  2

Results from stocatree (5 years)
::

    #shorts longs   florals 0   mediums len_16_to_25    len_26_to_40    len_over_40 fruits
    1995-01-01   0   0   0   0   0   0   0   0
    1996-01-01   1   6   1   0   1   1   0   5
    1997-01-01   48  38  52  0   19  11  25  2
    1998-01-01   300     58  238     0   62  45  11  2
    1999-01-01   557     30  245     0   119     27  3   0


Trunk size
============

**Trunk Radius in meters**

=================== ======= =======
                    Lpy     MAppleT
=================== ======= =======
year 1              0.00308 TODO
year 2              0.00679 TODO
year 3              0.01506 1.52 cm
year 4              0.023   TODO
=================== ======= =======

**Trunk surface**

=================== ======== =========
                    Lpy      MAppleT
=================== ======== =========
year 1              2.9 10-5
year 2              0.000144 TODO
year 2              0.000726 0.000734
year 4              0.0017   TODO
=================== ======== =========



.. plot:: pyplots/trunk_radius_versus_time.py
    :include-source:

.. image:: trunk_radius_versus_time_ori.png
    :width: 45%
    :height: 7cm


Fruits
=======

.. plot:: pyplots/fruit.py

Units
=====

Unlike MAppleT, stocatree does not used a specific units module to manage 
physical units. Units are in S.I. that is meters, kilograms. However, 
for convenience, the time units are currently set in days.






.. sectionauthor:: Thomas Cokelaer
