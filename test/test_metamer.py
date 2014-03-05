from openalea.stocatree.metamer import *
# the following two functions are not accessible in __all__so, we need to be explicit
# this one is required by leaf_area
from openalea.stocatree.tools.read_function import ReadFunction
from vplants.plantgl.all import Vector3



def test_reaction_wood_target():
    up = Vector3(1.,1.,1.)
    heading = Vector3(1.,0.,-0.)
    previous_heading = Vector3(-1.,-1.,-1.)

    reaction_wood_target(up, heading, previous_heading)

    #r statement
    up = Vector3(0.,0.,1.)
    heading = Vector3(0.,1.,0.)
    previous_heading = Vector3(3.1,1.,1.)
    reaction_wood_target(up, heading, previous_heading)

def test_cambial():
    c = cambial_layer()
    assert c.thickness==0
    assert c.radius==0
    assert c.reaction_wood==0
    assert c.second_moment_of_area==0

class test_metamer_data():

    def __init__(self):
        from openalea.stocatree.wood import Wood
        from openalea.stocatree.fruit import AppleFruit
        from openalea.stocatree.leaf import AppleLeaf
        from openalea.stocatree.internode import Internode
        from openalea.stocatree.physics import Frame
        try:
            self.data = metamer_data(hlu=Frame(), wood=None, leaf=AppleLeaf(), fruit=AppleFruit(), internode=Internode())
        except:
            assert True
        try:
            self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=None, fruit=AppleFruit(), internode=Internode())
        except:
            assert True
        try:
            self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=None, internode=Internode())
        except:
            assert True
        try:
            self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=AppleFruit(), internode=None)
        except:
            assert True
        try:
            self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=AppleFruit(), internode=Internode(), zone='dummy')
        except:
            assert True
        self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=AppleFruit(), internode=Internode(), floral=True)
        self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=AppleFruit(), internode=Internode(), floral=True)
        self.data = metamer_data(hlu=Frame(), wood=Wood(), leaf=AppleLeaf(), fruit=AppleFruit(), internode=Internode(),number=2)
        print self.data 

        from openalea.stocatree.tools.simulation import SimulationStocatree
        self.sim = SimulationStocatree(dt=1)

    def test_organ_activity(self):
        self.data.organ_activity(self.sim)
        self.sim.events.harvest._active = True
        self.data.organ_activity(self.sim)
        self.data.fruit._state='flower'
        self.data.age=50
        for i in range(1,10):
            self.data.organ_activity(self.sim)


    def test_update_parameters(self):
        self.data.update_metamer_parameters(self.sim)

    def test_compute_mass(self):
        self.data.compute_mass()
        #self.data.compute_mass(mr=1)
        #self.data.compute_mass(mr=1,mb=1)
    
    def test_calculate_rotation_velocity(self):
        self.data.trunk = True
        self.data.calculate_rotation_velocity(self.sim)
        self.sim.events.harvest._active = True
        self.data.pre_harvest_mass = 1
        self.data.calculate_rotation_velocity(self.sim, stake=False)


    def test_update_position(self):
        from vplants.plantgl.all import Vector3
        self.data.update_position()
        self.data.update_position(left_metamer_position=Vector3(1,1,1))

def test_clamp():
    """TO FINALISE"""
    v = Vector3(0.000001, 1,1)
    clamp_v3d_components_if_near_zero(v)



