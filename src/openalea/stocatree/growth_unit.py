#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: growth_unit.py summary

    A module dedicated to growth units

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $
    :Usage: from openalea.stocatree.growth_unit import *

.. testsetup::

    from openalea.stocatree.growth_unit import *
"""


__all__ = [
    'growth_unit_data'
    ]


class growth_unit_data(object): 
    """A simple class for the growth unit data structure

    This class is used within the Lpy file only at the production level.

    For example, if a module called growth_unit is declared as follows::

        module growth_unit(growth_unit_data): scale=1

    then, it can be produced as follows::

        nproduce growth_unit(growth_unit_data(10, 1994, parent_observation=='floral'))

    """
    def __init__(self, index=0, year=0, inflorescence=False):
        """Constructor

        :param index: the index of this growth unit (default is 0)
        :param year: default is 0
        :param inflorescence: default is False

        """
        self.index = index
        self.year =year
        self.inflorescence = inflorescence


