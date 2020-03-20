#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: internode.py summary

   A module dedicated to define an internode

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.internode import *

.. testsetup::

    from openalea.stocatree.internode import *
"""

__all__ = ['Internode']



internode_options = {
    'min_length'          : 0.0001,
    'elongation_period'   : 10.,
    'plastochron'         : 3.}



class Internode(object):
    """Internode class to be used within a metamer

    >>> i = Internode()
    >>> i._plastochron
    3.0
    >>> i.growth_rate('small')
    0.001

    """
    def __init__(self, min_length=0.0001, elongation_period=10.,
                 plastochron=3.0, max_length = 3.0):
        """
        The "final_length_amplifier" attribute was added by Han on 14-04-2011.
        """
        r"""**internode constructor**

        ====================  ========================== ========================= ====================
        type                  notation                   default value             units
        ====================  ========================== ========================= ====================
        plastochron                                      3                         days
        elongation_period                                10                        days
        min_length            :math:`l_{\rm{min}}^{i}`    0.0001                    m/day
        ====================  ========================== ========================= ====================


        :param min_length:
        :param plastochron:
        :param elongation period:

        """
        self._min_length = min_length # switch to meters
        self._plastochron = plastochron
        self._elongation_period = elongation_period
        self._max_length = max_length

        """
        # The following parameters were added by Han on 11-04-2011
        # to replace the numerical representqtions in "growth_rate()"
        self._final_none = final_none
        self._final_dormant_start = final_dormant_start
        self._final_small = final_small
        self._final_diffuse = final_diffuse
        self._final_medium = final_medium
        self._final_floral = final_floral
        self._final_dormant_end = final_dormant_end
        self._final_else = final_else
        """

        """
        # The following parameters were added by Han on 17-04-2011
        # This allows the feasibility to only modify max_length in the "ini" file
        # for sensitivity analysis
        self._final_none = self._max_length * (3.0/3.0)
        self._final_dormant_start = self._max_length * (0.5/3.0)
        self._final_small = self._max_length * (1.0/3.0)
        self._final_diffuse = self._max_length * (2.3/3.0)
        self._final_medium = self._max_length * (2.7/3.0)
        self._final_floral = self._max_length * (3.0/3.0)
        self._final_dormant_end = self._max_length * (0.6/3.0)
        self._final_else = self._max_length * (2.0/3.0)
        # Alhtough the internode max_length is changable in the ini file, which
        # could not be 3.0, the ratio for handling different zones can be kept.
        # Commented by Han on 03-05-2011
        """

        """
        # The follwoing parameters were further modified by Han in December 2011
        # The idea is to use mean value rather than the maixmum one to control
        #     internode elongation. That means, all the internodes in the same
        #     zone will reach the same length, which is calculated by
        #               mean = maximum/1.5
        # And only the "diffuse" zone can use the maximum value as user-defined
        #     for this calculation. For other zones, a coefficient is multiplied
        #     according to Evelyne's knowledge.
        self._final_none = self._max_length/1.5
        self._final_dormant_start = self._min_length
        self._final_small = 0.5 * self._max_length/1.5
        self._final_diffuse = self._max_length/1.5
        self._final_medium = 0.75 * self._max_length/1.5
        self._final_floral = 0.5 * self._max_length/1.5
        self._final_dormant_end = self._min_length
        self._final_else = 0.25 * self._max_length/1.5
        """

        """
        #Modified by Han on 06-03-2012 according to Evelyne's knowledge
        self._final_none = self._max_length/1.5
        self._final_dormant_start = 0.25 * self._max_length/1.5
        self._final_small = 0.5 * self._max_length/1.5
        self._final_diffuse = self._max_length/1.5
        self._final_medium = self._max_length/1.5
        self._final_floral = 0.75 * self._max_length/1.5
        self._final_dormant_end = 0.25 * self._max_length/1.5
        self._final_else = 0.25 * self._max_length/1.5
        """

        #Modified by Han on 07-03-2012 according to Evelyne's knowledge (because of instability prbs in bio-mechanics)
        self._final_none = self._max_length/1.5
        self._final_dormant_start = 0.25 * self._max_length/1.5
        self._final_small = 0.5 * self._max_length/1.5
        self._final_diffuse = self._max_length/1.5
        self._final_medium = 0.75 * self._max_length/1.5
        self._final_floral = 0.5 * self._max_length/1.5
        self._final_dormant_end = 0.25 * self._max_length/1.5
        self._final_else = 0.25 * self._max_length/1.5



        """
        # The following parameters were added by Han on 14-04-2011
        self.final_length_amplifier = final_length_amplifier
        self._final_none = final_none * final_length_amplifier
        self._final_dormant_start = final_dormant_start * final_length_amplifier
        self._final_small = final_small * final_length_amplifier
        self._final_diffuse = final_diffuse * final_length_amplifier
        self._final_medium = final_medium * final_length_amplifier
        self._final_floral = final_floral * final_length_amplifier
        self._final_dormant_end = final_dormant_end * final_length_amplifier
        self._final_else = final_else * final_length_amplifier
        """

    def growth_rate(self, uzone):
        """compute te growth rate of the internode as a function of its zone

        :Hypothesis:

        The elongation rate of an internode depends on the zone in which it appears

        :param float uzone: zone in which is situated the internode

        :returns: a velocity in m/day
        """
        # To avoid unnecessary errors and confusions, the calculation of internode
        # length will be based on meters rather than centimeters. (Commented by Han
        # on 03-05-2011)

        # cm2m = 0.01

        #10 and none are not equivalent. Thhe else at the end corerspond to 10
        # When the apex leads the growth of the trunk, the returned value is "None"
        # (Noted by Han on 11-04-2011)
        if uzone == None:
            res = self._final_none / self._elongation_period
        elif uzone == 'dormant_start':
            res = self._final_dormant_start / self._elongation_period
        elif uzone == 'small':
            res = self._final_small / self._elongation_period
        elif uzone == 'diffuse':
            res = self._final_diffuse / self._elongation_period
        elif uzone == 'medium':
            res = self._final_medium / self._elongation_period
        elif uzone == 'floral':
            res = self._final_floral / self._elongation_period
        elif uzone == 'dormant_end':
            res = self._final_dormant_end / self._elongation_period
        else:
            res = self._final_else / self._elongation_period
        """
        if uzone == None:
            res =  3.0 / self._elongation_period * cm2m
        elif uzone == 'dormant_start':
            res = 0.5 / self._elongation_period *cm2m
        elif uzone == 'small':
            res = 1.0 / self._elongation_period *cm2m
        elif uzone == 'diffuse':
            res = 2.3 / self._elongation_period *cm2m
        elif uzone == 'medium':
            res = 2.7 / self._elongation_period *cm2m
        elif uzone == 'floral':
            res = 3.0 / self._elongation_period *cm2m
        elif uzone == 'dormant_end':
            res = 0.6 / self._elongation_period *cm2m
        else:
            res = 2.0 / self._elongation_period *cm2m
        """

        return res