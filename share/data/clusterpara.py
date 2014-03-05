#-------------------------------------------------------------------------------
# Name:        clusterpara.py
# Purpose: A script to manage parallel computing on a cluster
#
# Author:      Han
#
# Created:     08/12/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import openalea.lpy as lpy
from openalea.plantgl.all import *

from parameterisation import Pararange, Parameterise
from openalea.stocatree.diclist import Dic_to_list, List_to_dic
from openalea.stocatree.combination import Partit, Comb, Exp_batch, Substract
from openalea.stocatree.rw_tools import Ensure_dir, Recorder, Create_file
from openalea.stocatree.csv import ExprecCSV

from datetime import datetime
import os

from multiprocessing import Process, Pool

from lockfile import MkdirFileLock as Filelock

import time

import gc

class Cluster_Parallel(object):
    def __init__():
        self.l = lpy.Lsystem("stocatree.lpy")

    #Setting parameters, preparing the batchmode simulations
    def pre_batch(self):
        c = self.l.context()
        conf = c["options"]
        conf.internode.max_length = 0.01
        c["options"] = conf
        self.l.context() = c

	def run(self):
		l.iterate()



#This is a parallel batchmode approach developed by Han for PC-based computing
class Parallel_batchmode(object):
	def __init__(self, batch_nbr=3, grade=0, output_dir="ParallelResults/"):
		self.batch_nbr = batch_nbr
		self.grade = grade
		self.exp_inputs = []
		self.exp_nbr = 0
		self.exp_groups = []

		self.pre_exp_nbr = 0

		self.output_dir = output_dir

	def run(self):
		l = lpy.Lsystem("stocatree.lpy")
		l.animate()
		#l.iterate()

	def exp(self, exp_id, exp_ii, batch_dir):

		#The list of parameter values
		pvalues = self.exp_inputs[exp_ii[exp_id]]

		#Covert the input data from list to dictionary
		ltd = List_to_dic(pvalues, self.dtl.diclist_keys)
		input = ltd.listdic

		r = Recorder(self.output_dir + "current_exp.h")
		lock = Filelock(self.output_dir + "current_exp.h")
		if not lock.is_locked():
			lock.acquire()
			#Write the parameter values to the Sensitivity_Parameters.ini
			prts = Parameterise(parameter_dic=input, out_dir=batch_dir)
			prts.ini_write()
			cr = Recorder(batch_dir + "exp_recorder.h")
			cr.write(str(exp_id))

			self.run()


		"""
		e = 0
		while e==0:
			r = Recorder(self.output_dir + "current_exp.h")
			r.read()
			if r.content == "":
				r.write(str(exp_id))

				#Write the parameter values to the Sensitivity_Parameters.ini
				prts = Parameterise(parameter_dic=input, out_dir=batch_dir)
				prts.ini_write()
				cr = Recorder(batch_dir + "exp_recorder.h")
				cr.write(str(exp_id))

				self.run()
				e = 1
				r.clear()
			else:
				print r.content
		"""

		"""
		r = Recorder(self.output_dir + "current_exp.h")
		r.read()
		if r.content == "":
			r.write(str(exp_id))

			#Write the parameter values to the Sensitivity_Parameters.ini
			prts = Parameterise(parameter_dic=input, out_dir=batch_dir)
			prts.ini_write()
			cr = Recorder(batch_dir + "exp_recorder.h")
			cr.write(str(exp_id))

			self.run()
			e = 1
			r.clear()

		else:
			e = 0
			print r.content
		print e
		"""

		finichk = Recorder(batch_dir + "exp_successful.h")
		finichk.read()
		print finichk.content
		if finichk.content != "":
			fini_exp = int(finichk.content)
			if fini_exp == exp_id:
				exprec_file = "Exp_Record.csv"
				Create_file(batch_dir + exprec_file)
				dt = datetime.utcnow()
				cpdt = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + " " + str(dt.hour) + ":" + str(dt.minute)
				ExprecCSV(exp_id=fini_exp, finidate=cpdt, para_dic=input, file_name=exprec_file, output_directory=batch_dir)
			else:
				print fini_exp, exp_id





		"""
		try:
			cr = Recorder(batch_dir + "exp_recorder.h")
			cr.write(str(exp_id))
			run()
			finished = True
		except:
			finished = False

		if finished == True:
			r = Recorder(batch_dir + "exp_successful.h")
			r.write(str(exp_id))
		"""







	#This is a requisite method for using batch
	#That is to say, before batch(), there must be pre_parabatch()
	def pre_parabatch(self):

		#Make sure the output directory exists, otherwise create one
		Ensure_dir(self.output_dir)

		#Set ranges for investigated parameters
		prange = Pararange()

		#Convert the ranges (from dictionary) into form of a list
		self.dtl = Dic_to_list(prange.ranges_dic)

		#Generate combinations of parameter values
		comb = Comb(ranges=self.dtl.diclist_values, grade=self.grade)
		comb.combine()

		#Before setting inputs for new experiments, check the grade that has been used
		r = Recorder(self.output_dir + "finished_grade.rec")
		r.read()

		if r.content == "":
			pre_grade = ""
		else:
			pre_grade = int(r.content)

		if pre_grade == "":
			#Each combination is an input for an experiment
			self.exp_inputs = comb.combinations
		elif self.grade > pre_grade:
			#Get combinations based on the previously used grade
			previous_comb = Comb(ranges=self.dtl.diclist_values, grade=pre_grade)
			previous_comb.combine()
			#and then remove those combinations
			self.exp_inputs = Substract(comb.combinations, previous_comb.combinations).result
			#Record the number of experiments based on previous grade
			self.pre_exp_nbr = len(previous_comb.combinations)
		elif self.grade <= pre_grade:
			raise Exception("The grade has been tested. Please set a new one.")

		#The number of inputs (or combinations) is the number of experiments
		self.exp_nbr = len(self.exp_inputs)
		#Group experiment ids for each batch (in form of [[first_exp_id, last_exp_id], [first_exp_id, last_exp_id], ...])
		exp_batch = Exp_batch(self.exp_nbr, self.batch_nbr)
		self.exp_groups = exp_batch.exp_groups
		print self.exp_groups
		#print self.exp_inputs

		r = Recorder(self.output_dir + "current_exp.h")
		r.clear()


	def batch(self, batch_id):

		#print batch_id
		#print self.exp_groups
		#print self.exp_inputs


		#Matach the exp group for this batch and get the ids of the first and last exps
		exps = self.exp_groups[batch_id]

		#The index of first experiment in list exps for this batch
		fexp_index = exps[0]
		#The index of last experiment in list exps for this batch
		lexp_index = exps[1]

		#The ids of the first and last experiments
		#The indexes are used to get parameter combinations
		#The ids are used for outputs and records
		fexp_id = fexp_index + self.pre_exp_nbr
		lexp_id = lexp_index + self.pre_exp_nbr
		#A dictionary for the one-to-one matches between ids and indexes
		#{id1:index1, id2:index2, ...}
		exp_ii = {}

		for ind in range(fexp_index, lexp_index+1):
			exp_ii.update({(ind+self.pre_exp_nbr):ind})

		#Create a folder for output from this batch
		batch_dir = self.output_dir + str(fexp_id) + "~" + str(lexp_id) + "/"
		Ensure_dir(batch_dir)



		eid = fexp_id
		while eid <= lexp_id:
			#Read the previous exp id
			sr = Recorder(batch_dir + "exp_successful.h")
			sr.read()

			if sr.content == "":
				prvs_expid = fexp_id - 1
			else:
				prvs_expid = int(sr.content)


			print eid, prvs_expid

			time.sleep(batch_id*3)
			#If this eid is the supposed-to-be exp id (namely, prvs_expid+1)
			if eid == prvs_expid+1:
				self.exp(eid, exp_ii, batch_dir)
				gc.collect()
				eid += 1
			#If this eid is not the supposed-to-be exp id, force it to be
			#This is to avoid that some experiments are jumped over or ignored
			else:
				eid = prvs_expid+1
				self.exp(eid, exp_ii, batch_dir)
				gc.collect()
				eid += 1

	def post_parabatch(self):
		r = Recorder(self.output_dir + "finished_grade.rec")
		r.write(str(self.grade))



class Try(object):
	def __init__(self, n):
		self.n = n
	def pr(self, n):
		print n


p = Parallel_batchmode(grade=1)
#p.pre_parabatch()
#t = Try(1)
def parabatch(n):
	#pp = Parallel_batchmode(grade=0)
	pp = p
	pp.pre_parabatch()
	pp.batch(n)
	#pp.post_parabatch()
	#p.batch(n)
	#p.run()
	#print n
	#print n
	#t.pr(n)




if __name__ == "__main__":
	#p = Parallel_batchmode(grade=0)
	#p.pre_parabatch()
	#p.batch(1)

	"""
	p.batch(0)
	p.pre_parabatch()
	p.batch(1)
	p.batch(2)
	p.post_parabatch()
	"""



	pool = Pool(processes=4)
    #result = pool.apply_async(main, 0)
    #pool.map(p.batch, range(3))
	pool.map(parabatch, range(3))
	p.post_parabatch()
	#parabatch(0)
	#parabatch(1)
	#parabatch(2)





