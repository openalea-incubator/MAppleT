"""
.. topic:: Summary

    This module implements a set of functions that return random sequences
    Only :func:`generate_sequence`, :class:`Markov` and :meth:`terminal_fate`
    should be used.

    It contains quite a few harcoded data arrays that may need to be extracted

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.sequences import *

.. testsetup:: *

    from openalea.stocatree.sequences import *
"""

from openalea.sequence_analysis import HiddenSemiMarkov
from openalea.sequence_analysis._sequence_analysis import _SemiMarkovIterator, _HiddenSemiMarkov
from openalea.sequence_analysis._sequence_analysis import srand
#srand(123)

import random
import srandom
import numpy as np
#import cPickle
#import os




__all__ = [
    'DataTerminalFate',
    'terminal_fate',
    'Markov',
    'generate_trunk',
    '_non_parametric_distribution',
    '_generate_random_draw_sequence',
    'generate_floral_sequence',
    'generate_short_sequence',
    'generate_hsm_sequence',
    'generate_bounded_hsm_sequence',
    'generate_sequence',
    'length_pool'
]

class Markov():
    """class to manage all the markov and hidden semi markov sequences

    This is used within the Lpy script only. It may be used as a private class

    .. code-block:: python

        >>> markov = Markov()
        >>> markov.hsm_96_medium = HiddenSemiMarkov('../../data/fmodel_fuji_5_15_y3_96.txt')
        >>> sequence = generate_sequence('small',  markov, 1996, False)
        [[0, 0], [0, 0], [0, 0], [0, 0]]

    see generate_sequence for an explantion of the arguments

    """
    def __init__(self, maximum_length=70, minimum_length=4):
        """**constructor**

        :param max_sequence_length: the maximum length of markov sequence (default is 100)
        :param max_length: the maximum length (default is 70)
        :param min_length: the minimum length (default is 4)

        :attributes:
            * hsm_medium
            * hsm_long
            * hsm_short
            * hsm_short
            * hsm_96_medium
            * hsm_97_medium
            * hsm_98_medium
            * hsm_95_long
            * hsm_96_long
            * hsm_97_long
            * hsm_98_long
        """
        assert maximum_length <= 300
        assert maximum_length > minimum_length
        assert minimum_length > 0

        self.max_sequence_length  =  100
        self.maximum_length       =  maximum_length
        self.minimum_length       =  minimum_length
        self.hsm_medium           =  None
        self.hsm_long             =  None
        self.hsm_short            =  None
        self.hsm_medium1          =  None
        self.hsm_medium2          =  None
        self.hsm_medium3          =  None
        self.hsm_long1            =  None
        self.hsm_long2            =  None
        self.hsm_long3            =  None
        self.hsm_long4            =  None


class DataTerminalFate(object):
    """Class to deal with terminal fate probabilities

    :Example:

        >>> d = DataTerminalFate()
        >>> d._check_probabilities()
        >>> data = d.get_data_terminal_fate(1994, 'large')

    """
    """
    data = {
        (1995, 'large') : [0.500, 0.167, 0.000, 0.333],
        (1995, 'medium'): [0.000, 0.000, 0.000, 1.000],
        (1995, 'small') : [0.500, 0.000, 0.000, 0.500],
        (1995, 'floral'): [0.400, 0.000, 0.600, 0.000],
        (1996, 'large') : [0.246, 0.185, 0.000, 0.569],
        (1996, 'medium'): [0.016, 0.238, 0.032, 0.714],
        (1996, 'small') : [0.066, 0.067, 0.317, 0.550],
        (1996, 'floral'): [0.317, 0.250, 0.433, 0.000],
        (1997, 'large') : [0.351, 0.106, 0.010, 0.533],
        (1997, 'medium'): [0.123, 0.148, 0.063, 0.666],
        (1997, 'small') : [0.015, 0.094, 0.453, 0.438],
        (1997, 'floral'): [0.182, 0.249, 0.569, 0.000],
        (1998, 'large') : [0.213, 0.082, 0.000, 0.705],
        (1998, 'medium'): [0.027, 0.046, 0.016, 0.911],
        (1998, 'small') : [0.000, 0.024, 0.205, 0.771],
        (1998, 'floral'): [0.003, 0.413, 0.584, 0.000],
        (1999, 'large') : [0.100, 0.050, 0.000, 0.850],
        (1999, 'medium'): [0.000, 0.020, 0.130, 0.850],
        (1999, 'small') : [0.000, 0.000, 0.375, 0.625],
        (1999, 'floral'): [0.008, 0.325, 0.667, 0.000],
        (2000, 'large') : [0.000, 0.100, 0.000, 0.900],
        (2000, 'medium'): [0.000, 0.050, 0.050, 0.900],
        (2000, 'small') : [0.000, 0.000, 0.350, 0.650],
        (2000, 'floral'): [0.000, 0.200, 0.800, 0.000],}
    """
    #Modified by Costes on 30-05-2012
    data = {
        (1, 'large') : [0.500, 0.167, 0.000, 0.333],
        (1, 'medium'): [0.000, 0.000, 0.000, 1.000],
        (1, 'small') : [0.100, 0.100, 0.300, 0.500],
        (1, 'floral'): [0.100, 0.300, 0.600, 0.000],
        (2, 'large') : [0.246, 0.185, 0.000, 0.569],
        (2, 'medium'): [0.016, 0.238, 0.032, 0.714],
        (2, 'small') : [0.066, 0.067, 0.317, 0.550],
        (2, 'floral'): [0.317, 0.250, 0.433, 0.000],
        (3, 'large') : [0.351, 0.106, 0.010, 0.533],
        (3, 'medium'): [0.123, 0.148, 0.063, 0.666],
        (3, 'small') : [0.015, 0.094, 0.453, 0.438],
        (3, 'floral'): [0.182, 0.249, 0.569, 0.000],
        (4, 'large') : [0.213, 0.082, 0.000, 0.705],
        (4, 'medium'): [0.027, 0.046, 0.016, 0.911],
        (4, 'small') : [0.000, 0.024, 0.205, 0.771],
        (4, 'floral'): [0.003, 0.413, 0.584, 0.000],
        (5, 'large') : [0.100, 0.050, 0.000, 0.850],
        (5, 'medium'): [0.000, 0.020, 0.130, 0.850],
        (5, 'small') : [0.000, 0.000, 0.375, 0.625],
        (5, 'floral'): [0.008, 0.325, 0.667, 0.000],
        (6, 'large') : [0.000, 0.100, 0.000, 0.900],
        (6, 'medium'): [0.000, 0.050, 0.050, 0.900],
        (6, 'small') : [0.000, 0.000, 0.350, 0.650],
        (6, 'floral'): [0.000, 0.200, 0.800, 0.000],}

    def __init__(self):
        """Constructor description

        There is one constructor without arguments that simply setup
        the :attr:`codes` attributes that is  a list of possible shoots:
          1. 'large'
          2. 'medium'
          3. 'small'
          4. 'floral'

        """
        self.codes = {'large':0, 'medium':1, 'small':2, 'floral':3}

    def get_data_terminal_fate(self, year, code):
        """Returns the probabilities corresponding to a shoot code and a year

        It uses hardcoded list of probabilities such as::

            (1996, 'medium'): [0.016, 0.238, 0.032, 0.714],


        :param year: if year is less than 1994 or greater than 2000, then 2000 is chosen
        :param code: must be large, medium, small, floral

        :returns: an array containing the probabilities to have a large, medium,
            small or floral sequence.
        """
        #Terminal fate for year 0 and 1 are the same
        if year == 0:
            year = 1
        elif year < 0 or year > 6:
            year = 6

        if code in self.codes.keys():
            return self.data[(year, code)]
        else:
            raise ValueError('code must be in %s. %s provided' %
                (self.codes.keys(), code))

    def _check_probabilities(self):
        """Check that all arrays sum up to a probability of 1

        for testing usage only.

        :Example:

            >>> d = DataTerminalFate()
            >>> d._check_probabilities()
        """
        for data in self.data.values():
            assert sum(data)==1

def terminal_fate(year, observation):
    """This function returns a type of metamer (large, short, ...)


    It uses :class:`~openalea.stocatree.sequences.DataTerminalFate` class.

    :param year: is an int
    :param observation: is a string. ['large', 'medium','small', 'floral'].
        See :class:`DataTerminalFate` class documentation for details.

    :Example:

        >>> index=terminal_fate(1994, 'large')

    """
    d = DataTerminalFate()
    data = d.get_data_terminal_fate(year, observation)
    index = _non_parametric_distribution(data)
    codes = {1:'large', 2:'medium', 3:'small', 4:'floral'}
    return codes[index]


def _non_parametric_distribution(pdf):
    """Returns the index(x) at which the PDF(x) reaches random value in [0,1]

    :param pdf: The PDF function

    :Example:

        >>> res = _non_parametric_distribution([0.25,0.25,0.25,0.25])

    .. note:: The sum of PDF must be 1 (checked by this function)

    """
    assert sum(pdf)==1
    target = srandom.random(1.0)
    cumulation = 0
    i = 0
    length = len(pdf)
    while i < length and cumulation < target:
        cumulation += pdf[i]
        i += 1
    return i

def generate_hsm_sequence(hsm, sequence_length=100):
    """Generate a Hidden Semi Markov Sequence given an input transition matrix

    Used by :meth:`~openalea.stocatree.sequences.generate_sequence`

    :param hsm: A hidden semi markov instance of HiddenSemiMarkov class from VPlants.Sequence_analysis
    :param sequence_length: a length of sequence set to 100 by default

    :returns: a sequence

    """

    # Generate a Markov sequence
    #from openalea.sequence_analysis._sequence_analysis import _SemiMarkovIterator, _HiddenSemiMarkov
    #from openalea.sequence_analysis import HiddenSemiMarkov

    if type(hsm)==HiddenSemiMarkov or type(hsm)==_HiddenSemiMarkov:
        iterator =  _SemiMarkovIterator(hsm)
        simulation = iterator.simulation(sequence_length, True)
    else:
        print "expected hsm datatype. Got %s" % type(hsm)
        return None
    #processes = hsm.nb_output_process() + 1
    #used to free memory in the c++ code

    i = 0
    sequence = []
    for i in range(0, sequence_length):
        if simulation[0][i] == 6 :
            break
        sequence.append([simulation[0][i], simulation[1][i]])

    sequence.reverse()
    return sequence

def generate_bounded_hsm_sequence(hsm, lower_bound, upper_bound):
    """Returns a bouded sequence

    One problem with the Markov chains is that they may produce sequences
    with an unrealistic number of metamers. when this occurs, the generated
    sequence is thrown away and a new one is generated.

    Medium shoots are always limited to five to fifteen metamers.

    Long shoots ashrinks as the tree ages. They are therefore separated into
    subcategories: 15-25, 26-40 and over 40 metamers (41 to 70).

    The probability to select one type of shoot length depends on the year. These
    probabilities are stored within the hsm data structure

    :param hsm: a HiddenSemiMarkov instance
    :param lower_bound: int
    :param upper_bound: int

    ::

        generate_bounded_hsm_sequence(markov.hsm_long,  15, 26);

    """
    length = upper_bound + 1; # defines a max length for the sequence
    count = 0
    while length > upper_bound or length < lower_bound and count<1000:
        sequence = generate_hsm_sequence(hsm)
        length = len(sequence)
        count += 1
    if count == 1000:
        raise ValueError('to be done. max count limit reached in generate_bounded_hsm_sequence')
    if count > 100:
        print 'Warning, count in generate_bounded_hsm_sequence was large :%d' % count
    #print 'Counts hsm = ', count
    return sequence

def generate_short_sequence():
    """Generate a short sequence

    Used by :meth:`~openalea.stocatree.sequences.generate_sequence`

    :rtype: a list of sequences

    :Example:

        >>> seq = generate_short_sequence()

    .. todo:: check the relevance of this function

    """
    seq =  []
    seq.append([0, 0])
    seq.append([0, 0])
    seq.append([0, 0])
    seq.append([0, 0])

    return seq

def generate_floral_sequence():
    """Generate a floral sequence

    Used by :meth:`~openalea.stocatree.sequences.generate_sequence`

    :rtype: a list of sequences
    :Example:

        >>> seq = generate_floral_sequence()

    .. todo:: do not known what this is doing what difference with short_sequence? Seems normal behaviour
    .. todo:: original code uses s(0,12) but was not used
    """
    seq =  []
    seq.append([0, 0])
    seq.append([0, 0])
    seq.append([0, 0])
    seq.append([0, 0])

    return seq


def generate_trunk(trunk_seq='sequences.seq', select=0):
    """Generate a trunk sequence randomly selected within a list of hard-coded trunk sequences

    Used by :meth:`~openalea.stocatree.sequences.generate_sequence` only

    :param list select: the index of the selected trunk in the list of trunk sequence (default is 0).

    :Example:

        >>> deterministic_sequence = generate_trunk(select=1)

    """
    s = np.loadtxt(trunk_seq)
    print('There are {0} sequences in the files'.format(len(s)))
    assert 0 <= select < len(s)
    seq = list(s[select])
    sequence =[]
    for obs in seq:
      if obs == 9:
        break
      sequence.append([None, obs])

    #TODO comment this to get same results as in MAppleT. ???
    sequence.reverse()
    return sequence



def _generate_random_draw_sequence():
    """an alternative to the long shoot  model of the 2nd year.


    Usually not used.


    """
    max_length = 65
    number     =  9


    # an alternative to the long shoot
    # model of the 2nd year. Usually not used.


    second_year_branches = [
            [0, 0, 0, 0, 0, 3, 2, 2, 1, 1,  0, 0, 0, 0, 2, 0, 1, 1, 4, 1,  4, 4, 4, 4, 4, 4, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 4, 0, 0, 4, 0, 4,  0, 0, 4, 0, 0, 0, 0, 0, 0, 0,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3,  3, 0, 0, 0, 0, 0, 4, 4, 4, 4,  4, 3, 0, 4, 4, 4, 0, 4, 0, 4,  4, 0, 0, 4, 0, 0, 0, 2, 3, 0,  0, 0, 3, 3, 3, 3, 0, 0, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 0, 3, 0, 3,  4, 0, 1, 4, 4, 1, 0, 4, 0, 1,  4, 4, 0, 4, 4, 4, 4, 4, 4, 0,  4, 4, 0, 0, 0, 1, 0, 4, 4, 4,  0, 4, 0, 4, 0, 0, 0, 3, 0, 1,  0, 0, 0, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 4,  1, 1, 4, 3, 1, 0, 0, 4, 0, 0,  4, 0, 0, 4, 0, 4, 4, 4, 4, 4,  4, 4, 4, 0, 0, 3, 0, 0, 0, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 3, 2, 3, 0,  0, 3, 3, 0, 0, 0, 1, 2, 0, 1,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 4, 0, 4, 0, 0, 4,  0, 0, 0, 0, 0, 0, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 4, 3, 2, 4, 4, 0,  2, 0, 3, 0, 2, 0, 0, 4, 0, 4,  4, 4, 4, 4, 0, 0, 0, 0, 0, 0,  0, 4, 0, 4, 4, 0, 0, 0, 0, 4,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 3, 0, 2, 3, 0, 0, 0, 3, 2,  0, 0, 9, 9, 9],
            [0, 0, 0, 0, 1, 4, 0, 4, 0, 3,  0, 0, 1, 3, 2, 0, 0, 0, 0, 0,  0, 0, 4, 0, 0, 0, 3, 0, 0, 1,  1, 0, 0, 3, 4, 0, 4, 0, 0, 4,  0, 4, 0, 0, 0, 0, 0, 1, 0, 3,  0, 1, 0, 0, 0, 0, 1, 9, 9, 9,  9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 3, 0, 3, 3, 0,  3, 0, 0, 0, 0, 0, 0, 0, 3, 0,  1, 0, 0, 4, 0, 4, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 4, 0, 0, 1, 0, 0, 1, 1, 1,  1, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9]
        ]

    select_branch = srandom.random(number)
    i = 0
    sequence = []
    for i in range(0, max_length):
        if second_year_branches[select_branch][i] == 9:
            break
        sequence.append([None,  second_year_branches[select_branch][i]])


    sequence.reverse()

    return sequence





#// Generation of sequences from Markov chains, based directly on the work
#// of Michael Renton
def generate_sequence(obs, markov=None, year=0, second_year_draws=False,
                      trunk_seq='sequences.seq', select_trunk=0):
    """Generation of sequences from Markov chains, based directly on the work
    of Michael Renton

    if observation is
        * trunk, call :meth:`~openalea.stocatree.sequences.generate_trunk`
        * small, call :meth:`~openalea.stocatree.sequences.generate_short_sequence`
        * floral, call :meth:`~openalea.stocatree.sequences.generate_floral_sequence`
        * medium, call :meth:`~openalea.stocatree.sequences.generate_bounded_hsm_sequence` with bounded values = [5, 15]
        * large, call :meth:`~openalea.stocatree.sequences.generate_bounded_hsm_sequence`



    :param obs: the apex observation in ['trunk', 'small', 'floral', 'medium', 'large']
    :param markov: an instance of :class:`~openalea.stocatree.sequences.Markov`
    :param year: the simulation year, first year is 0
    :param second_year_draws: if True, uses the alternative `_generate_random_sequences`
        function instead of generate_bounded_hsm_sequence. (default is False).
        Can only be set to True if year=1
    :param int select_trunk: selection of trunk sequences within the list. See :func:`generate_trunk`


    :returns: a random sequence
    """
    #This fix the c++ seed at each call with a random number from the uniform law in python were the seed was also fixed
    #Therefore the successive seeds used in c++ are fixed for a given python seed allowing to reproduce trees
    srand(int(random.uniform(0,1e6)))
    
    #The "sylleptic"s to the conditions as following were added by Han on 30-04-2012
    if obs == 'trunk':
        return generate_trunk(trunk_seq=trunk_seq, select=select_trunk)
    elif obs == 'small' or obs == 'sylleptic_short':
        return generate_short_sequence()
    elif obs == 'floral':
        return generate_floral_sequence()
    elif obs == 'medium' or obs == 'sylleptic_medium':
        return generate_bounded_hsm_sequence(markov.hsm_medium,  5, 15);
    elif obs == 'large' or obs == 'sylleptic_large':
        if (second_year_draws and year== 1):
            return _generate_random_draw_sequence()
        else:
            res = length_pool(year)
            assert res in [1, 2, 3], 'Error Bad Length pool category'
            if res == 1:
                return generate_bounded_hsm_sequence(markov.hsm_long, 15, 26)
            elif res == 2:
                return generate_bounded_hsm_sequence(markov.hsm_long, 26, 41)
            elif res == 3:
                return generate_bounded_hsm_sequence(markov.hsm_long, 41, markov.maximum_length)
    else:
        raise("ERROR: A bad sequence observation (%s) was passed to generate_sequence().\n" % obs)

def generate_pruned_sequence(obs, react_pos, rank, closest_apex, farthest_apex, sons_nb, markov=None, year=0 ):
    #The pruned length is assimilated to the distance to the farthest apex

    #obs is the shoot type of the prunned shoot
    #react_pos is the position of the reacting apex from the cuting point [0,2]
    #year is the year pruned shoot creation - start date year

    #Determining the case of pruning reaction for the 3 react-pos
    # A : Succession - Succession - lower Cat
    # B : Reiteration - Succession - lower Cat
    # C : Reiteration - Reiteration - Succession
    
    
    #Case of pruning a shoot w/o branching
    #Type of shoot is generated according to the pruned length
    if closest_apex == farthest_apex:
      #ratio of pruned over total length
      pruned_ratio = 1.0*farthest_apex / (rank + farthest_apex)
      if pruned_ratio < 0.25:
        #case A
        newobs = shoot_type_react(year,obs,'A', react_pos) 
      elif pruned_ratio < 0.75:
        #case B
        newobs = shoot_type_react(year,obs,'B', react_pos) 
      else:
        #Case C
        newobs = shoot_type_react(year,obs,'C', react_pos) 

    #Case of pruning a shoot with branching
    #Then depending on the pruned length and biomass represented by the sons_nb,
    else:
      #ratio of total biomass(sons_nb) over pruned length(farthest_apex)
      bio_ratio = 1.0*sons_nb / farthest_apex
      if bio_ratio < 2:
        #case A
        newobs = shoot_type_react(year,obs,'A', react_pos) 
      if bio_ratio < 3:
        #case B
        newobs = shoot_type_react(year,obs,'B', react_pos) 
      else:
        #case C
        newobs = shoot_type_react(year,obs,'C', react_pos) 

    hsm_react_long, hsm_react_medium = pruned_hsmc(year, markov)

    if newobs == 'trunk' or newobs == 'large' or newobs == 'sylleptic_large':
      if farthest_apex > 30: 
        return generate_bounded_hsm_sequence(hsm_react_long, 41, markov.maximum_length)
      elif farthest_apex > 20:
        return generate_bounded_hsm_sequence(hsm_react_long, 26, 41)
      elif farthest_apex > 8:
        return generate_bounded_hsm_sequence(hsm_react_long, 15, 26)
      else:
        return generate_bounded_hsm_sequence(hsm_react_medium,  5, 15);

    elif newobs == 'medium'or newobs == 'sylleptic_medium':
      if farthest_apex > 5:
        return generate_bounded_hsm_sequence(hsm_react_long,  15, 26);
      else:
        return generate_bounded_hsm_sequence(hsm_react_medium,  5, 15);

    elif newobs == 'small' or newobs == 'sylleptic_short':
      return generate_short_sequence()

    elif newobs == 'floral':
      return generate_floral_sequence()

def shoot_type_react(year, pruned_shoot_type, pruning_case, react_pos):

  if pruned_shoot_type == 'trunk':
    pruned_shoot_type = 'large'
    reiteration = 'large'
    succession = 'large'
    lower_cat = terminal_fate(year, pruned_shoot_type)
  else:
    reiteration = pruned_shoot_type
    succession = terminal_fate(year, pruned_shoot_type)
    lower_cat = terminal_fate(year,terminal_fate(year, pruned_shoot_type))

  if react_pos == 0:
    if pruning_case == 'A':
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, succession))
      return succession
    else:
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, reiteration))
      return reiteration
  elif react_pos == 1:
    if pruning_case == 'C':
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, reiteration))
      return reiteration
    else:
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, succession))
      return succession
  elif react_pos == 2:
    if pruning_case == 'C':
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, succession))
      return succession
    else:
      print("reaction at pos {0} in case {1} of type {2}".format(react_pos, pruning_case, lower_cat))
      return lower_cat


"""
    if closest_apex == farthest_apex:
      if obs == 'trunk' or obs == 'large' or obs == 'sylleptic_large':
        #In case of pruned trunk, a large shoot will be generated
        if farthest_apex > 35:
          return generate_bounded_hsm_sequence(markov.hsm_long, 41, markov.maximum_length)
        elif farthest_apex > 25:
          return generate_bounded_hsm_sequence(markov.hsm_long, 26, 41)
        elif farthest_apex > 10:
          return generate_bounded_hsm_sequence(markov.hsm_long, 15, 26)
        else:
          return generate_bounded_hsm_sequence(markov.hsm_medium,  5, 15);
      elif obs == 'medium'or obs == 'sylleptic_medium':
        if farthest_apex > 5:
          return generate_bounded_hsm_sequence(markov.hsm_medium,  5, 15);
        else:
          return generate_short_sequence()
      elif obs == 'small' or obs == 'sylleptic_short':
        return generate_short_sequence()
      elif obs == 'floral':
        return generate_floral_sequence()

    #Case of pruning a shoot with branching
    #Then depending on the pruned length and biomass represented by the sons_nb,
    #shoot type may be upgraded or vigor increased by using previous year of HSMC
    else:
      print("######## Pruning reaction from shoot with branching \n \
            closest Apex: {0} - Farthest Apex: {1} - Sons nb: {2}".format(closest_apex, farthest_apex, sons_nb))

      if sons_nb >= 2*farthest_apex:
        hsm_react_long, hsm_react_medium = pruned_hsmc(year, markov)
      else:
        hsm_react_long = markov.hsm_long
        hsm_react_medium = markov.hsm_medium


      if obs == 'trunk' or obs == 'large' or obs == 'sylleptic_large':
        if farthest_apex > 30: 
          return generate_bounded_hsm_sequence(hsm_react_long, 41, markov.maximum_length)
        elif farthest_apex > 20:
          return generate_bounded_hsm_sequence(hsm_react_long, 26, 41)
        elif farthest_apex > 8:
          return generate_bounded_hsm_sequence(hsm_react_long, 15, 26)
        else:
          return generate_bounded_hsm_sequence(hsm_react_medium,  5, 15);
      elif obs == 'medium'or obs == 'sylleptic_medium':
        if farthest_apex > 5:
          return generate_bounded_hsm_sequence(hsm_react_long,  15, 26);
        else:
          return generate_bounded_hsm_sequence(hsm_react_medium,  5, 15);
      elif obs == 'small' or obs == 'sylleptic_short':
        return generate_short_sequence()
      elif obs == 'floral':
        return generate_floral_sequence()
"""

def pruned_hsmc(year, markov):
  """
  Return a long and a medium hsmc model from the year before the current one
  """

  if year in [0,1]:
      hsmc_medium = markov.hsm_medium1
      hsmc_long   = markov.hsm_long1
  elif year == 2:
      hsmc_medium = markov.hsm_medium2
      hsmc_long   = markov.hsm_long2
  elif year == 3:
      hsmc_medium = markov.hsm_medium3
      hsmc_long   = markov.hsm_long3
  else:
      hsmc_medium = markov.hsm_medium4
      hsmc_long   = markov.hsm_long4

  return hsmc_long, hsmc_medium



    #if the trunk was cut far enough from the top, generate the longest possible shoot, otherwise, depending on the pruned length, i.e. farthest apex

def length_pool(year):
    """Returns a random number according to `year`

    year should come from simulation.year
    """
    pool_1995 = [0.111, 0.222, 0.667]
    pool_1996 = [0.538, 0.346, 0.116]
    pool_1997 = [0.830, 0.170, 0.000]
    pool_1998 = [0.940, 0.060, 0.000]
    pool_1999 = [0.965, 0.035, 0.000]

    if year == 0 or year == 1:
        return _non_parametric_distribution(pool_1995)
    elif year == 2:
        return _non_parametric_distribution(pool_1996)
    elif year == 3:
        return _non_parametric_distribution(pool_1997)
    elif year == 4:
        return _non_parametric_distribution(pool_1998)
    else:
        return _non_parametric_distribution(pool_1999)


