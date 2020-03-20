"""
This module was written by Han in April and May, 2011
"""

from openalea.stocatree.csv import GroupCSV, LstringCSV

class Group(object):
    def __init__(self, lstring, group_id_name = '', attribute_list = []):
        # The name for the group id. For example, "parent_unit_id" if this is for the unit level.
        self.group_id_name = group_id_name
        # The list of attributes that are studied here. For example ['length', 'radius']
        self.attribute_list = attribute_list

        # a dictionary to store match between group id and its included metamer ids, {group_id:[id_metamer_1, id_metamer_2, ...]}
        # where the group can be a unit or a branch
        self.group_metamer = {}

        # a dictionary to store mathcn between group id and the ids of its included units. For example, {branch_id: [id_unit_1, id_unit_2, ...]}
        self.group_unit = {}

        # a dictionary to store mathcn between group id and the ids of its included first-order branches. For example, {tree_id: [id_branch_1, id_branch_2, ...]}
        self.group_fbr = {}

        self.group_metamer_attributes = {}

    """
    The id_group method is to fill the
            self.group_metamer dictionary to:
                {
                    group_id1:[metamer_id1, metamer_id2, ...]
                    group_id2:[metamer_id1, metamer_id2, ...]
                    .
                    .
                    .
                }

            self.group_unit dictionary to:
                {
                    group_id1:[unit_id1, unit_id2, ...]
                    group_id2:[unit_id1, unit_id2, ...]
                    .
                    .
                    .

                }

            self.group_fbr dictionary to:
                {
                    tree_id:[fbr_id1, fbr_id2, ...]
                }


    """

    def id_group(self,lstring):
        for i, elt in enumerate(lstring):
            if elt.name == 'metamer':
                # For example, if the value of self.group_id_name is "parent_unit_id",
                # then group_id will have the value of elt[0].parent_unit_id
                group_id = getattr(elt[0], self.group_id_name)

                if group_id in self.group_metamer:
                    self.group_metamer[group_id].append(i)
                else:
                    self.group_metamer.update({group_id:[i]})

                if self.group_id_name != "parent_unit_id":
                    if group_id in self.group_unit:
                        if lstring[i][0].parent_unit_id not in self.group_unit[group_id]:
                            self.group_unit[group_id].append(lstring[i][0].parent_unit_id)
                    else:
                        self.group_unit.update({group_id: [lstring[i][0].parent_unit_id]})

                if self.group_id_name == "parent_tree_id":
                    if group_id in self.group_fbr:
                        if lstring[i][0].parent_fbr_id not in self.group_fbr[group_id]:
                            self.group_fbr[group_id].append(lstring[i][0].parent_fbr_id)
                    else:
                        self.group_fbr.update({group_id: [lstring[i][0].parent_fbr_id]})

    def attr_group(self,lstring):
        self.id_group(lstring)

        # To initialise a dictionary like {attr1_name:{}, attr2_name:{}, ...}
        for attribute in self.attribute_list:
            if attribute not in self.group_metamer_attributes:
                if attribute == "parent_observation":
                    if self.group_id_name == "parent_unit_id":
                        self.group_metamer_attributes.update({attribute:{}})
                else:
                    self.group_metamer_attributes.update({attribute:{}})

        for gid,mid_list in self.group_metamer.iteritems():
            for attr in self.group_metamer_attributes:
                if gid not in self.group_metamer_attributes[attr]:
                    self.group_metamer_attributes[attr].update({gid:[]})
                for mid in mid_list:
                    # Note that the value of attr is a string, thus the "getattr()" method is needed here
                    # to return the value of attribute that corresponds to attr
                    if hasattr(lstring[mid][0],attr):
                        self.group_metamer_attributes[attr][gid].append(getattr(lstring[mid][0],attr))
                    else:
                        self.group_metamer_attributes[attr][gid].append("N/A")


        """
        The above loop is to further extend the dicitonary self.group_metamer_attributes to
        {
            attr1_name:
                {
                    group1_id:[metamer1_attr1, metamer2_attr1, ...],
                    group2_id:[metameri_attr1, metamerj_attr1, ...],
                    .
                    .
                    .
                },
            attr2_name:
                {
                    group1_id:[metamer1_attr2, metamer2_attr1, ...],
                    group2_id:[metameri_attr1, metamerj_attr1, ...],
                    .
                    .
                    .
                },
                .
                .
                .
        }

        """
        """
            if hasattr(elt[0], attribute):
                if attribute in self.group_metamer_attributes:
        """



class Statistics(object):
    def __init__(self, lstring, attribute_list = [], shoot_level = True, branch_level = False, tree_level = False, exp_id = 0, growth_date = 1994, exp_date = 2011, dir = "Batchmode_ExpCounters&Results/"):
        #self.lstring = lstring

        #The list of attributes to be investigated
        self.attribute_list = attribute_list
        #These are used to control which level of the structure that needs to be grouped
        self.shoot_level = shoot_level
        self.branch_level = branch_level
        self.tree_level = tree_level

        self.exp_id = exp_id
        self.growth_date= growth_date
        self.exp_date = exp_date
        self.dir = dir

        self.groupid_values = {}
        self.group_metamer = {}
        self.group_unit = {}
        self.group_fbr = {}

        self.metamer_file_name = "Statistics_Metamer.csv"

        if self.shoot_level:
            self.shoot_avg = self.average(lstring, "parent_unit_id")
            self.output("parent_unit_id", self.shoot_avg)
        if self.branch_level:
            self.branch_avg = self.average(lstring, "parent_fbr_id")
            self.output("parent_fbr_id", self.branch_avg)
        if self.tree_level:
            self.tree_avg = self.average(lstring, "parent_tree_id")
            self.output("parent_tree_id", self.tree_avg)

        self.lstring_details(lstring, self.metamer_file_name)

    # a function to return the average value
    def average(self,lstring, group_id_name):
        group_avg = {}
        """
        group_avg is to be:
        {
            attr1_name:
                {
                    group_id1:average_value1
                    group_id2:average_value2
                }
            attr2_name:
                {
                    group_idi:average_valuei
                    group_idj:average_valuej
                }
            .
            .
            .
        }
        """
        grp = Group(lstring, group_id_name, self.attribute_list)
        grp.attr_group(lstring)

        self.groupid_values.update({group_id_name: grp.group_metamer.keys()})
        """
        The above statement updates groupid_values with:
        {
            group_id_name : [group_id_1, group_id_2, ...]
        }
        The length of the list is therefore the number of groups under this
        grouping method
        """

        self.group_metamer.update({group_id_name: grp.group_metamer})
        """
        The above statement updates group_metamer with:
        {
            group_id_name:
                {
                    group_id1:[metamer_id1, metamer_id2, ...]
                    group_id2:[metamer_id1, metamer_id2, ...]
                    .
                    .
                    .

                }
        }
        Since there are three values for group_id_name to represent the three
        scales (unit, branch, tree), this dictionary could be used to calculate
        the number of metamers in each group at each level. For example, if
        group_id_name is "parent_unit_id", then this dictionary can be used to
        know how many metamers each unit has.
        """

        for attr,groups in grp.group_metamer_attributes.iteritems():
            if attr not in group_avg:
                group_avg.update({attr:{}})
            # Here avl is a list of metamer attribute values
            for gid,avl in groups.iteritems():
                # Since the value of "parent_observation" is a string, it cannot
                # really be averaged
                if attr == "parent_observation" \
                            or attr == "leaf_state"\
                            or attr == "zone":
                    group_avg[attr].update({gid : grp.group_metamer_attributes[attr][gid][0]})
                    #print attr, group_avg[attr]
                else:
                    if len(avl) != 0:
                        # Here it is divided by (len(avl) - avl.count(0)) rather
                        # than len(avl). This is to avoid that, in a branch for
                        # example, there are some metamers without leaves (scar),
                        # thus the average value of leaf area of this branch should
                        # not be calculated from division by the number of metamers
                        # it has.
                        if (len(avl) - avl.count(0)) != 0:
                            a = sum(avl)/(len(avl) - avl.count(0))
                        else:
                            a = 0
                    else:
                        a = 0
                    group_avg[attr].update({gid:a})


        if "star_pgl" in group_avg:
            group_avg.update({"total_star":{}})
            for gid in grp.group_metamer.keys():
                if sum(grp.group_metamer_attributes["ta_pgl"][gid]) !=0:
                    group_avg["total_star"].update({gid: sum(grp.group_metamer_attributes["sa_pgl"][gid])/sum(grp.group_metamer_attributes["ta_pgl"][gid])})
                else:
                    group_avg["total_star"].update({gid: 0})

        self.gp_stat_updt(group_avg, "metamer_number")
        self.gp_stat_updt(group_avg, "leaf_number")
        for gid,v in self.group_metamer[group_id_name].iteritems():
            #group_avg["metamer_number"].update({gid: len(v)})
            #Modified by Han on 12-01-2012, because there are two extra elements
            #lstring[0] and lstring[1] in the pseudo lstring
            if gid > 0:
                group_avg["metamer_number"].update({gid: len(v)})
            else:
                group_avg["metamer_number"].update({gid: (len(v)-2)})
            if "leaf_area" in grp.group_metamer_attributes:
                if gid > 0:
                    group_avg["leaf_number"].update({gid: (len(grp.group_metamer_attributes["leaf_area"][gid]) - grp.group_metamer_attributes["leaf_area"][gid].count(0))})
                else:
                    group_avg["leaf_number"].update({gid: (len(grp.group_metamer_attributes["leaf_area"][gid]) - grp.group_metamer_attributes["leaf_area"][gid].count(0) - 2)})
            else:
                group_avg["leaf_number"].update({gid: 0})
                for i in v:
                    if lstring[i][0].leaf_state == "growing":
                        group_avg["leaf_number"][gid] += 1
            assert group_avg["leaf_number"][gid] <= group_avg["metamer_number"][gid]


        """
        The above statement and loop updates the group_avg dictionary with:
        {
            "metamer_number":
                {
                    gid_i: metamer_number_i
                    .
                    .
                    .
                }

            "leaf_number":
                {
                    gid_i: leaf_number_i
                    .
                    .
                    .
                }
        }
        """

        if group_id_name != "parent_unit_id":
            self.group_unit.update({group_id_name: grp.group_unit})
            self.gp_stat_updt(group_avg, "unit_number")
            for gid,v in self.group_unit[group_id_name].iteritems():
                group_avg["unit_number"].update({gid: len(v)})
            if group_id_name == "parent_tree_id":
                self.group_fbr.update({group_id_name: grp.group_fbr})
                self.gp_stat_updt(group_avg, "fbr_number")
                for gid,v in self.group_fbr[group_id_name].iteritems():
                    group_avg["fbr_number"].update({gid: len(v)})

        return group_avg


    # This method is used to output the grouped resutls at shoot, branch or tree levels
    def output(self, group_id_name, group_stat):
        #self.exp_info = ["Experiment_ID", "Growth_Date", "Experiment_Date"]
        self.exp_info = {"Experiment_ID": self.exp_id, "Growth_Date": self.growth_date, "Experiment_Date":self.exp_date}
        #self.group_id_info = [group_id_name]
        #self.line_feed = ["\n"]
        #self.item_name_list = self.exp_info + self.group_id_info + self.attribute_list

        group_output = group_stat

        for name,value in self.exp_info.iteritems():
            if name not in group_output.keys():
                group_output.update({name:{}})
            for gid in self.groupid_values[group_id_name]:
                group_output[name].update({gid:value})
        """
        The above loop updates group_output with:
        {
            exp_info1_name:
                {
                    group_id1 : exp_info1_value
                    group_id2 : exp_info1_value
                }
            exp_info2_name:
                {
                    group_id1 : exp_info2_value
                    group_id2 : exp_info2_value
                }
            .
            .
            .
        }
        """

        group_output.update({group_id_name:{}})
        for gid in self.groupid_values[group_id_name]:
            group_output[group_id_name].update({gid:gid})
        """
        The above statement and loop update group_output with:
        {
            group_id_name:
                {
                    group_id1 : group_id1
                    group_id2 : grouo_id2
                }
        }
        """



        item_name_list = self.exp_info.keys() + [group_id_name] + self.attribute_list + ["total_star", "metamer_number", "leaf_number"] + ["unit_number", "fbr_number"]

        self.shoot_file_name = "Statistics_Shoot.csv"
        self.branch_file_name = "Statistics_Branch.csv"
        self.tree_file_name = "Statistics_Tree.csv"

        if group_id_name == "parent_unit_id":
            fn = self.shoot_file_name
        elif group_id_name == "parent_fbr_id":
            fn = self.branch_file_name
        elif group_id_name == "parent_tree_id":
            fn = self.tree_file_name

        csv = GroupCSV(self.dir, fn, item_name_list, group_output, self.groupid_values[group_id_name])
        csv.open()
        #if (self.exp_id == -1 or self.exp_id == 0) and self.growth_date == 1994:
        if csv.read() == '':
            #csv.clear()
            csv.item_names()
            csv.item_values()
        else:
            csv.item_values()
        csv.close()

    # This method is used to output attributes of each metamer
    def lstring_details(self, lstring, file_name):
        item_name_list = self.exp_info.keys() + ["lstring_id"] + self.attribute_list + ["leaf_state"]
        fn = file_name
        csv = LstringCSV(self.dir, fn, self.exp_info, item_name_list)
        csv.open()
        if csv.read() == '':
            csv.item_names()
        csv.item_values(lstring)
        csv.close()


    def gp_stat_updt(self, group_stat, attribute_name):
        if attribute_name not in group_stat:
            group_stat.update({attribute_name: {}})



