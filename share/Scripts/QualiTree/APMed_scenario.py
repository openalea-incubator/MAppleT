#!/usr/bin/python
 
from openalea.stocatree.export import export2qualitree
import openalea.plantgl.all as pgl 

import os.path as op

date = '1998-05-15'
variety = 'fuji'
sla = 0.01155
specific_weight = 0.40e6
fruit_dwc = 0.153
srr = 4.55

def Fujix(num):
  """
  Getting the necessary inputs for 1 Fuji Tree
  """

  dirpth = "/home/ddasilva/dev/QualiTree/Fuji/Fuji{0}_1998_5_15/".format(num)
  mtgpth = op.join(dirpth, "{0}.mtg".format(num))
  geompth = op.join(dirpth, "{0}.bgeom".format(num))

  scene = pgl.Scene(geompth)
  lvs = pgl.Scene([ sh for sh in scene if sh.appearance.getName() == "Color_15"])

  assert op.isdir(dirpth)
  assert op.isfile(mtgpth)
  assert op.isfile(geompth)

  return dirpth, mtgpth, lvs

  
def scenario(fuji_num, pf_type='default', scenar='default'):
  dirpth, mtgpth, lvs = Fujix(fuji_num)
  export2qualitree(save_pth = dirpth, mtg_file_path = mtgpth, leaf_scene = lvs, nom_arbre = "MAppleT_Fuji{0}_{1}".format(fuji_num,scenar), date = date, variete = variety , SLA = sla, densite_MS_rameaux = specific_weight, TMS_fruits = fruit_dwc, SR = srr, userEllipse=True, pf_type=pf_type)
