#-------------------------------------------------------------------------------
# Name:        pararun
# Purpose:     A script for running batchmode experiments in parallel.
# Note:        The difference of this script with parabatch.py is that, the
#              communication with stocatree.lpy is through Lsystem().context()
#              rather than file reading and writing.
# Author:      Han
# Created:     12/12/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import openalea.lpy as lpy
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree import get_shared_data
import csv as pycsv
from multiprocessing import Process, Pool
import gc
import cPickle
import sys
import os

class Para_Run(object):
    def __init__(self, lsystem_file="stocatree.lpy", \
                        ini_file="stocatree.ini", \
                        sensitivity_plan="plan.csv", \
                        csv_delimiter = ";", \
                        cpu_number=1):
        self.lsystem_file = lsystem_file
        self.ini_file = ini_file
        self.sensitivity_plan = sensitivity_plan
        self.csv_delimiter = csv_delimiter
        self.cpu_number = cpu_number

        print sensitivity_plan, csv_delimiter, cpu_number

        #A list to record unsuccessful experiment ids
        self.unsccfl_exps = []
        #The directory for data output
        self.data_dir = None

        #Initialise exp_inputs
        self.exp_inputs = []
        plan_read = pycsv.reader(open(self.sensitivity_plan, "rb"), \
                                    delimiter=self.csv_delimiter)
        for row in plan_read:
		    if row[0]!="":
			    self.exp_inputs.append([float(row[3])/2, float(row[4]), float(row[2]), float(row[1]), int(row[5])])
        """
		Data structure of self.exp_inputs:
		[
			[apex.maximum_size_1, leaf.max_area_1, internode.max_length_1, tree.branching_angle_1, stocatree.select_trunk_1],
			[apex.maximum_size_2, leaf.max_area_2, internode.max_length_2, tree.branching_angle_2, stocatree.select_trunk_2],
			.
			.
			.
			[apex.maximum_size_n, leaf.max_area_n, internode.max_length_n, tree.branching_angle_n, stocatree.select_trunk_n],
		]
		"""

        #The number of proposed experiments, equivalent to the number of inputs
        self.exp_nbr = len(self.exp_inputs)
        #If the number of assigned cpus is bigger than the number of experiments
        #if self.exp_nbr>self.cpu_number:
        #    #then only use enough cpus
        #    self.cpu_number=self.exp_nbr
        self.exp_groups = [[]] * self.cpu_number
        self.expnbr_per_grp = int(round(float(self.exp_nbr)/self.cpu_number))

        #The index of the last item of self.exp_groups
        lid = len(self.exp_groups)-1
        #Initialise self.exp_groups except its last item
        #Note: the exp_id varies from 0 to exp_nbr-1 (not 1 to exp_nbr)
        for i in range(lid):
            self.exp_groups[i] = range(i*self.expnbr_per_grp, (i+1)*self.expnbr_per_grp)
        #Initialise the last item of self.exp_groups
        self.exp_groups[lid] = range(lid*self.expnbr_per_grp, self.exp_nbr)

    #Changing parameter configurations for each experiment and then running it
    def run(self, exp_id):

        #Added by han on 16-06-2012
        start_time = time.time()

        #print exp_id
        conf = ConfigParams(get_shared_data("stocatree.ini"))
        conf.apex.maximum_size = self.exp_inputs[exp_id][0]
        conf.leaf.max_area = self.exp_inputs[exp_id][1]
        conf.internode.max_length = self.exp_inputs[exp_id][2]
        conf.tree.branching_angle = self.exp_inputs[exp_id][3]
        conf.stocatree.select_trunk = self.exp_inputs[exp_id][4]
        print conf.stocatree.select_trunk
        l = lpy.Lsystem("stocatree.lpy")
        l.context()["options"] = conf
        l.context()["current_experiment"] = exp_id
        if self.data_dir == None:
            self.data_dir= l.context()["output_directory"]
        #l.iterate()
        l.animate()
        gc.collect()

        #Added by Han on 16-06-2012
        end_time = time.time()
        running_duration = end_time - start_time

        #Added by Han on 16-06-2012 for calucating running duration for each experiment
        durations = open("durations.txt", "a")
        durations.write(str(exp_id)+","+str(running_duration))
        durations.write("\n")
        durations.close()

    #Each batch of experiments are represented by a list of exp ids (exp_grp).
    #One CPU one batch.
    def batch(self, exp_grp):
        for exp_id in exp_grp:
            try:
                self.run(exp_id)
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


#The number of processors to be used
v = sys.argv
plan_file = v[1]
pnbr = int(v[2])
tg_data = open(v[3])
#In SGE, the index is from 1~10 for example, therefore here the corresponding
#index should be int(v[4])-1
eg = cPickle.load(tg_data)[int(v[4])-1]
tg_data.close()


def parafunc(exp_grp):
    pr = Para_Run(sensitivity_plan=plan_file, \
                    csv_delimiter=",", \
                    cpu_number=pnbr)
    pr.batch(exp_grp)

if __name__ == "__main__":
    os.chdir("/home/han/vplants/MAppleT/share/data/")
    pool = Pool(processes=pnbr)
    #To get the exp_groups for using parafunc
    #eg = Para_Run(cpu_number=pnbr).exp_groups
    #eg = [[23],[35]]
    for i in eg:
        print i
    print "Hi"
    pool.map(parafunc, eg)

