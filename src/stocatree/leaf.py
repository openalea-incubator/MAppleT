#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: Summary

    A module dedicated to the leaves

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.leaf import *
    :References:

        1. Colin Smith, Costes Evelyne, On the Simulation of Apple Trees
           Using Statistical and Biomechanical Principles, INRIA
           technical report, 2007

.. testsetup::

    from openalea.stocatree.leaf import *
"""

import numpy
from scipy import interpolate
sigmoid = numpy.array([ 0.00247262,  0.00669285,  0.01798621,  0.04742587,
                       0.11920292,   0.26894142,  0.5       ,  0.73105858,
                       0.88079708,  0.95257413,  0.98201379,  0.99330715,
                       0.99752738])

days = numpy.arange(0,13)

leaf_options = {'fall_probability': 0.1,
    'maturation':12,
    'mass_per_area': 0.220,
    'max_area': 0.0030,
    'min_final_area': 0.0020,
    'petiole_radius': 0.0006,
    'preformed_leaves': 8}


class Leaf(object):
    """a base class interface for leaves

    A leaf is defined by an **age**, a **mass** and a **surface** (area). Moreover,
    a **state** is chosen in ['scar', 'growing'].

    In addition, we must set the following attributes that are used to compute the
    mass :meth:`compute_mass` and area :meth:`compute_area`:

        * mass_per_area
        * maturation number of days after which the leaf does not grow anymore
        * max_area of the leaf

    Those attributes should be used to compute the area and mass of the leaf. By default
    these attributes are set to None so as to force the user to specifically provide
    their values.

    There is also a :meth:`initialisation` that may be used by derived classes to check
    that the attributes have been set correctly.

    By default, there is a setter/getter for the state.

    """
    valid_state = ['scar', 'growing']
    def __init__(self):
        self.mass = 0.               # in g
        self.area = 0.              # in m^2
        self.age = 0.                # in days
        self.max_area = None        # in m**2
        self.mass_per_area = None   # g/m**2
        self.maturation = None      # in days
        self.func_leaf_area = None
        self._state = Leaf.valid_state[0]

        self.pathogen = False


    def compute_mass(self):
        """Compute the mass of the leaf and returns its value (in kgrams)

        :return: area times mass_per_area

        .. warning:: compute_area must be called before.

        .. plot:: pyplots/leaf_mass.py

        """
        self.mass = self.area * self.mass_per_area
        return self.mass

    def compute_area(self):
        """Compute the area of the leaf and returns its value (in m**2)"""
        self.area = self.max_area
        return self.area

    def initialisation(self):
        """check that mass_per_area, maturation and max_area have been set
        to numerical values"""
        for attr in ['mass_per_area', 'maturation', 'max_area', 'state']:
            if getattr(self, attr) is None:
                raise NotImplementedError("%s is None. Set a value." % attr)


    def _get_state(self):
        return self._state
    def _set_state(self, state):
        if state in Leaf.valid_state:
            self._state = state
        else:
            raise ValueError("state must be in %s , %s provided" % (Leaf.valid_state,state))
    state = property(fget=_get_state, fset=_set_state,
                    doc="setter/getter for the state attribute given a valid state")


class AppleLeaf(Leaf):
    """A specialised leaf class for apple trees


    This class inherits methods and attributes from
    :class:`~openalea.stocatree.leaf.Leaf` and specialises
    the :meth:`compute_area` method.

    :Usage:

        >>> leaf = AppleLeaf(maturation=12., petiole_radius=0.0006)
        >>> area = leaf.compute_area(16)
        >>> mass = leaf.compute_mass()


    """
    def __init__(self, state='growing', fall_probability=0.1, maturation=12,
                 mass_per_area=0.220, max_area=0.0030, min_final_area=0.0020,
                 petiole_radius=0.0006, preformed_leaves=8):
        """**Constructor**

        The following atttributes are specific to apple tree and used as argument to the constructor.

        .. warning:: be careful with units. Should be in S.I.

        The following parametesr are used by the constructor and may be provided
        within the configuration within the L-system (see stocatree.lpy).

        ==================  ========================== ========================= ==================
        type                notation                   value                     units
        ==================  ========================== ========================= ==================
        max_area            :math:`A_{\\textrm{max}}`   :math:`30.10^{-4}`        :math:`m^2`
        min_final_area      :math:`A_{\\textrm{min}}`   :math:`20.10^{-4}`        :math:`m^2`
        mass_per_area                                  :math:`0.220`             :math:`g.m^{-2}`
        petiole_radius                                 :math:`0.6\\times10^{-3}`  :math:`m`
        fall_probability                               0.1
        maturation          :math:`T^{l}_m`            12                        days
        preformed_leaves    :math:`N_p`                8
        ==================  ========================== ========================= ==================


        :param state: see :class:`Leaf` for possible values (default is growing)
        :param fall_probability:
        :param maturation:
        :param mass_per_area:
        :param max_area:
        :param min_final_area:
        :param petiole_radius:

        """
        Leaf.__init__(self)

        self.state = state

        self.fall_probability = fall_probability         #per day
        self.maturation       = maturation         #day
        self.mass_per_area    = mass_per_area          #kg/m**2
        self.max_area         = max_area           #m^2
        self.min_final_area   = min_final_area           #m^2
        self.area_range       = self.max_area - self.min_final_area # unit:cm^2
        self.petiole_radius   = petiole_radius          #m

        self.maturity = False


        self.preformed_leaves = preformed_leaves
        self._inversed_preformed_leaves = 1. / self.preformed_leaves

        self.initialisation()

        #others (added by Han, 25-11-10)
        self.lg = 0.            # light interception (STAR)
        # Added by Han on 17-04-2011:
        self.silhouette_area = 0

    def compute_area_from_func(self, number, func_leaf_area):
        """reads a fset file (Lstudio to get growth sigmoid function

        .. deprecated:: 8981
            use compute_area instead that is a bit slower but simpler and more precise

        ::

            func_leaf_area = ReadFunction('functions.fset', 'leaf_area')
            leaf.compute_area_from_func(8, func_leaf_area)

        This function should give results equivalent to :meth:`compute_area`.
        """
        if not self.maturity:
            maturity = self.age/float(self.maturation)# dimensionless
            if (maturity > 1.0):
                self.maturiry = True
                maturity = 1.0
            relative_area = func_leaf_area.gety(maturity)
        else:
            relative_area = 1.

        # tree.Tree().preformed_leaves =8
        if number >= self.preformed_leaves:
            self.area = self.max_area * relative_area
        else:
            #self.area= relative_area * (number * self._inversed_preformed_leaves
            #                            * self.area_range + self.min_final_area)
            #Modified by Han on 28-02-2012, according to the discussion with Evelyne on 27-02-2012
            #Unlike the definition of "reduced" maximum area with Equition 21 at Page 21 in Smith's
            # report, this reduced maximum area is re-defined as: (Nt/Np)*Amax
            self.area = relative_area * number * self._inversed_preformed_leaves *self.max_area

        return self.area

    def compute_area(self, number):
        """computes the leaf area

        The growth dynamic of the leaves, as a normalised surface area relative
        to the area at maturity, has been fitted to an S-curve over twelve days,
        based on observation by Kelner [1]. The maximum surface of a neoformed
        leaf :math:`A_{\\textrm{max}}=30 \\textrm{cm}^2` [2], and the density is, as
        a mass per surface area unit is :math:`220 g/m^2` [3].

        The S-curve is hard-coded as a numpy array.

        It is assumed that the first :math:`N_p=8` metamers support preformed leaves,
        with a reduced maximum area according to their order in the growth unit
        following the equation

        .. math::

            \\frac{N_l}{N_p}(A_{\\textrm{max}}-A_{\\textrm{min}}) + A_{\\textrm{min}}

        func_leaf_area = ReadFunction('functions.fset', 'leaf_area')

        :param number: the leaf number (not used if greater than 8, the neoformed leaves)

        .. note:: age must be in days since maturity is in days.


        :references:

            1. J.J Kelner. Personnal communications on unpublished measurements of leaves (2006)
            2. Massonnet C (2004) Variabilité architecturale et fonctionnelle du système
               aérien chez le pommier (MalusDomestica Borkh.): comparaison de
               quatre cultivars par une approche de modélisation structure-fonction. PhD
               Thesis, SupAgro Montpellier University, Montpellier.
            3. J.L. Regnard, pers. comm.

        The sigmoid function that is used to compute the relative area is as follows

        .. plot:: pyplots/leaf.py
        """
        if  self.age >= self.maturation:
            relative_area = 1.
        else:
            relative_area = interpolate.interp1d(days, sigmoid)(self.age)

        if number >= self.preformed_leaves:
            self.area = self.max_area * relative_area
        else:
            #self.area= relative_area * (number * self._inversed_preformed_leaves
            #                            * self.area_range + self.min_final_area)
            #Modified by Han on 28-02-2012, according to the discussion with Evelyne on 27-02-2012
            #Unlike the definition of "reduced" maximum area with Equition 21 at Page 21 in Smith's
            # report, this reduced maximum area is re-defined as: (Nt/Np)*Amax
            self.area = relative_area * number * self._inversed_preformed_leaves *self.max_area
        print relative_area
        return self.area










