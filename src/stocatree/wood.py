#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: Summary

    A module dedicated to the wood

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.wood import *
    
.. testsetup::

    from openalea.stocatree.wood import *
"""

wood_options = {
    'wood_density'                      : 1000,
    'reaction_wood_rate'                : 0.5,
    'reaction_wood_inertia_coefficient' : 0.1,
    'youngs_modulus'                    : 1.1,
    'modulus_of_rupture'                : 50e6}


class Wood():
    """a class to manage wood characteristics

    This class has only one constructor and no methods. It is used
    to store the wood parameters only.

    
    ================================== ============== ==============
    parameters                         default values  units
    ================================== ============== ==============
    density                            1000           kgs per m^3
    reaction_wood_rate                 0.5
    reaction_wood_inertia_coefficient  0.1
    youngs_modulus                     1.0            GPa
    modulus of rupture                 50 10e-6       Pa
    ================================== ============== ==============

    .. note:: in stocatree, the config.ini file contains a section [wood] that
            allows to instanciate this class.
    """
    def __init__(self, wood_density=1000, reaction_wood_rate=0.5, 
                 reaction_wood_inertia_coefficient=0.1, youngs_modulus=1.1,
                 modulus_of_rupture=50e6):
        """**Constructor**

        
        :param wood_density:
        :param reaction_wood:
        :param reacton_wood_inertia_coefficient:
        :param youngs_modulus:
        :param modulus of rupture:


        .. todo:: use Pa for youngs modulus in the config file.
        """


        self._density = wood_density 
        self._reaction_wood_rate = reaction_wood_rate
        self._reaction_wood_inertia_coefficient = \
            reaction_wood_inertia_coefficient
        self._youngs_modulus = youngs_modulus

        #TODO convert into Pa ? 
        self._youngs_modulus *= 1e9
        self._modulus_of_rupture = modulus_of_rupture