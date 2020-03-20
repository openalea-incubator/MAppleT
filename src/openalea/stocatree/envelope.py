import cPickle
import openalea.fractalysis.fractutils as fruti
import openalea.fractalysis.light as lit
#from openalea.fractalysis import light as lit
import openalea.plantgl.all as pgl
import os.path as op
from os import getcwd
from numpy import sin, radians, array
import os
#The "eid" argument was added by Han on 19-03-2012, namely exp_id
#The "growth_date" argument was added by Han on 19-03-2012
def IntegratedMultiScaleStar(treename, ctrd_scene, scale_dict_list, growth_date, distrib=[['R','R','R'],['A','R','R'],['A','A','R'], ['A','A','A']], save_pth = getcwd(), eid=0):

  #os.chdir(save_pth)

  """
  Compute the integrated star over the 46 skyturtle directions for each scenario and save it to a csv file using the semi colon ; as separator
  Parameters are:
  - treename = name used to create a folder that will contain output from computeDir and also identify the line on the generated csv file
  - ctrd_scene = the plantGL scene
  - scale_dict_list = the list of scale dictionaries
  - distrib = the list of scenario to compute
  - save_pth = the path to save the outputs, default to current dir
  """
  pgl.Viewer.setBatchMode(True)
  scc=fruti.centerScene( ctrd_scene )
  ss=lit.ssFromDict(treename, scc, scale_dict_list, "CvxHull")

  myresult = {}
  #for i in range(1,47):
  for i in range(1,47):
    res = ss.computeDir(skt_idx=i, distrib=[['R','R','R'],['A','R','R'],['A','A','R'], ['A','A','A']])
    az,el,wg = lit.sunDome.getSkyTurtleAt(i)
    wg2 = wg*sin(radians(el))

    #Added by Han on 19-03-2012

    sc1=ss.genScaleScene(1)
    sc1_name = str(eid)+"_env_1_"+str(growth_date)
    sc1.save(sc1_name+".bgeom")
    sc2=ss.genScaleScene(2)
    sc2_name = str(eid)+"_env_2_"+str(growth_date)
    sc2.save(sc2_name+".bgeom")
    sc3=ss.genScaleScene(3)
    sc3_name = str(eid)+"_env_3_"+str(growth_date)
    sc3.save(sc3_name+".bgeom")
    sc4=ss.genScaleScene(4)
    sc4_name = str(eid)+"_env_4_"+str(growth_date)
    sc4.save(sc4_name+".bgeom")
    """
    sc1=ss.genScaleScene(1)
    sc1.save(str(eid)+"_env_1"+str(growth_date)+".bgeom")
    sc2=ss.genScaleScene(2)
    sc2.save(str(eid)+"_env_1"+str(growth_date)+".bgeom")
    sc3=ss.genScaleScene(3)
    sc3.save(str(eid)+"_env_1"+str(growth_date)+".bgeom")
    sc4=ss.genScaleScene(4)
    sc4.save(str(eid)+"_env_1"+str(growth_date)+".bgeom")
    """

    tmplist = myresult.get('weight', [])
    tmplist.append(wg2)
    myresult['weight'] = tmplist
    tmplist = myresult.get('turbid', [])
    tmplist.append(res['Star_turbid'])
    myresult['turbid'] = tmplist
    for d in distrib:
      tmplist = myresult.get(str(d), [])
      tmplist.append(res['Star_'+str(d)])
      myresult[str(d)] = tmplist

  sav = op.join(save_pth, 'IntegratedMultiScaleStar.csv')
  if not op.isfile(sav):
    f = open(sav, 'a')
    #Modified by Han on 19-03-2012 for the addition of "Growth_Date"
    header = 'Grwoth_Date;Experiment_ID;Turbid'
    for d in distrib:
      header += ';'+str(d)
    header +='\n'
    f.write(header)
    f.close()

  #print myresult
  soc = array(myresult['weight'])
  f = open(sav, 'a')
  #Modified by Han on 19-03-2012 for the addition of "Growth_Date"
  row = str(growth_date) + ';' + str(treename) + ';' + str((array(myresult['turbid'])*soc).sum())
  for d in distrib:
    row += ';'+str((array(myresult[str(d)])*soc).sum())
  row += '\n'
  f.write(row)
  f.close()
