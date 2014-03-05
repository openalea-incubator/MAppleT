#-------------------------------------------------------------------------------
# Name:        Batchmode
# Purpose:
#
# Author:      Han
#
# Created:     16/12/2010
# Copyright:   (c) Han 2010
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


# define the number of experiments used for random batchmode, which is also the planned number of experiments
exp_nbr = 1
end_year = 1995
end_month = 6
end_day = 30

# define the maximum number of re-try implementations when an experiment is broken because of errors
rd_nbr = 1

#define the directory of the files for counting experiments and for storing output results
output_directory = "Batchmode_ExpCounters&Results/"

#define the list of result files
#result_list = ['light_interception_per_shoot.csv', 'light_interception_observ.csv', 'light_interception.csv']
result_list = ['Statiscis_Metamer.csv', 'Statistics_Shoot.csv', 'Statistics_Branch.csv', 'Statistics_Tree.csv']

#define the email address to receive the batchmode experiment results
receiver = 'han@supagro.inra.fr,stocatree@gmail.com'

#initialise the starting date and the ending date of the batchmode experiments (real-world time)
starting_date = None
ending_date = None

#initilise the planned number of successful experiments
count_successful_experiments = 0

#initialise the flag to indicate whether the batchmode is successfully completed or not
Batchmode_Completed = 0

Viewer.animation(True)

f = open('stocatree.lpy', 'r')
code = f.read()

def parameterise(end_year_x, end_month_x, end_day_x):
    fp = open("C:/Python26/Lib/site-packages/VPlants.StocaTree-0.9.4-py2.6.egg/share/data/Parameters.ini", "w")
    #fp = open("Parameters.ini", "w")
    fp.write("[general]\n")
    fp.write("batchmode = True\n")
    fp.write("verbose = False\n")
    fp.write("max_iterations  = 3600000\n")
    fp.write("filename = stocatree.lpy\n")
    fp.write("starting_year = 1994\n")
    fp.write("end_year = %u-0%u-%u\n" % (end_year_x, end_month_x, end_day_x))
    #fp.write("end_year = %d-06-30\n" % end_year_x)
    fp.write("time_step = 1\n")
    fp.write("seed = 1163078255\n")
    fp.write("tag = test\n")
    fp.write("batch_dir = Batchmode_ExpCounters&Results/\n")
    fp.write("single_dir = Singlemode_ExpCounters&Results/\n")

    fp.write("[stocatree]\n")
    fp.write("saveimage = False\n")
    fp.write("savescene = True\n")
    fp.write("movie = False\n")
    fp.write("second_year_draws = False\n")
    fp.write("ruptures = False\n")
    fp.write("stake = True\n")
    fp.write("select_trunk = 2\n")
    fp.write("mechanics = True\n")
    fp.write("render_mode = bark\n")
    fp.write("stride_number = 5\n")
    fp.write("light_interception = True\n")

    fp.write("[output]\n")
    fp.write("sequences = True\n")
    fp.write("l_string  = True\n")
    fp.write("light_interception = True\n")
    fp.write("counts = True\n")
    fp.write("trunk = True\n")
    fp.write("leaves = True\n")
    fp.write("mtg = True\n")

    fp.write("[tree]\n")
    fp.write("phyllotactic_angle = -144.0\n")
    fp.write("branching_angle = -45.\n")
    fp.write("floral_angle = -10.\n")
    fp.write("tropism = 0.1\n")
    fp.write("preformed_leaves = 8\n")
    fp.write("spur_death_probability = 0.3\n")
    fp.write("inflorescence_death_probability = 0.2\n")

    fp.write("[wood]\n")
    fp.write("wood_density = 1000\n")
    fp.write("reaction_wood_rate = 0.5\n")
    fp.write("reaction_wood_inertia_coefficient = 0.1\n")
    fp.write("youngs_modulus = 1.1\n")
    fp.write("modulus_of_rupture = 50e6\n")

    fp.write("[internode]\n")
    fp.write("min_length = 0.015\n")
    fp.write("elongation_period = 10.\n")
    fp.write("plastochron = 3.\n")
    fp.write("max_length = 0.05\n")

    fp.write("[apex]\n")
    fp.write("terminal_expansion_rate=0.00002\n")
    fp.write("minimum_size=0.00075\n")
    fp.write("maximum_size=0.006\n")

    fp.write("[markov]\n")
    fp.write("maximum_length = 70\n")
    fp.write("minimum_length = 4\n")

    fp.write("[fruit]\n")
    fp.write("flower_duration = 10.\n")
    fp.write("max_relative_growth_rate = 0.167\n")
    fp.write("lost_time = 28\n")
    fp.write("max_age = 147\n")
    fp.write("probability = 0.3\n")
    fp.write("max_absolute_growth_rate = 0.0018\n")

    fp.write("[leaf]\n")
    fp.write("fall_probability = 0.1\n")
    fp.write("maturation = 12\n")
    fp.write("mass_per_area = 0.220\n")
    fp.write("max_area = 0.009\n")
    fp.write("min_final_area = 0.0003\n")
    fp.write("petiole_radius = 0.0006\n")
    fp.write("preformed_leaves = 8\n")

    fp.close()

def result_sending():
    directory = output_directory
    email_result.email(directory, result_list, receiver, starting_date, ending_date, exp_nbr, count_successful_experiments, Batchmode_Completed)

def run():
    l = lpy.Lsystem('stocatree.lpy')
    l.animate()
    #l.iterate()

# The returned value of this batch() function is the number of succesful experiments
def batch():
    # Read the id of the previous virtual experiment
    # The value of experiment id starts from 0 rather than 1
    try:
        exp_sccfl = open(output_directory + 'exp_successful.h', 'r')
    except:
        exp_sccfl = open(output_directory + 'exp_successful.h', 'w')
        exp_sccfl.close()
        exp_sccfl = open(output_directory + 'exp_successful.h', 'r')
    prvs_exp = exp_sccfl.read()
    exp_sccfl.close()
    if (prvs_exp == '' or int(prvs_exp) >= exp_nbr):
        prvs_exp = -1
    # Initialise the id for the current experiment
    crrt_exp = int(prvs_exp) + 1

    # A local varialbe to count the number of successful experiments
    cnt_sccfl_expts = 0
    # Start the batchmode from the current point:
    for exp_id in range(crrt_exp,exp_nbr):
        parameterise(end_year, end_month, end_day)

        # This file is used to restore the current experiment so that the experiment \
        # id can be read and then written through L-system into the result
        exp_rec = open(output_directory + 'exp_recorder.h', 'w')
        exp_rec.write('%u' % exp_id)
        exp_rec.close()
        # e is a flag to mark whether a try is sucessful: initialised as 0, successful as 1 and otherwise 0
        # e = 0

        for i in range(rd_nbr):
            #If this is the first time to try this experiment or if the try at last time is not successful
            #if e == 0:
            try:
                run()
                e = 1
            except:
                e = 0
                continue
            if e == 1:
                cnt_sccfl_expts += 1
                # This is to record the successful point so that the next experiment can start from the one right after this
                exp_sccfl = open(output_directory + 'exp_successful.h', 'w')
                exp_sccfl.write('%u' % exp_id)
                exp_sccfl.close()
                break

    return cnt_sccfl_expts


if __name__ == '__main__':
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

