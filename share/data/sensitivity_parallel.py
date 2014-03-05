#-------------------------------------------------------------------------------
# Name:        sensitivity.py
# Purpose:     Running experiments for sensitivity analysis
#
# Author:      Han
#
# Created:     04/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import openalea.lpy as lpy
from openalea.plantgl.all import *
#If this import is filtered, then the email_result module under the "share/data" category will be used instead
#import openalea.stocatree.tools.email_result
import email_result
#For recording the starting and the ending datetime
from datetime import datetime
import os
#from openalea.stocatree.parameterisation import Parameterise
from parameterisation import Parameterise
from parameters_ranges import Para_ranges


from combination import *

batches = 3

p_rng = Para_ranges(batch_nbr=batches)
p_rng.set_ranges()
p_rng.set_combinations()
p_rng.set_exp_batch()


def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.mkdir(d)
		
def para_batch(batch_id):
	# define the number of experiments used for random batchmode
	first_exp = p_rng.exp_groups[batch_id][0]
	last_exp = p_rng.exp_groups[batch_id][1]

	#define the directory of the files for counting experiments and for storing output results
	output_directory = "Batchmode_ExpCounters&Results/"
	ensure_dir(output_directory)
	output_directory = output_directory + str(first_exp) + "~" + str(last_exp) + "/"
	ensure_dir(output_directory)

	#initialise the starting date and the ending date of the batchmode experiments (real-world time)
	starting_date = None
	ending_date = None

	#initilise the planned number of successful experiments
	count_successful_experiments = 0

	#initialise the flag to indicate whether the batchmode is successfully completed or not
	Batchmode_Completed = 0

	Viewer.animation(True)

	def pre_batch():
		"""	
		#First, it would be good to back up the previous output directory by renaming it
		t = datetime.utcnow()
		backup_name = "Batchmode_ExpCounters&Results" + "_" + str(t.year) + "-" + str(t.month) + "-" + str(t.day) + "-" + str(t.hour) + "-" + str(t.minute) + "-" + str(t.second)
		os.rename(output_directory, backup_name)
		#And then, a new output directory can be created
		os.mkdir(output_directory)
		"""
	
		
		#Create a file to record the id of the previous successful experiment
		#Once an experiment is successfully finished, its id will be written to this file
		exp_sccfl = open(output_directory + 'exp_successful.h', 'w')
		exp_sccfl.close()

	# To run the 'stocatree.lpy'
	def run():
		l = lpy.Lsystem('stocatree.lpy')
		l.animate()
		#l.iterate()

	# The returned value of this batch() function is the number of succesful experiments
	def batch():

		# To set parameter values for sensitivity analysis and write them into an ini file
		# The pre-set values will be used to re-set their counterparts in "stocatree.ini", which is done later in lpy
		para = Parameterise(out_dir=output_directory)


		# Read the id of the previous virtual experiment
		# The value of experiment id starts from 0 rather than 1
		exp_sccfl = open(output_directory + 'exp_successful.h', 'r')
		prvs_exp = exp_sccfl.read()
		exp_sccfl.close()
		if (prvs_exp == '' or int(prvs_exp) >= last_exp):
			prvs_exp = -1 + first_exp
		# Initialise the id for the current experiment
		crrt_exp = int(prvs_exp) + 1

		# A local varialbe to count the number of successful experiments
		cnt_sccfl_expts = 0
		# Start the batchmode from the current point:
		for exp_id in range(crrt_exp,last_exp+1):
		   # This file is used to restore the current experiment so that the experiment \
			# id can be read and then written through L-system into the result
			exp_rec = open(output_directory + 'exp_recorder.h', 'w')
			exp_rec.write('%u' % exp_id)
			exp_rec.close()

			# e is a flag to mark whether a try is sucessful: initialised as 0, successful as 1 and otherwise 0
			# e = 0
			try:
				para.set_value(parameter_list=p_rng.combination_lists[exp_id])
				para.ini_write()
				run()
				e = 1
			except:
				e = 0

			if e == 1:
				cnt_sccfl_expts += 1
				# This is to record the successful point so that the next experiment can start from the one right after this
				exp_sccfl = open(output_directory + 'exp_successful.h', 'w')
				exp_sccfl.write('%u' % exp_id)
				exp_sccfl.close()

		return cnt_sccfl_expts


	# To send results to the
	def result_sending():
		directory = output_directory
		#define the list of result files
		result_list = ['Statistics_Metamer.csv', 'Statistics_Shoot.csv', 'Statistics_Branch.csv', 'Statistics_Tree.csv']
		#define the email address to receive the batchmode experiment results
		receiver = 'han@supagro.inra.fr,stocatree@gmail.com'
		email_result.email(directory, result_list, receiver, starting_date, ending_date, last_exp-first_exp+1, count_successful_experiments, Batchmode_Completed)



	#Back up the previous output directory and create a new empty output directory
	pre_batch()

	# Record the starting date
	starting_date = datetime.utcnow()
	try:
		# Run experiments
		count_successful_experiments = int (batch())
		# Record the ending date
		ending_date = datetime.utcnow()
		Batchmode_Completed = 1
	except:
		# Record the ending date
		ending_date = datetime.utcnow()
		Batchmode_Completed = 0
	try:
		result_sending()
	except:
		Batchmode_Completed = 2
		result_sending()

if __name__ == '__main__':
	para_batch(0)
	para_batch(1)
	para_batch(2)