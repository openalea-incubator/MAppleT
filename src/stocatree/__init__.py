import frame
import tools
import physics
import apex
import growth_unit
import pipe
import leaf
import metamer
import internode
import wood
import fruit
import sequences
import srandom
import tree
import tools 
"""
src/stocatree/constants.py   
src/stocatree/colors.py
src/stocatree/post_analysis.py
src/stocatree/stocatree.py
src/stocatree/config_doc.py    
src/stocatree/output.py     
"""



#import post_analysis

#from tools import *
#from physics import *
#from growth_unit import *
#from pipe import *


from openalea.deploy.shared_data import get_shared_data_path
from os.path import join as pj

def get_shared_data(file):
    import openalea.stocatree
    shared_data_path = get_shared_data_path(openalea.stocatree.__path__)
    #print "FUUUUUUUUUUUCCCCCCCCCCCCCKKKKKKKKKKKKKK : ", type(shared_data_path)
    return str(pj(shared_data_path, file))


