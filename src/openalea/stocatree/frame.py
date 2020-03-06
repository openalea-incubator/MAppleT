"""
.. topic:: summary

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :References:
        1. Colin Smith, Costes Evelyne, On the Simulation of Apple Trees Using 
           Statistical and Biomechanical Principles, INRIA technical report, 2007

    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.frame import *

.. testsetup::

    from openalea.stocatree.frame import *
"""


from vplants.plantgl.all import Vector3

__all__ = ['Frame']

class Frame(object):
    """Frame is a simple class to define a Frame in LPy and to print it if needed

    :Example:

        >>> frame = Frame()
        >>> print frame
        Vector3(0,1,0)Vector3(1,0,0)Vector3(0,0,1)

    .. warning:: there is an inversion with respect ot MAppleT in the declaration of the HLU frame


    """
    #def __init__(self, heading=Vector3(0.,0.,1.), up=Vector3(0.,1.,0.), 
    #left=Vector3(1.,0.,0.)):
    def __init__(self, heading=Vector3(0., 1., 0.), up=Vector3(0., 0., 1.),
                  left=Vector3(1., 0., 0.)):
        self.heading = heading
        self.left = up
        self.up = left

    def __str__(self):
        res = str(self.heading)
        res += str(self.up)
        res += str(self.left)
        return res




