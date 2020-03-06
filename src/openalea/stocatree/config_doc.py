#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: configuration file summary

    Documentation of a standard configuration file to be used within stocatree

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: namespace_options.py 8954 2010-05-20 13:07:16Z cokelaer $

Stocatree requires a configuration file called **config.ini** that must contain specific sections and parameters.
Here below we provide an example of the different sections together with an explanation of their parameters.

general section
---------------

The [general] section is used to set the simulation parameters such as duration and steps::

    [general]
    verbose             = True
    max_iterations      = 24000
    starting_year       = 1994
    end_year            = 1996.5
    ; set to True, if simulation must stop when current year has reached end_year
    end_on_year         = True
    time_step           = 1
    seed                = 1163078255
    tag                 = test



* **tag** is used to tag output filenames
* **time_step** the step in days
* **max_iterations** is the maximum number of iterations. You need to take into account that 
  at each time step, they may be several iterations. For instance in stocatree there are 4 iterations 
  times N for each time step to loop over the different groups. N being the number of iteration required 
  by the rotation convergence (2 by default)
* **starting_year** should be kept to 1994 since many parameters depends on this year.
* **end_year** the end of the simulation. May be non integer. If **max_iterations** is reached, the simulation
  stops even though the time has not reached **end_year**

stocatree section
-----------------

The [stocatree] section sets some booleans that are obvious::

    [stocatree]
    saveimage   = False
    movie       = False

    ; Set to true to override the Markov models with a pool draw for the second year shoots
    second_year_draws = False

    ; Enable rupturing in branches
    ruptures = False

    ; Set the trunk on a stake - for all the trunk metamers to remain vertical
    stake = True

    ; Disable the rotation calculations (mechanics)
    mechanics = True

    ; render mode  may be bark, observations, zones, reaction_wood, year
    render_mode = bark

The **render mode**  may be bark, observations, zones, reaction_wood, year
render_mode = bark

=============== ==============================================
render options  description
=============== ==============================================
bark            use a bark-like colour
observations    colour encoding of the observations in the
                sequences extracted from the Markov models
zones           colour encoding of the zones in the
                sequences extracted from the Markov models
reaction_wood   colour relative to the amount of reaction
                wood in the outermost cambial layer
years           colour encoding the year of metamer appearance
=============== ==============================================

see :mod:`openalea.stocatree.output` for more information on the colors.

output section
--------------

The [output] section is described in :mod:`openalea.stocatree.output` and looks like::


    [output]
    sequences = False
    l_string  = False
    counts    = False
    trunk     = False
    leaves    = False
    mtg       = False

These options will allow to save relevant data:

=============== ===============================================================
config option   description
=============== ===============================================================
sequences       The sequences of observations generated from the Markov models
l_string        The L-string
counts          The numbers of shoots generated per length category
trunk           Properties regarding the metamer adjacent to the root
mtg             An MTG representation of the tree
leaves          Status of the leaves (e.g, position) (draft)
=============== ===============================================================

tree section
-------------
The [output] section is described in :mod:`openalea.stocatree.tree` and looks like::



    [tree]
    phyllotactic_angle              = -144.0
    branching_angle                 = -45.
    floral_angle                    = -10.
    tropism                         =  0.1
    preformed_leaves                =  8
    spur_death_probability          =  0.3
    inflorescence_death_probability  =  0.2

wood section
------------
The [wood] section is described in :class:`openalea.stocatree.wood.Wood` and looks like::


    [wood]
    ;The following parameters name are the keys required to create a Wood class, which in turn is used to instanciate a metamer_data class
    ;;in kgs/m3
    wood_density                      = 1000
    reaction_wood_rate                = 0.5
    reaction_wood_inertia_coefficient = 0.1
    ; in GPa
    youngs_modulus                    = 1.1
    ; in Pa
    modulus_of_rupture                = 50e6


internode section
------------------
The [internode] section is described in :class:`openalea.stocatree.internode.Internode` and looks like::


    [internode]
    ;min_length in meters
    min_length          = 0.0001
    ; elongation and plastochrom in days
    elongation_period   = 10.
    plastochron         = 3.


apex section
--------------
The [apex] section is described in :class:`openalea.stocatree.apex.apex_data` and looks like::


    [apex]
    ; im meters per day
    terminal_expansion_rate=0.00002
    ; in meters
    minimum_size=0.00075
    ; in meters
    maximum_size=0.006

markov section
---------------
The [markov] section is described in :class:`openalea.stocatree.sequences.Markov` and looks like::


    [markov]
    ; must be less than 100
    maximum_length = 70
    minimum_length = 4

fruit section
--------------
The [fruit] section is described in :class:`openalea.stocatree.fruit.AppleFruit` and looks like::



    [fruit]
    flower_duration             = 10.
    max_relative_growth_rate    = 0.167
    lost_time                   = 28
    max_age                     = 147
    probability                 = 0.3
    max_absolute_growth_rate    = 0.0018

leaf section
--------------
The [leaf] section is described in :class:`openalea.stocatree.leaf.AppleLeaf` and looks like::


    [leaf]
    ; maturation is in days
    ; mass_per_area, in kgs/m**2
    ; max_area, min_final_area in meters**2
    ; petiole_radius in meters
    fall_probability = 0.1
    maturation       = 12
    mass_per_area    = 0.220
    max_area         = 0.0030
    min_final_area   = 0.0020
    petiole_radius   = 0.0006
    preformed_leaves = 8



"""
