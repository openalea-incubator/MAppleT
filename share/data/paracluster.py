#-------------------------------------------------------------------------------
# Name:        paracluster
# Purpose:     A script to organise and run sge sh file as well as the parasuper
#
# Author:      HAN
#
# Created:     03/01/2012
# Copyright:   (c) HAN 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os, math, cPickle

class Para_Cluster(object):
    def __init__(self, plan="/home/han/vplants/MAppleT/share/data/pleqplan.csv", \
                    prn=8, jbn=10, tg_file="task_groups.tg"):
        self.plan = plan
        #Number of experiments in the plan
        self.exn = 0
        #Number of processors at each node
        self.prn = prn
        #Number of nodes you want to use, but not the number of nodes
        #that are already available or that you can use
        self.jbn = jbn
        #Task groups, e.g.
        """
         [
            [
                [0,1,2,3,4,5,6,7],
                [8,9,10,11,12,13,14,15]
            ]
            [
                [16,17,18,19,20,21,22,23],
                [24,25,26,27,28,29,30,31]
            ]
            [
                [32,33,34,35,36,37,38,39],
                [40,41,42,43,44,45,46,47]
            ]
            ...
         ]

        """
        self.tg = []
        #A pickled file of self.tg
        self.tg_file = tg_file

    #Write information to a sh file
    def shw(self):
        sh = open("para_sge.sh", "w")
        sh.write("#!/bin/bash\n")
        sh.write("#\n")
        sh.write("# SGE PARAMETERS\n")
        sh.write("#$ -N MAppleT\n")
        sh.write("#$ -q bioinfo.q\n")
        sh.write("#$ -pe parallel_smp {0}\n".format(self.prn))
        sh.write("#$ -S /bin/bash\n")
        sh.write("#$ -cwd\n")
        sh.write("#$ -V\n")
        sh.write("#$ -t 1-{0}\n".format(self.jbn))
        sh.write("# JOB BEGIN\n")
        sh.write("/usr/bin/python26 /home/han/vplants/MAppleT/share/data/parasuper.py {0} {1} {2} $SGE_TASK_ID\n".format(self.plan, self.prn, self.tg_file))
        sh.write("# JOB END\n")
        sh.close()

    def alloc(self):
        p = open(self.plan, "r")
        #The number of experiments is equal to the number of lines minus 1
        self.exn = sum(1 for line in p) - 1
        p.close()

        #If the number of processors in total is bigger than the number of
        #experiments, then only use "enough" nodes with "enough" processors
        ttl_prn = self.prn * self.jbn
        if ttl_prn>self.exn:
            self.jbn = int(math.ceil(float(self.exn)/self.prn))
        self.tg = [[]]*self.jbn
        #The number of experiments going to be allocated to each node
        #However, for the last node, its number of experiments could be higher
        #or lower than other nodes, equal to
        #    self.exn - self.exn_per_node * (self.jbn-1)
        #This is supported by the following code
        self.exn_per_node = int(round(float(self.exn) / self.jbn))
        if self.exn_per_node < self.prn:
            self.exn_per_node = self.prn
        """
        if n*self.jbn >= self.exn:
            self.exn_per_node = n
        else:
            self.exn_per_node = n+1
        """
        #For teach task/job, the number of experiment groups ("eg" in parasuper)
        #should be equal to the number of processors each node has
        lnid = self.jbn - 1
        #The id of the last processor at a node, equivalent to the number
        #of processors minus 1 (the id of the first processor is 0)
        lpid = self.prn-1
        #For all nodes except the last node
        for i in range(lnid):
            self.tg[i] = [[]] * self.prn
            exn_per_cpu = int(round(self.exn_per_node/self.prn))
            #The base of experiment ids for this node, equivalent to the first
            #experiment id allocated to this node
            eid_base = self.exn_per_node * i
            for j in range(lpid):
                self.tg[i][j] = range(eid_base+exn_per_cpu*j, eid_base+exn_per_cpu*(j+1))
            if exn_per_cpu*self.prn >= self.exn_per_node:
                self.tg[i][lpid] = range(eid_base+exn_per_cpu*lpid, eid_base+self.exn_per_node)
            else:
                self.tg[i][lpid] = range(eid_base+exn_per_cpu*lpid, eid_base+exn_per_cpu*(lpid+1))
                extra_eids = range(eid_base+exn_per_cpu*(lpid+1), eid_base+self.exn_per_node)
                for k in range(len(extra_eids)):
                    self.tg[i][k].append(extra_eids[k])
        #For the last node
        self.tg[lnid] = [[]] * self.prn
        #The number of experiments for the last node
        exn_ln = self.exn - self.exn_per_node*(self.jbn-1)
        #The number of experiments for each cpu at the last node
        exn_per_cpu_ln = int(round(exn_ln/self.prn))
        #The base of experiment ids for the last node, equivalent to the first
        #experiment id allocated to this node
        eid_base_ln = self.exn_per_node * lnid
        for j in range(lpid):
            self.tg[lnid][j] = range(eid_base_ln+exn_per_cpu_ln*j, eid_base_ln+exn_per_cpu_ln*(j+1))
        if exn_per_cpu_ln*self.prn >= self.exn_per_node:
            self.tg[lnid][lpid] = range(eid_base_ln+exn_per_cpu_ln*lpid, eid_base_ln+exn_ln)
        else:
            self.tg[lnid][lpid] = range(eid_base_ln+exn_per_cpu_ln*lpid, eid_base_ln+exn_per_cpu_ln*(lpid+1))
            extra_eids_ln = range(eid_base_ln+exn_per_cpu_ln*(lpid+1), eid_base_ln+exn_ln)
            for k in range(len(extra_eids_ln)):
                self.tg[lnid][k].append(extra_eids_ln[k])

        for i in range(len(self.tg)):
            if self.tg[i] != []:
                for j in range(len(self.tg[i])):
                    if self.tg[i] == []:
                        break
                    else:
                        for k in self.tg[i]:
                            if k == []:
                                self.tg[i].remove(k)
            if self.tg[i] == []:
                self.tg.remove(self.tg[i])

        #Pickle the tg list
        tg_op = open(self.tg_file, "w")
        cPickle.dump(self.tg, tg_op, 0)
        tg_op.close()

    def launch(self):
        os.system("qsub para_sge.sh")
        #os.system("/usr/bin/python26 /NAS/home/han/vplants/MAppleT/share/data/parasuper.py {0} {1} {2} 1\n".format(self.plan, self.prn, self.tg_file))



if __name__ == "__main__":
    #p = open("/han/vplants/MAppleT/share/data/plan300.csv","r")
    #print p.read()

    parac = Para_Cluster(plan="/home/han/vplants/MAppleT/share/data/pleqplan.csv", jbn=1)
    parac.alloc()
    parac.shw()
    parac.launch()
    """
    for i in parac.tg:
        print "{0}\n".format(parac.tg.index(i))
        for j in i:
            print "\t" + str(j)
    """














