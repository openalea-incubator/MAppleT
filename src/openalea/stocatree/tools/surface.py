#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""Surface module

.. module:: surface

.. topic:: Summary

    Aliases to surface used within stocatree (petal/leaf/ground)

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$

.. testsetup::

    from openalea.stocatree.tools.surface import *

"""
from openalea.stocatree import get_shared_data
from openalea.plantik.tools.surface import createSurface

__all__ = ['leafSurface','petalSurface','groundSurface']

def leafSurface(u_stride=6, v_stride=6):
    """read leaf_surface.s file and return the surface associated

    :param int u_stride: stride in u direction (default is 6)
    :param int v_stride: stride in v direction (default is 6)

    >>> leaf = leafSurface(6, 12)
    """
    s = createSurface(get_shared_data('leaf_surface.s'), u_stride, v_stride)
    s.name = 'leaf'
    return s

def groundSurface(u_stride=6, v_stride=6):
    """read ground_surface.s file and return the surface associated

    :param int u_stride: stride in u direction (default is 6)
    :param int v_stride: stride in v direction (default is 6)

    >>> ground = groundSurface(6, 12)
    """
    s = createSurface(get_shared_data('ground_surface.s'), u_stride, v_stride)
    s.name = 'ground'
    return s


def petalSurface(u_stride=6, v_stride=6):
    """read petal_surface.s file and return the surface associated

    :param int u_stride: stride in u direction (default is 6)
    :param int v_stride: stride in v direction (default is 6)

    >>> petal = petalSurface(6, 12)
    """
    s = createSurface(get_shared_data('petal_surface.s'), u_stride, v_stride)
    s.name = 'petal'
    return s


