from openalea.stocatree.leaf import Leaf, AppleLeaf

class test_leaf():
    def __init__(self):

        self.f = Leaf()
        self.f.state = 'growing'
        assert self.f.state=='growing'
        try:
            self.f.state = 'dummy'
            assert False
        except: 
            assert True

        assert self.f.state == 'growing'

    def test_leaf_compute_mass(self):
        try:
           self.f.compute_mass()
           assert False
        except:
            assert NotImplementedError


    def test_compute_area(self):
        self.f.compute_area()

def test_leaf_initialisation():
    f = Leaf()
    try:
        f.initialisation()
        assert False
    except:
        assert NotImplementedError

def test_apple_leaf_state():
    # test set_state/get_state
    f = AppleLeaf()
    f.state = 'growing'
    assert f.state == 'growing'
    try:
        f.state = 'dummy'
        assert False
    except: 
        assert True

    assert f.state=='growing'


class test_apple_leaf():
    def __init__(self):
        self.leaf = AppleLeaf()
        assert self.leaf.max_area == 30*0.01*0.01

    def test_apple_leaf_compute_mass(self):
        self.leaf.age = 50
        mass = self.leaf.compute_mass()

def test_apple_leaf_compute_area_from_func():
    from openalea.stocatree.tools.read_function import ReadFunction
    f = AppleLeaf()
    f.age = 50
    func_leaf_area = ReadFunction('functions.fset', 'leaf_area')
    # first test the preformeed leaves
    mass = f.compute_area_from_func(4, func_leaf_area)
    # and full leaves
    mass = f.compute_area_from_func(14, func_leaf_area)
    # then maturity
    f.age = f.maturation+1
    f.maturity= True
    mass = f.compute_area_from_func(14, func_leaf_area)

def test_apple_leaf_compute_area():
    from openalea.stocatree.tools.read_function import ReadFunction
    f = AppleLeaf()
    #before maturation
    f.age = 8
    f.compute_area(6)
    #after maturation
    f.age = 50
    f.compute_area(6)
    #number below and above 8
    f.compute_area(16)
