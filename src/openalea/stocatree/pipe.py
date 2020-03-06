#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: pipe.py summary

    A module dedicated to pipe models

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.pipe import *

.. testsetup::

    from openalea.stocatree.pipe import *
"""


def get_new_radius(ra, rb, exponent=2.49, previous_rt=-1):
    """Pipe model computation

    Returns the radius :math:`r_t` of a pipe segment at a given time `t` given the radius of
    2 children pipe segments. The new radius is determined as follows:

    .. math::

        r_t = \sqrt[P]{r_{a,t}^P+r_{b,t}^P}

    However, to prevent the radius to shrink, you may want to provide the current
    radius (which is negative by default), in which case, the new radius is computed as
    follows:

    .. math::

        r_t = \max{\\left(\sqrt[P]{r_{a,t}^P+r_{b,t}^P}, r_{t-1}\\right)}

    :param ra: first radius
    :param rb: second radius
    :param previous_rt: the current radius. If previous_rt is provided,
        returns max of previous_rt and new radius; this is to prevent the radius to shrink.

    :return: :math:`r_t` the new radius

    """
    exponent_invert = 1./exponent
    rap = pow(ra, exponent)
    rbp = pow(rb, exponent)
    newrt =  pow(rap+rbp, exponent_invert)
    return newrt

