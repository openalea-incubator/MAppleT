from openalea.stocatree.tools.simulation import *
from openalea.stocatree import get_shared_data

def test_simu():

    filename = get_shared_data('functions.fset')
    s = SimulationStocatree()
    s.func_leaf_area_init(filename=filename, func_name='leaf_area')


