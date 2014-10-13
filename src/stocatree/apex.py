#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: apex.py summary

    Module dedicated to apices

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Usage: >>> from openalea.stocatree.apex import *
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $

.. testsetup::

    from openalea.stocatree.apex import *
    a = apex_data()
"""

#import physics
from physics import Frame

__all__ = ['apex_data']

apex_options = {'terminal_expansion_rate':0.00002,
            'minimum_size':0.00075,
            'maximum_size':0.006}

markov_options = {'maximum_length':70,
            'minimum_length':4}


class apex_data(object):
    """An apex class to be used in stocatree

    :Usage:

    First, you need to create an instance of the apex

    >>> a = apex_data()

    There are several default parameters described in the constructor
    documentation. You can now access to the attributes such as the
    **observation** using the getter :func:`get_observation`. There is
    also a setter for the observation :func:`set_observation`

    >>> a.get_observation()
    'trunk'

    :possible observations:

    ================ ======================================== ================================
    observation Code        Type of shoot from a bud                 Number of metamers
    ================ ======================================== ================================
    dormant          dormant bud (no shoot grow)
    large            long shoot                               16-70
    medium           medium shoot                             5-15
    small            short shoot                              4
    floral           inflorescence                            4 followed by a sylleptic shoot
    trunk            on the main trunk
    new_shoot        not yet determined
    ================ ======================================== ================================

    The other important attribute is the **radius**.

    >>> a.radius
    0.0

    There is a **maximum target radius** that is defined by the
    :func:`max_terminal_radius_target`.

    Each apex is associated to an HLU :class:`~openalea.stocatree.physics.Frame` to
    keep track of its orientation in the scene.


    Finally, an apex is part of a sequence.

    .. seealso:: :func:`generate_sequence`, :func:`terminal_fate`

    """

    #states = ['dormant', 'large', 'medium', 'small', 'floral', 'trunk',
    #         'new_shoot']
    #The content of "states" were changed by Han on 09-05-2012
    states = ['dormant', 'large', 'medium', 'small', 'floral', 'trunk',
              'new_shoot', 'sylleptic_small', 'sylleptic_medium', 'sylleptic_large']

    def __init__(self, hlu=Frame(), observation='trunk',
                 terminal_expansion_rate=0.00002, minimum_size=0.00075,
                 maximum_size=0.006, minimum_length=4, maximum_length=70,
                 expansion_period=300, target_radius=0.006, sylleptic=False):
        """
        The arguments "expansion_period" and "target_radius" were added by Han
        on 14-04-2011.
        """
        """**Constructor**

        The following attributes are set

        :param hlu: an instance of :class:`~openalea.stocatree.physics.Frame`
        :param observation: a string defining the apex's state (default is 'trunk')
        :param terminal_expansion_rate: default is 0.00002 meters per day
        :param minimum_size: default is 0.00075 meters
        :param maximum_size: default is 0.006 meters
        :param minimum_length: minimum length of the sequence (default 4)
        :param maximum_size: maximum length of the sequence (default is 70)

        :attributes:

        =========================== =============== ============
        type                        Default value   units
        =========================== =============== ============
        :attr:`radius`              0.              meters
        :attr:`target_radius`       0.              meters
        parent_observation          'new_shoot'
        trunk                       False
        sequence_position           0
        sequence                    None
        =========================== =============== ============


        """
        self.sequence_position  = 0
        self._observation = None
        self.set_observation(observation)
        self.parent_observation = 'new_shoot'
        self.hlu = hlu
        if observation == 'trunk':
            self.trunk = True
        else:
            self.trunk = False
        self.sequence = None

        self.radius = 0.
        self.target_radius = 0.
        # The expansion_period attribute was added by Han on 14-04-2011
        self.expansion_period = expansion_period
        self.expansion_days_counter = 0

        # sequence length
        self.sequence_minimum_length = minimum_length
        self.sequence_maximum_length = maximum_length
        assert self.sequence_maximum_length > self.sequence_minimum_length
        self.sequence_length_range = float(self.sequence_maximum_length
                                           - self.sequence_minimum_length)

        # expansion rate of the radius
        self.terminal_expansion_rate = terminal_expansion_rate

        # define the radius size
        self.maximum_size = maximum_size
        self.minimum_size = minimum_size
        self.radius_range = maximum_size - minimum_size

        # This is used to record the parent unit id
        # Added by Han
        self.parent_unit_id = 0

        # This is used to record the parent branch id (first-order branch)
        # Added by Han on 02-05-2011
        self.parent_fbr_id = 0

        # Since only one tree is investigated at this stage, there is no need to
        # update this parameter:
        self.parent_tree_id= 0

        #Added by Han on 29-05-2012
        #The value will be set to be the same with the current year once a
        #growth unit (sequence) is fully generated
        #This is to avoid there are two growth units at the same year
        self.year = 1993

        #Added by Han on 06-07-2012
        #This is to avoid "1,2,3,4" growth units to be syllpetic at the first year
        self.sylleptic = sylleptic

        #Flag to show that this apex was generated as a reaction to pruning
        self.from_pruning = False
        #Information related to pruning reaction
        self.rank = 0
        self.react_pos = 0
        self.closest_apex = 0
        self.farthest_apex = 0
        #the cumulated sum of metamers sons
        self.sons_nb = 0

    def set_observation(self, observation):
        """set the apex observation

        :param observation: a valid observation

        observation values are given in the class documentation, or by typing::

            >>> import openalea.stocatree.apex as apex
            >>> apex.apex_data.states
            ['dormant', 'large', 'medium', 'small', 'floral', 'trunk', 'new_shoot']

        """

        if observation in apex_data.states:
            #if observation == 'sylleptic_small':
            #    self._observation = 'small'
            #elif observation == 'sylleptic_medium':
            #    self._observation = 'medium'
            #elif observation == 'sylleptic_large':
            #    self._observation = 'large'
            #else:
            #    self._observation = observation
            self._observation = observation
        else:
            raise ValueError("observation must be in %s , %s provided"
                             % (apex_data.states, observation))

    def get_observation(self):
        """returns the current apex observation"""
        return self._observation

    def get_observation_from_sequence(self):
        """return observation corresponding to the current position"""
        index = self.sequence[self.sequence_position][1]
        if index == 0:
            #self.sylleptic = False
            return 'dormant'
        elif index == 1:
            #self.sylleptic = False
            return 'large'
        elif index == 2:
            #self.sylleptic = False
            return 'medium'
        elif index == 3:
            #self.sylleptic = False
            return 'small'
        elif index == 4:
            #self.sylleptic = False
            return 'floral'
        #The following indexes were added by Han on 30-04-2012
        elif index == 5:
            #self.sylleptic = True
            return 'sylleptic_small'
            #return 'small'
        elif index == 6:
            #self.sylleptic = True
            return 'sylleptic_medium'
            #return 'medium'
        elif index == 7:
            #self.sylleptic = True
            return 'sylleptic_large'
            #return 'large'
        else:
          #should never reach this line, however old sequences may contain 9s
          return 'dormant'

    def max_terminal_radius_target(self):
        """Set the max terminal radius :attr:`target_radius`

        The radius range is defined by the minimum and maximum apex radius.

        .. math::

            r_{\\textrm{range}} = \\left(r_{\\textrm{max}} - r_{\\textrm{min}} \\right)

        The position is also defined within a valid range

        .. math::

            \\textrm{Position}_{\\textrm{range}} = \\left(\\textrm{Posistion}_{\\textrm{max}} - \\textrm{Position}_{\\textrm{min}} \\right)

        Therefore the maximum terminal apex range is defined by

        .. math::

            r_{\\textrm{target}} = r_{\\textrm{min}} + r_{\\textrm{range}} \\times (\\frac{ \\textrm{Position} - \\textrm{Position}_{\\textrm{min}})}{\\textrm{Position}_{\\textrm{range}}}

        :Hypothesis: a terminal apex expands to a maximum size based on the number
         of leaves in a shoot (i.e., position)

        """
        assert self.sequence_position >= self.sequence_minimum_length
        res = self.minimum_size + self.radius_range * (self.sequence_position
                    - self.sequence_minimum_length) / self.sequence_length_range
        self.target_radius = res


    def terminal_expansion(self, dt):
        self.radius = self.radius + self.terminal_expansion_rate * dt
        self.expansion_days_counter += dt

    #Added by Han on 11-07-2012, to be used as a condition to control the first-year sylleptic growth from trunk
    def trunk_sylleptic(self):
        index = self.sequence[self.sequence_position][1]
        print "==============================================================="
        if index == 0:
            return False
        elif index == 1:
            return False
        elif index == 2:
            return False
        elif index == 3:
            return False
        elif index == 4:
            return False
        #The following indexes were added by Han on 30-04-2012
        elif index == 5:
            return True
            #return 'sylleptic_short'
        elif index == 6:
            return True
            #return 'sylleptic_medium'
        elif index == 7:
            return True
            #return 'sylleptic_large'
        #should never reach this line
