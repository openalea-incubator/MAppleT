"""
This surface/area calculation part of this module was co-developed by Da Silva, Boudon and Han in April, 2011.
The rest functionalities were written by Han in April and May, 2011.
"""
from openalea.plantgl.all import *
from openalea.fractalysis.light.directLight import diffuseInterception
#from vplants.fractalysis.light.directLight import diffuseInterception
import openalea.fractalysis.fractutils as fruti
import openalea.fractalysis.light as lit
import openalea.plantgl.all as pgl
import os, shutil
from openalea.stocatree.rw_tools import Ensure_dir

"""
def metamer_star(scene):
    Viewer.display(scene)
    d = diffuseInterception(scene)
    sc = dict()
    for sh in scene:
        # If the surface is not the ground (with id 0)
        if sh.id > 0:
            sc[sh.id] = sc.get(sh.id,[])+[sh]
            #print sh.id, sc[sh.id].appearance.getName()
        #print "######", sh.id, sh.appearance.getName()

    #for shape in sc[2]:
        #print shape.appearance.getName()

    # Total surface of each metamer #
    # Each "id" here corresponds to a metamer, thus the elements of a metamer,
    # including its leaf blade, petiole and internode, have the same id. Each
    # element also corresponds to its own shape, thus the total surface (namely,
    # area) of a memater is equivalent to the sum of surface values of all its
    # elements.
    totsurface = dict([(id,sum([surface(i) for i in shapes])) for id, shapes in sc.iteritems()])

    # If the total surface area of each metamer needs to be returned:
    mt_star = dict([(id ,[d[id],surf,d[id]/surf]) for id,surf in totsurface.iteritems()])
    return mt_star

def leaf_star(scene):
    Viewer.display(scene)
    sc = dict()
    for sh in scene:
        # If the surface is not the ground (with id 0)
        if sh.id > 0:
            sc[sh.id] = sc.get(sh.id,[])+[sh]

    # Total surface of each metamer #
    # Each "id" here corresponds to a metamer, thus the elements of a metamer,
    # including its leaf blade, petiole and internode, have the same id. Each
    # element also corresponds to its own shape, thus the total surface (namely,
    # area) of a memater is equivalent to the sum of surface values of all its
    # elements.
    totsurface = dict([(id,sum([surface(i) for i in shapes])) for id, shapes in sc.iteritems()])

    # leaf surface only #
    leafsurface = dict()
    for id, shapes in sc.iteritems():
        for shape in shapes:
            # "Color_19" is the color of internode (wood part).
            # This is to reduce the surface of this wood part so that the leaf
            # surface can be calculated.
            if shape.appearance.getName() == "Color_19":
                leafsurface[id] = totsurface[id] - surface(shape)
                shape.id = 999999999
            #print id, shape.id

    d = diffuseInterception(scene)

    # If only the leaf area (total metamer area - internode area) needs to be returned:
    #lf_star = dict([(id ,[d[id],surf,d[id]/surf]) for id,surf in leafsurface.iteritems()])
    #lf_star = dict([(id ,[d[id],leafsurface[id],d[id]/surf]) for id,v in d.iteritems()])
    #for k,v in d.iteritems():
    lf_star = {}
    for id,surf in leafsurface.iteritems():
        if id in d:
            ud = {id : [d[id], surf, d[id]/surf]}
            lf_star.update(ud)

    return lf_star
"""

class STAR(object):
    def __init__(self, lstring, scene):

        # a list to store the id of each leaf
        self.id_lf = []
        # a dictonary to store total area of each leaf, {id : total_area}
        self.ta_lf = {}
        # a dictonary to store silhouette area of each leaf, {id : silhouette_area}
        self.sa_lf = {}
        # a dictonary to store STAR value of each leaf, {id : star}
        self.star_lf = {}

        # a dictionary to store match between unit id and its included leaf ids, {unit_id:[id_lf_1, id_lf_2, ...]}
        self.unit_leaves = {}
        # a dictionary to store match between unit id and its included metamer ids, {unit_id:[id_lf_1, id_lf_2, ...]}
        # Note: self.unit_metamers contains all metamers while self.unit_leaves only contains leaves that were "detected" by diffuseInterception
        self.unit_metamers= {}

        # {unit_id : [leaf_area_1, leaf_area_2, ...]}
        self.ta_st = {}
        # {unit_id : [silhouette_area_1, silhouette_area_2, ...]}
        self.sa_st = {}
        # {unit_id : [star_leaf_1, star_leaf_2, ...]}
        self.star_st= {}

        # average value of leaf areas for each shoot, {unit_id : average_leaf_area}
        self.avg_ta_st = {}
        # average value of silhouette areas for each shoot, {unit_id : average_silhouette_area}
        self.avg_sa_st = {}
        # mean of all star values per shoot, sum(star_values)/count(star_values)
        self.mean_star_st = {}
        # total star per shoot, sum(silhouette_areas)/sum(leaf_areas)
        self.total_star_st = {}

    # a method to collect star and relevant data for each leaf (wooden part removed)
    def collect(self, lstring, scene):
        sc = dict()
        for sh in scene:
            # If the surface is not the ground (with id 0)
            if sh.id > 0:
                sc[sh.id] = sc.get(sh.id,[])+[sh]

        # Total surface of each metamer #
        # Each "id" here corresponds to a metamer, thus the elements of a metamer,
        # including its leaf blade, petiole and internode, have the same id. Each
        # element also corresponds to its own shape, thus the total surface (namely,
        # area) of a memater is equivalent to the sum of surface values of all its
        # elements.
        totsurface = dict([(id,sum([surface(i) for i in shapes])) for id, shapes in sc.iteritems()])

        # leaf surface only #
        leafsurface = dict()
        for id, shapes in sc.iteritems():
            for shape in shapes:
                # "Color_19" is the color of internode (wood part).
                # This is to reduce the surface of this wood part so that the leaf
                # surface can be calculated.
                if shape.appearance.getName() != "Color_15":
                    leafsurface[id] = totsurface[id] - surface(shape)
                    shape.id = 999999999
                #print id, shape.id

        d = diffuseInterception(scene)
        # Note: the surface returned by plantGL is in 10m*10m
        # Thus this value need to be divided by 100 to calculate the real surface in m*m
        for id,surf in leafsurface.iteritems():
            if id in d:
                self.id_lf.append(id)
                self.ta_lf.update({id:surf/100})
                lstring[id][0].ta_pgl = surf/100
                if d[id] <= surf:
                    self.sa_lf.update({id:d[id]/100})
                    self.star_lf.update({id:d[id]/surf})
                    lstring[id][0].sa_pgl = d[id]/100
                    lstring[id][0].star_pgl = d[id]/surf
                    #print id, d[id], surf, lstring[id][0].leaf.age, lstring[id][0].leaf.state
                else:
                    # If silhouette area is larger than leaf area, the "surface" will be returned as silhouette area
                    # and star will be returned as 1
                    self.sa_lf.update({id:surf/100})
                    self.star_lf.update({id:1})
                    lstring[id][0].sa_pgl = surf/100
                    lstring[id][0].star_pgl = 1

                    print "###########################################################################################################################################"
                    print id, d[id], surf, lstring[id][0].leaf.age, lstring[id][0].leaf.state
                    print "###########################################################################################################################################"

        if lstring[id][0].leaf.state == 'scar':
             lstring[id][0].ta_pgl = 0
             lstring[id][0].sa_pgl = 0
             lstring[id][0].star_pgl = 0


    def process_shoot(self, lstring, scene):
        # To group data from leaf scale to shoot scale
        for k in self.id_lf:
            if lstring[k][0].parent_unit_id in self.unit_leaves:
                self.unit_leaves[lstring[k][0].parent_unit_id].append(k)
                self.ta_st[lstring[k][0].parent_unit_id].append(self.ta_lf[k])
                self.sa_st[lstring[k][0].parent_unit_id].append(self.sa_lf[k])
                self.star_st[lstring[k][0].parent_unit_id].append(self.star_lf[k])
            else:
                self.unit_leaves.update({lstring[k][0].parent_unit_id:[k]})
                self.ta_st.update({lstring[k][0].parent_unit_id:[self.ta_lf[k]]})
                self.sa_st.update({lstring[k][0].parent_unit_id:[self.sa_lf[k]]})
                self.star_st.update({lstring[k][0].parent_unit_id:[self.star_lf[k]]})

        # To calculate statistic result at shoot scale
        for k,v in self.unit_leaves.iteritems():
            self.avg_ta_st.update({k : sum(self.ta_st[k])/len(self.ta_st[k])})
            self.avg_sa_st.update({k : sum(self.sa_st[k])/len(self.sa_st[k])})
            self.mean_star_st.update({k : sum(self.star_st[k])/len(self.star_st[k])})
            self.total_star_st.update({k : sum(self.sa_st[k])/sum(self.ta_st[k])})

        for i, elt in enumerate(lstring):
            if elt.name == 'metamer':
                if elt[0].parent_unit_id in self.unit_metamers:
                    self.unit_metamers[elt[0].parent_unit_id].append(i)
                else:
                    self.unit_metamers.update({elt[0].parent_unit_id:[i]})


        """
        for k,v in self.unit_leaves.iteritems():
            #print k, len(v)
            #print k, len(self.ta_st[k])
            print "-----------------------------------------------------------------------------------"
            print k, self.avg_sa_st[k], self.avg_ta_st[k], self.mean_star_st[k], self.total_star_st[k]
            print k, self.star_st[k]
            print "-----------------------------------------------------------------------------------"
            #print self.unit_metamers[k]
        """


"""
def STAR(lstring,scene):
    s = Scene(scene)

    # Calculation of STAR for each leaf
    ret = leaf_star(s)

    print "###STAR of Each Leaf###"
    print "ID : [silhouette area, surface area, STAR]"

    for k,v in ret.iteritems():
        #assert v[2] <= 1
        print lstring[k][0].parent_unit_id, lstring[k][0].parent_observation, k, lstring[k].name, ":", v
        if v[2] > 1:
            print "####################################################################################################################################"
        #if v[2] > 1:
            #print lstring[k][0].parent_unit_id, lstring[k][0].parent_observation, k, ":", v
    #for k,v in ret.iteritems():
        #assert v[2] <= 1
"""

class Envelope(object):
	def __init__(self, id_dict, scene, output_dir = "Envelope\\"):
		self.id_dict = id_dict
		self.scene = scene
		self.expname = self.get_expname()
		self.crrt_dir = os.getcwd()
		self.output_dir = output_dir

	def get_expname(self):
		(f_path, f_name) = os.path.split(self.scene)
		(f_short_name, f_extension) = os.path.splitext(f_name)
		return f_short_name

	def crt_opt_dir(self):
		Ensure_dir(self.output_dir)

	def intercept(self):
            self.crt_opt_dir()
            sc = pgl.Scene(self.scene)
            scc=fruti.centerScene(sc)

            ss = lit.ssFromDict(self.expname, scc, self.id_dict, "CvxHull")
            ss.checkFactor(150,150,8)
            sc1=ss.genScaleScene(1)
            sc2=ss.genScaleScene(2)
            sc3=ss.genScaleScene(3)
            sc4=ss.genScaleScene(4)
            sc1.save(self.output_dir+self.expname+"_"+"1.bgeom")
            sc2.save(self.output_dir+self.expname+"_"+"2.bgeom")
            sc3.save(self.output_dir+self.expname+"_"+"3.bgeom")
            sc4.save(self.output_dir+self.expname+"_"+"4.bgeom")

            for i in range(1,47):
                ss.computeDir(skt_idx=i, distrib=[['R','R','R'],['A','R','R'],['A','A','R'], ['A','A','A']])
            shutil.move(self.expname, self.output_dir)
            print "######################"
