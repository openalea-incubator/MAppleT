#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      KELNER
#
# Created:     22/05/2011
# Copyright:   (c) KELNER 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from combination import Partit, Comb, Exp_batch

class Para_ranges(object):
    def __init__(self, grade = 0, batch_nbr = 1):
        self.grade = grade
        self.batch_nbr = batch_nbr

    def set_ranges(self):

        self.ranges_dic = {
                                "tree" :
                                    {
                                        "branching_angle" : [-40, 90]
                                    },
                                "internode" :
                                    {
                                        "max_length" : [0.008, 0.05]
                                    },
                                "apex" :
                                    {
                                        "maximum_size" : [0.001, 0.0085]
                                    },
                                "leaf" :
                                    {
                                        "max_area" : [0.0003, 0.009]
                                    }
                            }

        diclist = {"tree":0, "internode":1, "apex":2, "leaf":3}
        self.ranges_list = [[]] * len(diclist)
        for k,v in self.ranges_dic.iteritems():
            i = diclist[k]
            self.ranges_list[i] = v.values()[0]

    def set_combinations(self):
        comb = Comb(self.ranges_list, self.grade)
        self.combination_lists = comb.combination_lists()


    def set_exp_batch(self):
        exp_bt = Exp_batch(len(self.combination_lists), self.batch_nbr)
        self.exp_groups = exp_bt.exp_groups