#-------------------------------------------------------------------------------
# Name:         launchSimu
# Purpose:      A script for launching 1 MAppleT simulation.
# Note:         Understanding the launch process and ease simulation launching for
#               development and debugging
# Author:       Da Silva
# Created:      03/06/2013
# Copyright:    (c) Da Silva 2013
# Licence:      CeCill/LGPL
#-------------------------------------------------------------------------------

from openalea.vpltk.qt import *

import openalea.lpy as lpy
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree import get_shared_data
#import csv as pycsv
#from multiprocessing import Process, Pool
#gc is garbage collector
#import gc
#import cPickle
#import sys
import os
#import time
from multiprocessing import Pool

#pleqplan.csv is a file containing the experimental plan, i.e. the set of input parameters for each simulation
#plan structure is:
# plan number, branching angle, internode max length, apex diameter, max leaf area
#in case of Topology variation, 2 additional values at the end of each plan:
#Sequence and combination (similar for now, combination should be used when 
#combining both geometry and topology variations

#The initial trunk sequences are pickled in sequences.seq, there are 239 of them.
#While the trunk them selves are of different sizes, all sequences are 112 length
#0 Dormant
#1 Large
#2 Medium
#3 Small
#4 Floral
#5 Sylleptic short
#6 Sylleptic medium
#7 Sylleptic large
#8 Not used
#9 End of sequence, used to fill sequence up to max length (112)

def launchMAppleT(seqid):

  for i in range(5):
    conf = ConfigParams("MAppleT_FSPM.ini") # generate a ConfigParam object from the ini file
    #Adding the experimental parameter to the conf object
    conf.apex.maximum_size = 0.003 # radius of apex [m]
    conf.leaf.max_area = 0.003 # max leaf area [m2]
    conf.internode.max_length = 0.03 # max internode length [m]
    conf.tree.branching_angle = 45 # branching angle [degree]
    
    
    #conf.general.end_year = '1994-06-30'
    conf.stocatree.select_trunk = seqid # initial trunk sequence from sequences.seq [0-238]
    conf.output.opti_idx = str(seqid)+"_"+str(i)

    #define the lsystem file to use and to define the "options" of the lsystem context
    lsys = lpy.Lsystem("MAppleT.lpy", {"options":conf})
    lsys.animate()    



idtodo = [50, 78, 107, 115, 121, 123, 124, 127, 128, 130, 131, 133, 134, 136, 142, 144, 145, 150, 151, 157, 158, 160, 175, 182, 185, 190, 191, 193, 194, 197, 198, 199, 204, 205, 206, 207, 208, 217, 227, 231, 232, 233, 234, 235, 238]

pbTrees=[137,170,176,184]

if __name__ == '__main__':
    pool = Pool(processes=1)              # start 4 worker processes
    #result = pool.apply_async(f, [10])    # evaluate "f(10)" asynchronously
    #print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
    #pool.map(launchMAppleT, [164,165,166,167])          # prints "[0, 1, 4,..., 81]"
    pool.map(launchMAppleT, [41] ) #, 79, 171, 41])          # prints "[0, 1, 4,..., 81]"
    #print "loaded"
