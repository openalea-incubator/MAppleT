#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: simulation.py summary

    Classes to create simulation protocols

    :Code: mature
    :Documentation: draft
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $

.. testsetup::

    from openalea.plantik.simulation.simulation import *
    from openalea.stocatree.tools.simulation import *
"""

from openalea.plantik.simulation.calendar import Calendar, Events, Event
from openalea.plantik.simulation.simulation import SimulationInterface
#from openalea.stocatree.tools.read_function import ReadFunction
from read_function import ReadFunction
import datetime


class RotationConvergence():
    steps = 2  # // Runge-Kutta order 2
    step  = 1.0 / steps



class SimulationStocatree(SimulationInterface):
    def __init__(self, dt=1, starting_date=2000, ending_date=2010,seed=1163078257):
        SimulationInterface.__init__(self, dt=dt, starting_date=starting_date, ending_date=ending_date)


        mydt = datetime.timedelta(dt)
        self.events.add_event('bud_break',
                              datetime.datetime(starting_date, 4, 15),
                              duration=datetime.timedelta(0))
        self.events.add_event('new_cambial_layer',
                              datetime.datetime(starting_date, 5, 15),
                              duration=mydt)
        self.events.add_event('pre_harvest',
                              datetime.datetime(starting_date, 10, 29),
                              duration=mydt)
        self.events.add_event('harvest',
                              datetime.datetime(starting_date, 10, 30),
                              duration=mydt)
        self.events.add_event('autumn',
                              datetime.datetime(starting_date, 11, 1),
                              duration=datetime.timedelta(45))
        self.events.add_event('leaf_fall',
                              datetime.datetime(starting_date, 11, 15),
                              duration=datetime.timedelta(45))
        #to make sure there are no remaining leaves for next year
        self.events.add_event('leaf_out',
                              datetime.datetime(starting_date, 12, 25),
                              duration=mydt)
        self.phase            = 0 #initialisation
        self.error            = False # purpose of that attribut is not clear, seems not used
        self.seed             = seed
        self.base_dt          = dt
        self.number           = 0
        self.rotation_convergence = RotationConvergence()
        self.harvested = False    # purpose of that attribut is not clear, seems not used

        #---------------------------------------------------------------------#
        # Here comes element that should be saved in order to be able to      #
        # restart the simulation from a saved point                           #
        #---------------------------------------------------------------------#

        # the tree representation as a lstring should be set just before saving to avoid duplication
        # and be deleted after loading to continue simulation
        self.lstring          = None    
        
        # Data structure that store output
        # should probably replaced and/or cleaned
        self.data             = None

        # Tree is the unique instance that represent the tree and store tree status
        self.tree             = None

        # Budbreak date is also saved in case the simulation is saved and reloaded
        # between 01/01 when budbreak date is calculated and the calculated date
        self.bud_break        = None

        
    def load_save(self, lstr, dat, tr, bbreak):
      """
      Gather all simulation element that are necessary to be able to reload it
      before being serialized
      """
      self.lstring = lstr
      self.data = dat
      self.tree = tr
      self.bud_break = bbreak      

    def unload_save(self):
      """
      Free some memory by setting some attributs back to None
      """
      self.lstring          = None    
      self.data             = None
      self.tree             = None


    def func_leaf_area_init(self, filename='functions.fset', func_name='leaf_area'):
        """read the functions.fset once for all the metamers"""
        self.func_leaf_area = ReadFunction(filename, func_name)



