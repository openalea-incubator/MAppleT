#Compared with the previous version, the "leaf_sate" has been used in this one
#to decide whether a leaf is in the scene. This is because, in the scene, as
#long as there leaf growth state is "growing", there is a shape there even if
#the leaf area is 0.

#import sys
#from amlPy   import *
#from openalea.plantgl.all import *
#import cPickle
#from PlantGL import *

import glob, os, time, cPickle, gc
from openalea.stocatree.file_tools import File_Index, Mtg_Processing
from openalea.stocatree.data_process import Group, Statistics
#from openalea.stocatree.interception import STAR, Envelope
from openalea.stocatree.rw_tools import Ensure_dir
from multiprocessing import Process, Pool
from openalea.plantgl.all import Viewer, Scene
from openalea.stocatree.envelope import IntegratedMultiScaleStar

class Postpara_Interception(object):
    def __init__(self,\
                    general_directory=".\\PararunResults\\",\
                    sub_directory_names=[\
                                            "1994_6_30",\
                                            "1995_6_30",\
                                            "1996_6_30",\
                                            "1997_6_30",\
                                            "1998_6_30"\
                                        ],\
                    cpu_number=4):
        self.general_directory = general_directory
        self.sub_directory_names = sub_directory_names
        self.cpu_number = cpu_number
        self.mtg_files = {}
        self.bgeom_files = {}
        self.lpk_files = {}

        for d in self.sub_directory_names:
            indx = File_Index(self.general_directory+d+"\\")
            self.mtg_files.update({d:indx.file_dic("mtg")})
            self.bgeom_files.update({d:indx.file_dic("bgeom")})
            self.lpk_files.update({d:indx.file_dic("lpk")})

        """
        self.mtg_files will look like:
            {
                "1994_6_30":
                    {
                        "1" : "e:\\...\\1.mtg",
                        "2" : "e:\\...\\2.mtg"
                        ...
                    },
                "1995_6_30":
                    {
                        "1" : "e:\\...\\1.mtg",
                        "2" : "e:\\...\\2.mtg"
                        ...
                    },
                "1996_6_30":
                    {
                        "1" : "e:\\...\\1.mtg",
                        "2" : "e:\\...\\2.mtg"
                        ...
                    }
            }
        the similar to self.bgeom_files
        """
        #Note: the keys of self.mtg_files and self.bgeom_files are expected
        #to be the same, otherwise there could be errors.

        #A list to record unsuccessful experiment ids
        self.unsccfl_exps = []

        self.exp_nbr = len(self.mtg_files[self.mtg_files.keys()[0]].keys())
        self.exp_groups = [[]] * self.cpu_number
        self.expnbr_per_grp = int(round(float(self.exp_nbr)/self.cpu_number))
        #The index/id of the last item of self.exp_groups
        lid = len(self.exp_groups)-1
        #Initialise self.exp_groups except its last item
        #Note: the exp_id varies from 0 to exp_nbr-1 (not 1 to exp_nbr)
        for i in range(lid):
            self.exp_groups[i] = range(i*self.expnbr_per_grp, (i+1)*self.expnbr_per_grp)
        #Initialise the last item of self.exp_groups
        self.exp_groups[lid] = range(lid*self.expnbr_per_grp, self.exp_nbr)

    def run(self, exp_id, batch_dir):
        for date, experiment in self.lpk_files.iteritems():
            ##experiment[str(exp_id)] is the name (including directory) of the
            ##corresponding mtg file
            #mtgp = Mtg_Processing(experiment[str(exp_id)])
            #lstring = mtgp.crt_pseudo_lstring()

            pl = open(experiment[str(exp_id)])
            lstring = cPickle.load(pl)
            pl.close()


            fbr_id_add = 100000000
            unit_id_add = 1000000
            id_dicts = [{},{},{}]
            print len(lstring)

            for i in range(len(lstring)):
                if lstring[i][0].parent_tree_id == 0:
                    new_fbr_id = lstring[i][0].parent_fbr_id + fbr_id_add
                    new_unit_id = lstring[i][0].parent_unit_id + unit_id_add
                    #If this element has not been processed yet
                    #Note that id_dicts[2] is a list, so do not use
                    #      i not in id_dicts[2].values
                    #ALSO: the selected metamer should have a leaf!
                    #OTHERWISE it could cause errors when using envelope
                    if i not in id_dicts[2] and lstring[i][0].leaf_area > 0:
                        ##If the growth unit is a floral one, then consider
                        ##it as part of the one before it
                        #if lstring[i][0].parent_observation == "floral":
                        #    new_unit_id -= 1
                        #If the new_unit_id has already been there
                        if new_unit_id in id_dicts[2].keys():
                            #Then only add the metamer id
                            id_dicts[2][new_unit_id].append(i)
                        #If the new_unit_id is not there
                        else:
                            id_dicts[2].update({new_unit_id:[i]})
                            #If the new_fbr_id has already been there
                            if new_fbr_id in id_dicts[1].keys():
                                #Then only add the new_unit_id
                                id_dicts[1][new_fbr_id].append(new_unit_id)
                            else:
                                id_dicts[1].update({new_fbr_id:[new_unit_id]})
                                #If the tree has been there already
                                if lstring[i][0].parent_tree_id in id_dicts[0].keys():
                                    #Then only add the new_fbr_id
                                    id_dicts[0][0].append(new_fbr_id)
                                else:
                                    id_dicts[0].update({0:[new_fbr_id]})
                    else:
                        continue
                else:
                    continue


            #This is the remove the cases where one growth
            #unit only has one leaf
            for k in id_dicts[2].keys():
                if len(id_dicts[2][k]) <= 1:
                    print k
                    id_dicts[2].pop(k)
                    for t in id_dicts[1].keys():
                        if k in id_dicts[1][t]:
                            id_dicts[1][t].remove(k)
                            if len(id_dicts[1][t]) == 0:
                                id_dicts[1].pop(t)
                                for r in id_dicts[0].keys():
                                    if t in id_dicts[0][r]:
                                        id_dicts[0][r].remove(t)
                                        if len(id_dicts[0][r]) == 0:
                                            id_dicts[0].pop(r)

            print "-----------------------------------------------------"


            idd_pk = open(batch_dir+str(exp_id)+"_"+date+"_"+".idpk", "w")
            cPickle.dump(id_dicts,idd_pk,0)
            idd_pk.close()

            idd_print = open(batch_dir+str(exp_id)+"_"+date+"_"+".txt", "w")
            for d in id_dicts:
                for k,v in d.iteritems():
                    idd_print.write("{0}------{1}\n\n".format(k,v))
                idd_print.write("####################\n\n")
            idd_print.close()


            scene = self.bgeom_files[date][str(exp_id)]
            sc = Scene(scene)
            experiment_date = time.strftime("%d/%m/%Y %I:%M:%S", time.localtime(os.path.getmtime(self.bgeom_files[date][str(exp_id)])))
            IntegratedMultiScaleStar(str(exp_id), sc, id_dicts, growth_date=date, distrib=[['R','R','R'],['A','R','R'],['A','A','R'], ['A','A','A']], save_pth=batch_dir, eid=exp_id)
            #nn is the new name for the package with envelope scenes and
            nn = str(exp_id)+"_"+date
            os.rename(str(exp_id),nn)
            #id_dict = mtgp.crt_envdic()
            print "###########################"


            gc.collect()
        gc.collect()

    #Each batch of experiments are represented by a list of exp ids (exp_grp).
    #One CPU one batch.
    def batch(self, exp_grp):
        batch_directory = self.general_directory+ str(exp_grp[0]) + "~" + str(exp_grp[-1]) + "\\"
        Ensure_dir(batch_directory)
        for exp_id in exp_grp:
            try:
                self.run(exp_id, batch_directory)
            except:
                self.unsccfl_exps.append(exp_id)
                continue

        #Try again the unsuccessful experiments
        if len(self.unsccfl_exps) > 0:
            for exp_id in self.unsccfl_exps:
                try:
                    self.run(exp_id)
                    self.unsccfl_exps.remove(exp_id)
                except:
                    continue
            #Pickle the unsuccessful experiments after the second trial
            fn = str(exp_grp[0]) + "~" + str(exp_grp[-1]) + ".unsccfl"
            op = open(fn, "w")
            cPickle.dump(self.unsccfl_exps, op, 0)
            op.close()


pnbr = 2
#An instance of the interception object


pi = Postpara_Interception(general_directory=".\\PararunResults\\",\
                sub_directory_names=[\
                                        "1996_6_30"\
                                    ],\
                cpu_number=pnbr)
"""

pi = Postpara_Interception(general_directory=".\\PararunResults\\",\
                sub_directory_names=[\
                                        "1994_6_30",\
                                        "1995_6_30",\
                                        "1996_6_30",\
                                        "1997_6_30",\
                                        "1998_6_30"\
                                    ],\
                cpu_number=pnbr)
"""
def parafunc(exp_grp):
    pr = pi
    pr.batch(exp_grp)


if __name__ == "__main__":
    pool = Pool(processes=pnbr)
    eg = [[3],[7]]
    #eg = pi.exp_groups
    print eg
    pool.map(parafunc, eg)

"""
mtgp = Mtg_Processing("./PararunResults_20-12-2011/1996_6_30/6.mtg")
#print len(mtgp.pseudo_lstring)
#for i in mtgp.pseudo_lstring:
#    print vars(i[0])
env = Envelope(mtgp.id_dict, "./PararunResults_20-12-2011/1996_6_30/6.bgeom")
#env.crt_opt_dir()
env.intercept()
"""



#itcpt = Interception(".\\PararunResults\\")

#print itcpt.mtg_files

"""
    def mtg_bgeom_link(self):

    def only_shape(self):

    def envelope(self):
"""



