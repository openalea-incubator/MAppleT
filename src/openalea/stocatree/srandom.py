#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: Summary

    A set of simple random functionalities

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.srandom import *

.. testsetup::

    from openalea.stocatree.srandom import *

"""

__all__ = ['random', 'boolean_event']

import random as std_random

"""
# Added by Han on 07-04-2011, to use the seed defined in the "parameters.ini" file #
# For batchmode only #
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree.tools.simulation import SimulationStocatree

# First, read the configuration file
options = ConfigParams(get_shared_data('stocatree.ini'))
if options.general.batchmode == True:
  options = ConfigParams(get_shared_data('parameters.ini'))

# Initialise the simulation
simulation = SimulationStocatree(dt=options.general.time_step,
  starting_date=options.general.starting_year,
  ending_date=options.general.end_year)

###################################################################################
"""

def random(*args):
    """returns a list of random values uniformly distributed

    1 or 2 arguments required.

    If only 1 argument is provided, a value between zero and the argument is returned
    using a uniform distribution. If 2 arguments are provided, the returned value will be between
    the two arguments.


    >>> x = random(1.5)
    >>> x = random(1., 2.)
    """
    # Added by Han on 07-04-2011, to fix the seed #
    #std_random.seed(1000)
    if len(args)==1:
        scale = args[0]
        if isinstance(scale, int):
            assert scale >= 0
            return std_random.randint(0, scale-1)
        elif isinstance(scale, float):
            return scale * std_random.random()
        else:
            raise ValueError('put an error message if we enter here')
    elif len(args)==2:
        m = args[0]
        M = args[1]
        assert m < M
        return std_random.uniform(m, M)
    else:
        raise ValueError("1 or 2 arguments expected")


def boolean_event(probability):
    """Return True if the random value is less than the  given probability.

    :param probability: a probability in [0,1]
    :rtype: boolean

    ::

        a = boolean_event(0.5)

    """
    assert probability >= 0.
    assert probability <= 1.0
    return std_random.random() < probability

