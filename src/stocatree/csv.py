#-------------------------------------------------------------------------------
# Name:        csv
# Purpose:     to generate csv files
#
# Author:      Han
#
# Created:     02/05/2011
# Copyright:   (c) KELNER 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

class GroupCSV(object):
    def __init__(self, output_directory = "", file_name = "", item_name_list = [], item_value_dict = {}, groupid_list = []):
        self.output_directory = output_directory
        self.file_name = file_name
        self.item_name_list = item_name_list
        self.item_value_dict = item_value_dict
        self.groupid_list = groupid_list

    def open(self):
        self.op = open(self.output_directory + self.file_name, 'a')

    def read(self):
        self.rd = open(self.output_directory + self.file_name, 'r')
        return self.rd.read()

    def clear(self):
        self.c = open(self.output_directory + self.file_name, 'w').close()

    def close(self):
        self.cl = self.op.close()

    def item_names(self):
        for it in self.item_name_list:
            self.op.write(it + ",")
        self.op.write("\n")

    def item_values(self):
        for gid in self.groupid_list:
            for n in self.item_name_list:
                if n in self.item_value_dict:
                    self.op.write(str(self.item_value_dict[n][gid]) + ",")
                else:
                    self.op.write("N/A" + ",")
            self.op.write("\n")


class LstringCSV(GroupCSV):
    def  __init__(self,output_directory = "", file_name = "", exp_info = {}, item_name_list = []):
        self.output_directory = output_directory
        self.file_name = file_name
        self.exp_info = exp_info
        self.item_name_list = item_name_list

    def item_values(self,lstring):
        for k,elt in enumerate(lstring):
            if lstring[k].name == "metamer":
                for n in self.item_name_list:
                    if hasattr(lstring[k][0], n):
                        self.op.write(str(getattr(lstring[k][0], n)) + ",")
                    elif n == "lstring_id":
                        self.op.write(str(k) + ",")
                    elif n in self.exp_info:
                        self.op.write(str(self.exp_info[n]) + ",")
                    else:
                        self.op.write("N/A" + ",")
                self.op.write("\n")

class ExprecCSV(GroupCSV):
    def __init__(self, exp_id, finidate, para_dic, file_name, output_directory):
        self.exp_id = exp_id
        self.finidate = finidate
        self.para_dic = para_dic
        self.file_name = file_name
        self.output_directory = output_directory
        self.exp_info = {"Experiment_ID": self.exp_id, "Finished_Date":self.finidate}
        self.para_dic2= {}

        for k,v in self.para_dic.iteritems():
            for vk,vv in v.iteritems():
                key = k + "_" + vk
                val = vv
                self.para_dic2.update({key:val})

        self.item_name_list = []
        self.item_value_list = []

        for n in self.exp_info.keys():
            self.item_name_list.append(n)
            self.item_value_list.append(self.exp_info[n])

        for n in self.para_dic2.keys():
            self.item_name_list.append(n)
            self.item_value_list.append(self.para_dic2[n])

        self.open()
        if self.read() == "":
            self.item_names()
        self.item_values()
        self.close()

    def item_values(self):
        for v in self.item_value_list:
            self.op.write(str(v) + ",")
        self.op.write("\n")

