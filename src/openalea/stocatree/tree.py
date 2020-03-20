#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: Summary

    Module used to define a tree with its standard characteristics
    such as branching angles, tropism, ...

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.tree import *

.. testsetup::

    from openalea.stocatree.tree import *
"""


from vplants.plantgl.all import Vector3
from constants import pi
from physics import Frame


class Tree():
    """A class to manage instance of trees.

    This class defines only parameters although there are two methods that allows to
    switch between radians and degrees for the angle parameters.

    >>> tree = Tree(branching_angle=45, tropism=0.5)
    >>> tree.convert_to_radians()
    """
    def __init__(self, phyllotactic_angle=-144.0, branching_angle=-45.,
                 floral_angle=-10., tropism=0.1, preformed_leaves=8,
                 spur_death_probability=0.3,
                inflorescence_death_probability=0.2):
        """**Constructor**

        ================================== ============== ==============
        parameters                         default values  units
        ================================== ============== ==============
        phyllotactic_angle                 144             degrees
        branching angle                    45              degrees
        ================================== ============== ==============


        :param phyllotactic_angle: default is -144 degrees
        :param branching_angle: default is -45 degrees
        :param floral_angle: default -10 degrees
        :param spur_death_probability: default is0.3
        :param tropism: the z value of the tropism vector (efault is z=0.1)
        :param preformed_leaves: 8
        :param inflorescence_death_probability: default is 0.2

        In addition, several attributes are defined:

            * an initial HLU frame is also defined to be along the z axis.
            * trunk_radius in meters
            * fruits : number of fruits
            * cross_sectional_area in m^2
            * growth units
            * fruit_load

        .. todo:: finalise this doc. end_terminal_expansion not used !
            Neither in original code.

        """
        self.angle_unit = 'radians'
        self.phyllotactic_angle              = phyllotactic_angle / 180.0 * pi
        self.branching_angle                 =  branching_angle / 180.0 * pi
        self.floral_branching_angle          =  floral_angle / 180.0 * pi
        # the original mappelt code the initial hlu frame as follows
        #self.initial_hlu  = Frame(Vector3( 0.0, 1.0, 0.0), Vector3( 0.0, 0.0, 1.0), Vector3(-1.0, 0.0, 0.0)); #
        # this one seems to work, which seems logival since HLU when the tree starts corresponds to zxy or zyx.
        self.initial_hlu                     = Frame(Vector3( 0.0, 0.0, 1.0), Vector3( 0.0, 1.0, 0.0), Vector3(1., 0.0, 0.));
        # the original one from mapplet leads to trunk being horizontal
        #self.initial_hlu                     = Frame(Vector3( 0.0, 1.0, 0.0), Vector3( 0.0, 0.0, 1.0), Vector3(-1., 0.0, 0.));
        self.spur_death_probability          = spur_death_probability
        self.inflorescence_death_probability = inflorescence_death_probability
        self.preformed_leaves                = preformed_leaves

        # variables
        self.trunk_radius                    = 0.0  #in m
        self.trunk_cross_sectional_area      = 0    #cm**2'
        self.fruit_load                      = 0.   #1/m**2
        #self.end_terminal_expansion          = convert_to_day(11, 1);
        # Count the number of growth units (note that the parent_unit_id starts from 0):
        # Commented by Han on 02-05-2011
        self.growth_units                    = 0
        # Count the number of first-order branches (note that the parent_branch_id starts from 0)
        # Added by Han on 02-05-2011
        self.first_branches                  = 0
        self.tropism                         = Vector3(0.0, 0.0, tropism); #// same as in N original mapplet
        self.fruits                          = 0

    def convert_to_radians(self):
        """.. deprecated:: v8991"""
        if self.angle_unit=="degrees":
            self.phyllotactic_angle /= 180.0 / pi
            self.branching_angle /= 180.0 / pi
            self.floral_branching_angle /=  180.0 / pi
            self.angle_unit = "radians"

    def convert_to_degrees(self):
        """.. deprecated:: v8991"""
        if self.angle_unit=="radians":
            self.phyllotactic_angle *= 180.0 / pi
            self.branching_angle *= 180.0 / pi
            self.floral_branching_angle *=  180.0 / pi
            self.angle_unit = "degrees"
