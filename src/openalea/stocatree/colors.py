#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: Summary

    A module dedicated to colors in the Lsystem

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: from openalea.stocatree.colors import *

.. testsetup::

    from openalea.stocatree.colors import *


.. todo:: to be moved to plantik in tools/colors.py

"""



__all__ = [
    'Colors',
    'colorInterface',
    'observation',
    'year',
    'reaction_wood',
    'pruning',
    'zone']





class Colors():
    """Define the indices for the colours to be used in the geometrical representation.

    This class gathers all color information related to the different rendering of
    the tree. The color indices refer to color material specified in the lpy color
    widget. The possible rendering (specified in the **config.ini** file, see
    :mod:`config_doc`) are

        * observation, :class:`observation`
        * year :class:`year`
        * zone :class:`zone`
        * reaction_wood :class:`reaction_wood`

    This rendering are defined by classes that inherit from :class:`colorInterface`.

    There are a few more independant indices:

        * background  = 0
        * error       = 1
        * fruit       = 14
        * leaf        = 15
        * autumn_leaf = 16
        * petal       = 17
        * stamen      = 18
        * bark        = 19
        * ground      = 20
        * red         = 2

    >>> color = Colors()
    >>> color.observation.get_color('small')
    5
    """
    def __init__(self):
        self.observation = observation()
        self.year = year()
        self.reaction_wood = reaction_wood()
        self.zone = zone()
        self.pruning = pruning()

        self.background   = 0
        self.error        = 1
        self.fruit        = 14

        self.petiole      = 8
        self.leaf         = 15
        self.autumn_leaf  = 16
        self.petal        = 17
        self.stamen       = 18
        self.bark         = 19
        self.ground       = 20
        self.red          = 2




class colorInterface(object):
    """An interface to associate colors to a render type

    For instance :class:`observation` associates colors to observation such as
    'short', 'medium', 'large'.

    Two compusalry methods :meth:`set_colors` and :meth:`get_color` are required.
    The setter defines a dictionary containing keywords and their corresponding color
    indices. The getter should return the color corresponding to an input keyword.
    """
    def __init__(self):
        pass

    def set_colors(self):
        """returns a dictionary of keys and correponding index color.
        """
        raise NotImplementedError

    def get_color(self):
        """returns the color index correponding to the key provided.
        It uses the dictionary set with :func:`set_colors`
        """
        raise NotImplementedError


class observation(colorInterface):
    """ Set of color codes for observation rendering

    Change the option *rendering* in the config.ini to *observations*

    ============ =============
    type         color index
    ============ =============
    dormant      2
    large        3
    medium       4
    small        5
    floral       6
    ============ =============

    inherits set_colors and get_colors from :class:`colorInterface`
    """

    def __init__(self):
        colorInterface.__init__(self)
        self.colors = self.set_colors()

    def set_colors(self):
        return {'dormant':2,
                'large':3,
                'medium':4,
                'small':5,
                'floral':6}

    def get_color(self, observation):
        if observation in self.colors.keys():
            color = self.colors[observation]
            return color
        else:
            raise ValueError("wrong observation argument (%s). Must be in %s" \
                % (observation, self.colors.keys()))



class reaction_wood(colorInterface):
    """ Set of color codes for reaction wood rendering

    rection wood is between 0 and pi. colors between 32
    and 47 are used.

    Change the option *rendering* in the config.ini to *reaction_wood*
    inherits set_colors and get_colors from :class:`colorInterface`
    """


    def __init__(self):
        colorInterface.__init__(self)
        self.colors = self.set_colors()

    def set_colors(self):
        return {}

    def get_color(self, reaction_wood):
        from scipy import pi
        color = int(((reaction_wood / pi) * (47 - 32)) + 32)
        #print reaction_wood, color
        return color


class zone(colorInterface):
    """ Set of color codes for zone rendering

    =============== ===============
    type            color index
    =============== ===============
    dormant_start   7
    small           8
    diffuse         9
    medium          10
    floral          11
    dormant_end     12
    none            13
    =============== ===============


    Change the option *rendering* in the config.ini to *zone*
    inherits set_colors and get_colors from :class:`colorInterface`
    """
    def __init__(self):
        colorInterface.__init__(self)
        self.colors = self.set_colors()

    def set_colors(self):
        return {'dormant_start':7,
                'small':8,
                'diffuse':9,
                'medium':10,
                'floral':11,
                'dormant_end':12,
                None:13
                }

    def get_color(self, zone):
        if zone in self.colors.keys():
            shoot_colour = self.colors[zone]
            return shoot_colour
        else:
            raise ValueError("wrong zone argument (%s). Must be in %s" \
                % (zone, self.colors.keys()))



class year(colorInterface):
    """ Set of color codes for year rendering

    a linear color index between 48 and 56 for each year from
    starting year onwards.

    Change the option *rendering* in the config.ini to *year*
    inherits set_colors and get_colors from :class:`colorInterface`
    """
    base = 24
    max  = 29

    def __init__(self):
        colorInterface.__init__(self)
        self.colors = self.set_colors()

    def set_colors(self):
        return {'base':24,'max':29}

    def get_color(self, year, starting_year):
        color  =int(self.colors['base'] + year - starting_year)
        color  = min(color, self.colors['max'])
        return color
        
class pruning(colorInterface):
    """
    Set a ccolor code for pruning rendering
    inherits set_colors and get_colors from :class:`colorInterface`
    In the pruning mode, the metamers are diplayed in green and the
    ones to be pruned are display in red.
    """

    def __init__(self):
        colorInterface.__init__(self)
        self.colors = self.set_colors()

    def set_colors(self):
        return {'prune':29, 'base':25}

    def get_color(self, to_prune):
        if to_prune:
            return self.colors['prune']
        else:
            return self.colors['base']


