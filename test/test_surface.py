#from openalea.plantik.tools.surface import *
from openalea.stocatree.tools.surface import *

class TestSurface():

    def __init__(self):
        pass
        
    def test_leaf(self):
        s = leafSurface(6)
    def test_ground(self):
        s = groundSurface(12)
    def test_petal(self):
        s = petalSurface(12)
