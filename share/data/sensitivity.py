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

from openalea.stocatree.combination import Partit

from multiprocessing import Process, Pool

"""
p = Partit(1,10,0)
print p.partition_list
"""
# define the number of experiments used for random batchmode
exp_nbr = 6

#define the directory of the files for counting experiments and for storing output results
output_directory = "Batchmode_ExpCounters&Results/"

#initialise the starting date and the ending date of the batchmode experiments (real-world time)
starting_date = None
ending_date = None

#initilise the planned number of successful experiments
count_successful_experiments = 0

#initialise the flag to indicate whether the batchmode is successfully completed or not
Batchmode_Completed = 0

Viewer.animation(True)


def pre_batch():
    #First, it would be good to back up the previous output directory by renaming it
    t = datetime.utcnow()
    backup_name = "Batchmode_ExpCounters&Results" + "_" + str(t.year) + "-" + str(t.month) + "-" + str(t.day) + "-" + str(t.hour) + "_" + str(t.minute) + "_" + str(t.second)
    os.rename(output_directory, backup_name)
    #And then, a new output directory can be created
    os.mkdir(output_directory)

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
    para = Parameterise()
    para.set_value()
    para.ini_write()

    # Read the id of the previous virtual experiment
    # The value of experiment id starts from 0 rather than 1
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
       # This file is used to restore the current experiment so that the experiment \
        # id can be read and then written through L-system into the result
        exp_rec = open(output_directory + 'exp_recorder.h', 'w')
        exp_rec.write('%u' % exp_id)
        exp_rec.close()

        # e is a flag to mark whether a try is sucessful: initialised as 0, successful as 1 and otherwise 0
        # e = 0
        try:
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
    email_result.email(directory, result_list, receiver, starting_date, ending_date, exp_nbr, count_successful_experiments, Batchmode_Completed)

def main():
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

    """
    pool = Pool(processes=4)
    #result = pool.apply_async(main, 0)
    pool.map(main, range(6))
    """


    """
    p = Process(target=main, args=())
    p.start()
    p.join()
    """



    main()




