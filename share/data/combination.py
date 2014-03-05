#-------------------------------------------------------------------------------
# Name:        combination
# Purpose:
#
# Author:      Han
#
# Created:     19/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import math

class Partit(object):
    def __init__(self, min=None, max=None, grade=None):
        self.min = float(min)
        self.max = float(max)
        self.grade= grade

        self.partition_list = [0] * (pow(2, self.grade)+1)

        self.partition_list[0] = self.min
        self.partition_list[len(self.partition_list)-1] = self.max
        for i in range(1, len(self.partition_list)-1):
            self.partition_list[i] = (self.min + self.max) * i/pow(2, self.grade)


class Comb(object):
    def __init__(self, ranges=None, grade=None):

        """
        ranges is a list of [min, max] for different aspects (e.g. internode length, leaf area)
        its structure is
        [
            [min_1, max_1]
            [min_2, max_2]
            .
            .
            .
        ]
        """
        self.ranges = ranges
        self.grade = grade

        self.points = []

        """
        points is a list of partitions corresponding to ranges, its number of points depend
        on the grade:
        [
            [min_1, point_1.1, point_1.2, ..., max_1]
            [min_2, point_2.1, point_2.2, ..., max_2]
            .
            .
            .
        ]
        """
        for i in range(len(self.ranges)):
            self.points.append(Partit(self.ranges[i][0], self.ranges[i][1], self.grade).partition_list)


    def combination_lists(self):
        c = [[]]
        for i in self.points:
            t = []
            for j in i:
                for k in c:
                    t.append(k+[j])
            c = t
        return c
        """
        This is to create a combination list like:
            [
                .
                .
                .
                [point_1.x, point_2.y,...]
                .
                .
                .
            ]
        """

class Exp_batch(object):
    def __init__(self, exp_nbr, batch_nbr):
        self.exp_nbr = exp_nbr
        self.batch_nbr = batch_nbr
        self.group_size = 0
        self.exp_groups= []
        """
        self.group_size is the number of exp_ids a batch group contains
        self.exp_groups is like
        [
            .
            .
            .
            [start_exp_id, end_exp_id]
            .
            .
            .
        ]
        where the index of this list is correspondant to batch_id
        """

        if self.exp_nbr <= self.batch_nbr:
            self.group_size = 1
        else:
            self.group_size = int(math.ceil(float(self.exp_nbr)/float(self.batch_nbr)))

        if self.exp_nbr > self.batch_nbr:
            for i in range(self.batch_nbr):
                start_id = i*self.group_size
                if i < self.batch_nbr-1:
                    end_id = start_id + self.group_size -1
                else:
                    end_id = self.exp_nbr-1
                self.exp_groups.append([start_id, end_id])
        else:
            self.exp_groups.append([0,self.exp_nbr-1])
