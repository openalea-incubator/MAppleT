#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      Han
#
# Created:     24/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# This class is suitable for the dict structure specified in "parameterisation.py" only
class Dic_to_list(object):
    def __init__(self, dic={}):
        self.dic = dic
        self.list = []
        """
        self.dic = {
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
        """


        self.diclist_keys = []
        self.diclist_attributes= []
        self.diclist_values = []

        for k,v in self.dic.iteritems():
            if type(v) == type({}):
                vk_list = v.keys()
                vv_list = []
                va_list = []
                for vk in vk_list:
                    vv_list.append(v[vk])
                    va_list.append(vk)

                self.diclist_keys.append({k:vk_list})
                self.diclist_values += vv_list
                self.diclist_attributes += va_list
            else:
                self.diclist_keys.append(k)
                self.diclist_values.append(v)



    """
    diclist_keys is like
        [
            {"tree" : ["branching_angle"]},
            {"internode" : ["max_length"]},
            {"apex" : ["maximum_size"]},
            {"leaf" : ["max_area"]}
        ]

    Note: for each element (in form of a dictionary) of diclist_keys,
            there is only one key (e.g. "trees") for that dictionary,
            though the value (in form of a list) of that dictionary can have
            multiple elements (e.g. "branching_angle", "flowering_angle"...)


    diclist_attributes is like
        [
            "branching_angle", "max_length", "maximum_size", "max_areac"]
        ]

    diclist_values is like
        [
            [-40,20],
            [0.008,0.05],
            [0.001, 0.0085],
            [0.0003, 0.009]
        ]

    Note, the length of diclist_values is equal to that of diclist_keys
    """

class List_to_dic(object):
    def __init__(self, list=[], dickeys=[]):
        self.list = list
        self.dickeys = dickeys
        self.attributes = []
        self.listdic = {}

        """
        The structure of self.list is different from diclist_values. It uses single
        numbers (rather than a [min,max] list) as individual elements, for example:
            [-40, 0.008, 0.001, 0.0003]
        """

        #This is to make sure the number of elements of the list is equal to the number of attributes (e.g. "branching_angle") in the dic
        p = [0] * len(dickeys)
        for i in range(len(p)):
            p[i] = len(dickeys[i])
        assert len(list) == sum(p)

        for d in self.dickeys:
            if type(d) == type({}):
                for k,v in d.iteritems():
                    self.attributes += v
                    av_dic = {}
                    for a in v:
                        av_dic.update({a:self.list[self.attributes.index(a)]})
                    self.listdic.update({k:av_dic})
            else:
                self.listdic.update({d:self.list[self.dickeys.index(d)]})










