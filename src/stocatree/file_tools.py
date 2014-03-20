#-------------------------------------------------------------------------------
# Name:        file_tools
# Purpose:     data file management
#
# Author:      HAN
#
# Created:     16/12/2011
# Copyright:   (c) HAN 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------





import glob
import os
import sys
#from amlPy   import *
#from openalea.plantgl.all import *
import cPickle
from openalea.stocatree.metamer import metamer_data
#from openalea.mtg.aml import VtxList

class File_Index(object):
    def __init__(self, dir):
        #The directory of files (e.g. "c:\\")
        self.dir = dir
        #The extension of files (e.g. "txt")
        #self.extn = extn

    #The list of paths of all the files (e.g. ["e:\\hi.txt"])
    def path_list(self, extn):
        #Get the lis of files with full directories (not sorted yet)
        p_l = glob.glob(self.dir+"*."+extn)
        return p_l

    #The list of files full names including their extensions (e.g. ["hi.txt"])
    def file_list(self, extn):
        f_l = []
        for p in self.path_list(extn):
            (d,f) = os.path.split(p)
            f_l.append(f)
        return f_l

    #The list of file names (e.g. ["hi"])
    def fn_list(self, extn):
      fn_l = []
      for f in self.file_list(extn):
        (n,e) = os.path.splitext(f)
        fn_l.append(n)
      #return fn_l
      #If the file names are pure integers, then sort them with "their values"
        try:
            #Convert them into int type at first
            for i in range(len(fn_l)):
                fn_l[i] = int(fn_l[i])
            #And then sort the int numbers
            fn_l.sort()
            #And then convert them back to str type
            for i in range(len(fn_l)):
                fn_l[i] = str(fn_l[i])
            return fn_l
        except:
            return fn_l

    #A dictionary of file names and their FULL directories
    #(e.g. {"1":"c:\\1.txt"})
    def file_dic(self, extn):
        dic = {}
        for p in self.path_list(extn):
            (d,f) = os.path.split(p)
            (n,e) = os.path.splitext(f)
            dic.update({n:p})
        return dic

class Mtg_Processing(object):
    def __init__(self, myfile, \
                    attr_list=["observation", "length", "leaf_state", \
                                "leaf_area", "ta_pgl", "sa_pgl", \
                                "star_pgl", "unit_id", "branch_id", \
                                "lstring_id", "zone", "radius"]):
        #File path + file name
        self.file = myfile
        self.mtg = MTG(self.file)
        self.pf = None
        self.attr_list = attr_list

        #The id_dict (actually a list of dictionaries) needed for using envelope
        #self.id_dict = self.crt_envdic()
        #The attribute dictionary needed for producing pseudo lstring
        self.attr_dict = self.get_attributes()
        #The pseudo_lstring as a list
        #self.pseudo_lstring = self.crt_pseudo_lstring()

    def diam(self, x):
        topdia = Feature(x, "TopDia")
        if not topdia is None:
            return topdia / 10.
        else:
            if x != MTGRoot():
                raise Exception("An item, other than the root, in the MTG without a TopDia was found")
            return None

    def leaf_area(self, vtx):
        return Feature(vtx, "leaf_area")

    def leaf_state(self, vtx):
        return Feature(vtx, "leaf_state")

    def id(self, vtx):
        return Feature(vtx, "lstring_id")

    def chemin(self,vtx):
        test_list = []
        chemin_list = []
        for a in Ancestors(vtx):
            if Successor(a) !=  Undef \
                    and Class(a) == "G" \
                    and Pos(Ancestors(vtx), Successor(a)) == Undef:
                test_list.append(a)
        if Size(test_list) > 0:
            for a in Ancestors(vtx):
                if a not in Ancestors(test_list[0]):
                    chemin_list.append(a)
        return chemin_list

    def gu_list(self, vtx):
        return Components(vtx, Scale=2)

    def it_list(self, vtx):
        return Components(vtx, Scale=3)

    def it_leaf_list(self, vtx):
        it_leaf = []
        for d in Descendants(vtx, Scale=3):
            if self.leaf_area(d)>0:
                it_leaf.append(d)
        return it_leaf

    def br_order(self, vtx, _order, plant_frame):
        p_tab = []
        br_order_list = []
        for i in Extremities(self.gu_list(vtx)[0]):
            if i not in [self.gu_list(vtx)[0]]:
                c = self.chemin(i)
                if c != Undef and c!=[]:
                    #This p_tab is filtered, equivalent to the "filter(tab(p))"
                    p_tab.append(c)
        for x in p_tab:
            if Order(x[-1]) == _order:
                br_order_list.append(x)
        return br_order_list

    def leafygu(self, y):
        if y!=2:
            return [x for x in Descendants(y) if self.leaf_area(Components(x)[0])>0 and Class(Father(x))!="I" and Feature(Father(x), "year")!= Feature(x, "year") ]
        else:
            return [x for x in Descendants(y) if Order(x)==Order(y) and self.leaf_area(Components(x)[0])>0 and Class(Father(x))!="I" and Feature(Father(x), "year")!= Feature(x, "year") ]

    #Create the dictionaries for using fractalysis envelope
    def crt_envdic(self):
        self.branch_1 = self.br_order(1, 1, self.pf)
        self.roots_branch_1 = [2] + [i[-1] for i in self.branch_1]
        self.branch_2 = self.br_order(1, 2, self.pf)
        self.roots_branch_2 = [Components(i[-1])[0] for i in self.branch_2]
        self.branch_3 = self.br_order(1, 3, self.pf)
        self.roots_branch_3 = [Components(i[-1])[0] for i in self.branch_3]

        self.ss1 = {0: self.roots_branch_1}

        def dict_crt_gu():
            dic = {}
            for x in self.roots_branch_1:
                dic.update({x: []})
                for y in self.leafygu(x):
                    dic[x].append(Components(y)[0])
            return dic

        self.ss2 = dict_crt_gu()
        self.root_gu = Flatten(self.ss2.values())

        def dict_crt_leaf():
            dic = {}
            for x in self.root_gu:
                dic.update({x: []})
                for y in self.it_leaf_list(x):
                    dic[x].append(self.id(y))
            return dic

        self.ss3 = dict_crt_leaf()

        self.sss1 = {0:[]}
        self.sss2 = {}
        self.sss3 = {}

        for k,v in self.ss2.iteritems():
            new_key = 300000+k
            new_v = []
            for i in v:
                new_i = 600000+i
                new_v.append(new_i)
            self.sss2.update({new_key:new_v})
            if k in Flatten(self.ss1.values()):
                self.sss1[0].append(new_key)

        for k,v in self.ss3.iteritems():
            new_key = 600000+k
            self.sss3.update({new_key:v})

        #self.id_dict = [self.sss1, self.sss2, self.sss3]
        #return self.id_dict
        return [self.sss1, self.sss2, self.sss3]

        """
        self.dtprint = open("dtprint", "w")
        for i in self.id_dict:
            for k,v in i.iteritems():
                self.dtprint.write(str(k)+"---"+str(v)+"\n"+"\n")
            self.dtprint.write("\n"+"##########################"+"\n")
        self.dtprint.close()

        self.id_file = open("id_dict", "w")
        cPickle.dump(self.id_dict, self.id_file, 0)
        self.id_file.close()
        """

    def get_attributes(self):
        v_dic = {}
        for vtx in VtxList(Scale=3):
            lid = Feature(vtx, "lstring_id")
            v_dic.update({lid:{}})
            for attr in self.attr_list:
                v_dic[lid].update({attr:Feature(vtx, attr)})
        return v_dic
        #The keys for v_dic are lstring_ids
        """
        {
            #lstring_id
            1:
                {
                    "leaf_state": "growing",
                    "branch_id": 1,
                    "lstring_id": 1,
                    ...
                }
            #lstring_id
            2:
                {
                    "leaf_state": "growing",
                    "branch_id": 1,
                    "lstrint_id":2,
                    ...
                }
            ...
        }
        """

    def crt_pseudo_lstring(self):
        #The size of the pseudo lstring list, which is the maximum lstring id
        #plus 1, rather than the number of lstring_ids (keys in get_attributes)
        #This allows the pseudo_lstring[id] to work like lstring[id]
        pl_size = max(self.attr_dict.keys()) + 1
        #The pseudo_lstring list
        ###e = L_Element()
        ###e.append(Metamer_Format())
        ###pl = [e] * pl_size
        ######The above line needs to be changed######
        ##################!!!!!!!!!!!!!!!!!!NOTE!!!!!!!!!!!!!!!!!!##################
        #Be careful of the use of initialisation like
        #        self.pseudo_lstring = [e] * len(self.lstring)
        #The drawback is that, if self.pseudo_lstring[i] is updated, e will be
        #updated and then all other elements in self.pseudo_lstring will be
        #updated with the same changes too. The result is that, all elements
        #of self.pseudo_lstring are identical at last.
        ############################################################################

        pl = [None] * pl_size
        for i in range(len(pl)):
            pl[i] = L_Element()
            pl[i].append(Metamer_Format())


        #pl = [None] * pl_size
        for k in self.attr_dict.keys():
            d = Metamer_Format()
            for attr, value in self.attr_dict[k].iteritems():
                if attr in vars(d).keys():
                    vars(d)[attr] = self.attr_dict[k][attr]
                else:
                    if attr == "branch_id":
                        d.parent_fbr_id = self.attr_dict[k][attr]
                    elif attr == "unit_id":
                        d.parent_unit_id = self.attr_dict[k][attr]
                    elif attr == "observation":
                        d.parent_observation = self.attr_dict[k][attr]
                        #print attr, d.parent_observation
                    elif attr == "leaf_state":
                        d.leaf_state = self.attr_dict[k][attr]
                        d.leaf.state = d.leaf_state
                    else:
                        vars(d).update({attr: value})
                        d.parent_tree_id = 0
            #print d.lstring_id
            ne = L_Element()
            ne.append(d)
            pl[k] = ne
            #print e.name
            #print "############################"
            #print len(pl[k])
            #print k, pl[k].name, pl[k][0].lstring_id
            #print k, self.attr_dict[k]["lstring_id"]

        return pl

#A data format/type for elements in pseudo_lstring[i][0]
class Metamer_Format(object):
    def __init__(self):

        self.parent_unit_id = -1
        self.parent_fbr_id = -1
        self.parent_tree_id = -1

        self.leaf_state = ""
        self.leaf_area = 0
        self.ta_pgl = 0
        self.sa_pgl = 0
        self.star_pgl = 0

        self.length = 0
        self.radius = 0

        self.parent_observation = ""
        self.zone = ""

        self.leaf = Leaf_Format()

class Leaf_Format(object):
    def __init__(self):
        self.state = ""

class L_Element(list):
    def __init__(self):
        self.name = "metamer"

#A class to copy information from a real lstring to a pseudo lstring
class Cp_Lstring(object):
    def __init__(self, lstring):
        self.lstring = lstring
        self.pseudo_lstring = None
    def copy(self):
        ###e = L_Element()
        ###e.append(Metamer_Format())
        #print len(lstring)
        self.pseudo_lstring = [None] * len(self.lstring)
        for i  in range(len(self.pseudo_lstring)):
            self.pseudo_lstring[i] = L_Element()
            self.pseudo_lstring[i].append(Metamer_Format())

        ###self.pseudo_lstring = [e] * len(self.lstring)
        ##################!!!!!!!!!!!!!!!!!!NOTE!!!!!!!!!!!!!!!!!!##################
        #Be careful of the use of initialisation like
        #        self.pseudo_lstring = [e] * len(self.lstring)
        #The drawback is that, if self.pseudo_lstring[i] is updated, e will be
        #updated and then all other elements in self.pseudo_lstring will be
        #updated with the same changes too. The result is that, all elements
        #of self.pseudo_lstring are identical at last.
        ############################################################################


        #print len(pseudo_lstring)
        #print vars(lstring[1][0]).keys()
        #print isinstance(lstring[2][0], metamer_data)
        #print len(lstring), len(self.pseudo_lstring)

        for i in range(len(self.pseudo_lstring)):
          try:
            for attr in vars(self.pseudo_lstring[i][0]).keys():
              if attr in vars(self.lstring[i][0]).keys():
                if attr == "leaf_state":
                  self.pseudo_lstring[i][0].leaf_state = self.lstring[i][0].leaf_state
                  self.pseudo_lstring[i][0].leaf.state = self.lstring[i][0].leaf.state
                  #print i, self.lstring[i][0].leaf.state, self.pseudo_lstring[i][0].leaf.state, self.pseudo_lstring[i-1][0].leaf.state
                else:
                  vars(self.pseudo_lstring[i][0])[attr] = vars(self.lstring[i][0])[attr]
                  #print i, self.lstring[i][0].leaf_area, self.pseudo_lstring[i][0].leaf_area
              else:
                continue
          except:
            continue

        """
        for i in range(len(self.pseudo_lstring)):
            try:
                print i, self.lstring[i][0].leaf.state, self.pseudo_lstring[i][0].leaf.state
                print i, self.lstring[i][0].leaf_area, self.pseudo_lstring[i][0].leaf_area
                print i, self.lstring[i][0].length, self.pseudo_lstring[i][0].length
            except:
                continue
        """
        """
        tp = open("check.txt", "w")
        for i in range(len(self.pseudo_lstring)):
            try:
                tp.write("{0}, {1}, {2}\n".format(i, self.lstring[i][0].leaf.state, self.pseudo_lstring[i][0].leaf.state))
                tp.write("{0}, {1}, {2}\n".format(i, self.lstring[i][0].leaf_area, self.pseudo_lstring[i][0].leaf_area))
                tp.write("{0}, {1}, {2}\n".format(i, self.lstring[i][0].length, self.pseudo_lstring[i][0].length))
            except:
                continue
        tp.close()
        """

#A class for merging statistical files (not ubiquitous for all situations)
class Merge(object):
    def __init__(self, src_files=[], dst_file=None, header="Experiment_Date"):
        #A list of source files, with full directories, which need to be merged
        #e.g. ["c:/1.txt", "c:/2.txt", "c:/3.txt"]
        self.src_files = src_files
        #The destination file for the merging
        self.dst_file = dst_file
        #The header to help in deciding whether a line needs to be copied or not
        self.header = header

        #Copy all content, including the header line, of the first file,
        #src_files[0], to the destination file
        opr = open(self.src_files[0], "r")
        opw = open(self.dst_file, "a")
        opw.write(opr.read())
        #opw.write("\n")
        opr.close()
        #Then copy and paste the content of other files, excluding the headings
        for i in range(len(src_files)):
            if i > 0:
                opr = open(src_files[i], "r")
                for line in opr:
                    if header not in line:
                        opw.write(line)
                    else:
                        continue
                #opw.write("\n")
                opr.close()
            else:
                continue
        opw.close()

#This is used to find some missed simulations according to the plan
class Find_missed(object):
    def __init__(self, file="PararunResults/IntegratedMultiScaleStar.csv",  plan_size=300, group_size=5, csv_delimiter=";"):
        op = open(file, "r")
        content = op.read()
        op.close()

        counters = [0] * plan_size

        for i in range(plan_size):
            search_target = csv_delimiter + str(i) + csv_delimiter
            if search_target not in content:
                print i, "is not there", "\n"
            elif content.count(search_target) < 5:
                print i, "is not five", "\n"
            elif content.count(search_target) > 5:
                print i, "is more than five", "\n"

        """
        for i in range(len(counters)):
            if counters[i] < group_size:
                print i, "is not five", "\n"
        """



