#-------------------------------------------------------------------------------
# Name:        parameterisation
# Purpose:     Parameterisation for sensitivity analysis
#
# Author:      Han
#
# Created:     04/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

class Pararange(object):
    def __init__(self):
        self.ranges_dic = {
                                "tree" :
                                    {
                                        "branching_angle" : [0, 130]
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


class Parameterise(object):
    def __init__(self, parameter_dic = {},
                    out_dir = "Batchmode_ExpCounters&Results/",
                    parameter_list = []):

        self.parameter_dic = parameter_dic
        """
        The structure of parameter_dic is:
            {
                obj1_name:
                    {
                    attr1_name: attr1_value
                    attr2_name: attr2_value
                    .
                    .
                    .
                    }
                obj2_name:
                    {
                    attr1_name: attr1_value
                    attr2_name: attr2_value
                    .
                    .
                    .
                    }
                .
                .
                .
            }
        Note: the obj_name and attr_name must be the same with their counterparts
              in the ini file.
        """
        self.out_dir = out_dir
        self.parameter_list = parameter_list

        self.parameter_dic.update({"general":{"batch_dir":self.out_dir}})

    def set_value(self):
        sensitivity_input = {
                                "general":
                                    {
                                        "batch_dir": self.out_dir
                                    },
                                "tree" :
                                    {
                                        "branching_angle" : self.parameter_list[0]
                                    },
                                "internode" :
                                    {
                                        "max_length" : self.parameter_list[1]
                                    },
                                "apex" :
                                    {
                                        "maximum_size" : self.parameter_list[2]
                                    },
                                "leaf" :
                                    {
                                        "max_area" : self.parameter_list[3]
                                    }
                            }
        """
        self.parameter_dic = sensitivity_input
        """
        self.parameter_dic.update({"general":{"batch_dir":self.out_dir}})

    def ini_write(self):
        fp = open("C:/Python26/Lib/site-packages/VPlants.StocaTree-0.9.4-py2.6.egg/share/data/Sensitivity_Parameters.ini", "w")
        print self.out_dir
        #fp = open(self.out_dir + "Sensitivity_Parameters.ini", "w")
        #fp = open("Parameters.ini", "w")
        for obj_name,attr_dic in self.parameter_dic.iteritems():
            fp.write("[" + obj_name + "]" + "\n")
            #fp.write(obj_name + "\n")
            for attr_name,attr_value in attr_dic.iteritems():
                fp.write(attr_name + "=" + str(attr_value) + "\n")
        fp.close()


