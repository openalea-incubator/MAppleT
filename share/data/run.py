import openalea.lpy as lpy
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree import get_shared_data

conf = ConfigParams(get_shared_data('stocatree.ini'))
conf.internode.max_length = 0.05
l = lpy.Lsystem("stocatree.lpy")
#l = lpy.Lsystem("cnt.lpy")
l.context()["options"] = conf
l.context()["v"] = 6
l.animate()
#l.iterate()
#print l.context()["options"].internode.max_length