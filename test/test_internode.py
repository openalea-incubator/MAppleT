from openalea.stocatree.internode import *


def test_internode():
    i = Internode()
    i.growth_rate(None) == 0.003
    i.growth_rate('dormant_start') == 0.005
    i.growth_rate('small') == 0.005
    i.growth_rate('diffuse') == 0.0023
    i.growth_rate('medium') == 0.0027
    i.growth_rate('floral') == 0.003
    i.growth_rate('dormant_end') == 0.0006
    i.growth_rate('whatever') == 0.002



