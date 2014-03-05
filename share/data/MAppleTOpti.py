#!/usr/bin/python

#-------------------------------------------------------------------------------
# Name:         MAppleTOpti
# Purpose:      A script for launching 1 MAppleT simulation.
# Note:         launch process should take the genetic parameters as argument
#               and return the performance value, i.e. whoel tree STAR
# Author:       Da Silva
# Created:      03/06/2013
# Copyright:    (c) Da Silva 2013
# Licence:      CeCill/LGPL
#-------------------------------------------------------------------------------

from openalea.vpltk.qt import *

import openalea.lpy as lpy
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree import get_shared_data

import pylab as p
import sys, getopt

"""
  self.lsys = lpy.Lsystem(self.confp.general.filename, {"options":self.confp})

  self.lsys = lpy.Lsystem(self.confp.general.filename, {"options":self.confp, 'PostDraw':self.myPostDraw})
  self.lsys.context()["current_experiment"] = self.confp.stocatree.select_trunk
  self.lsys.animate()    
  self.lsys.iterate()    

  self.confp.__dict__[section].__dict__[var] = val
  self.confp.config.set(section, var, val)
  self.lsys.context()['options'].__dict__[section].__dict__[var] = val


"""
lsystemFile = 'MAppleT.lpy'
iniFile = 'MAppleT_Opti.ini'

def main(argv):

  try:
     opts, args = getopt.getopt(argv,"hspi:l:a:r:x:",["help","savesimu","pix","internodelenght=","leafarea=","branchingangle=","apexradius=","optidx="])
  except getopt.GetoptError:
     print 'MAppleTOpti -h to get some help'
     sys.exit(2)

  #conf = ConfigParams(iniFile)
  #conf.internode.max_length = 0.03 # max internode length [m]
  #conf.leaf.max_area = 0.003 # max leaf area [m2]
  #conf.tree.branching_angle = 45 # branching angle [degree]
  #conf.apex.maximum_size = 0.003 # radius of apex [m]

  savesimu  = False # saving simu and pgl scene
  pix       = False # saving a picture of the tree
  length    = 0.03  # max internode length [m]
  area      = 0.003 # max leaf area [m2]
  angle     = 45    # branching angle [degree]
  diameter  = 0.003 # radius of apex [m]
  optidx    = 0     # idx of optimization experiment: 0 = None, -1 = created from variable ortherwise any #

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print "MAppleTOpti.py will be launched with the following default values :\n \
             \t Scene and simulation will not be saved \n \
             \t Picture of the 3D scene will not be taken \n \
             \t internode length  = 0.03 [m]   \n \
             \t max leaf area     = 0.003 [m2] \n \
             \t branching angle   = 45 [degree]\n \
             \t apex max radius   = 0.003 [m]  \n \
             \t idx of optimization experiment is not set \n \
             unless below options are used :   \n \n \
             -s : will save the scene and simulation (similar to  --savesimu)\n \
             -p : will take a picture of the scene (similar to --pix)\n \
             -i : specify the internode length in [m] (similar to --internodelength) \n \
             -l : specify the maximum leaf area in [m2] (similar to --leafarea) \n \
             -a : specify the branching angle in [degree] (similar to --branchingangle) \n \
             -r : specify the maximum apex radius in [m] (similar to --apexradius) \n \
             -x : specify the index to be used to identify experiment [0 and -1 are reserved values] (similar to --optidx) \n "
      sys.exit()
    elif opt in ('-s', "--savesimu"):
      savesimu = True
      print "Simulation and 3D scene from MAppleT will be saved"
    elif opt in ('-p', "--pix"):
      pix = True
      print "Picture of the 3D scene from MAppleT will be taken"
    elif opt in ('-i', "--internodelength"):
      length = float(arg)
      print "Starting MAppleT with modified internode length to {0} [m]".format(arg)
    elif opt in ("-l", "--leafarea"):
      area = float(arg)
      print "Starting MAppleT with modified max leaf area to {0} [m2]".format(arg)
    elif opt in ("-a", "--branchingangle"):
      angle = float(arg)
      print "Starting MAppleT with modified branching angle to {0} [degree]".format(arg)
    elif opt in ("-r", "--apexradius"):
      diameter = float(arg)
      print "Starting MAppleT with modified max apex radius to {0} [m]".format(arg)
    elif opt in ("-x", "--optidx"):
      optidx = int(arg)
      print "Starting MAppleT with modified experiment idx to {0}".format(arg)
   
  launchOptions(savesimu, pix, length, area, angle, diameter, optidx)


def launchOptions(savesimu, pix, length, area, angle, diameter, optidx):
  
  conf = ConfigParams(iniFile)

  conf.internode.max_length = length    # max internode length [m]
  conf.leaf.max_area        = area      # max leaf area [m2]
  conf.tree.branching_angle = angle     # branching angle [degree]
  conf.apex.maximum_size    = diameter  # radius of apex [m]
  
  conf.output.savescene     = savesimu  # wether to save the scene and simulation
  conf.output.saveimage     = pix       # wether to take a picture of the scene
  conf.output.opti_idx      = optidx    # idx to identify the optimization experiment

  lsys = lpy.Lsystem(lsystemFile, {"options":conf})
  lsys.animate()    

def optiPlan(csvfile, nb=None):
  params = p.loadtxt(csvfile, skiprows=1)
  if nb != None:
    star, angle, length, diameter, area = params[nb]
    launchOptions(length, area, angle, diameter)
  else:
    print "Not looping yet"
        

if __name__ == "__main__":
  #print "############ Main was called"
  main(sys.argv[1:])





