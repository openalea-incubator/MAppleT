from openalea.stocatree.output import *
import os
import random
from openalea.plantik.tools.config import *



tolerance = 1e-16

class test_data():
    def __init__(self):
        options = ConfigParams('config.ini')
        #options = {'tag':None,'sequences':True,'l_string':True,'counts':True,'mtg':True, 'trunk':True}

        self.data = Data(options=options)

    def test_init(self):
        self.data.init()

    def test_close(self):
        self.data.close_all()


def test_sequences():
    seq = sequences()
    seq.init()
    mysequences = [[1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1]]
    seq.save(mysequences, 2)
    print seq


#observation and dummy_lstrin g_class are used to mimic the lstring 
class position():
    def __init__(self):
        self.x=1
        self.y=1
        self.z=1
class observation():
    def __init__(self, observation='large'):
        self.observation = observation
        self.index = int(random.random()+0.5)
        self.number = int(random.random()+0.5)
        
        if int(random.random()+0.5)==1:
            self.inflorescence = True
        else:
            self.inflorescence=False
        self.year = 1990
        self.radius=1
        self.position=position()
        self.length=1
class dummy_lstring_class():
    def __init__(self, name='apex', obs='large'):
        self.name = name
        self.v = [observation(observation=obs)]

    def __getitem__(self, index):
        return self.v[index]

def test_lstring():
    l = l_string()
    l.init()
    lstring = [ dummy_lstring_class(name='apex'),
                dummy_lstring_class(name='branch'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='['),
                dummy_lstring_class(name=']'),
                dummy_lstring_class(name='metamer', obs='dormant'),
                dummy_lstring_class(name='metamer', obs='large'),
                dummy_lstring_class(name='metamer', obs='small'),
                dummy_lstring_class(name='metamer', obs='medium'),
                dummy_lstring_class(name='metamer', obs='floral'),
                dummy_lstring_class(name='metamer', obs='trunk'),
                dummy_lstring_class(name='metamer', obs='new_shoot'),
                dummy_lstring_class(name='metamer', obs='dummy')
            ]
    l.save(lstring, date='1995')
    print l
    os.remove(l.filename)


def test_mtg():
    import openalea.stocatree.output as output
    import datetime
    date = datetime.date(1995,10,10)
    mtg = output.mtg()
    mtg.init()

    lstring = [ dummy_lstring_class(name='apex'),
                dummy_lstring_class(name='branch'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='growth_unit'),
                dummy_lstring_class(name='['),
                dummy_lstring_class(name=']'),
                dummy_lstring_class(name='metamer', obs='dormant'),
                dummy_lstring_class(name='metamer', obs='dormant'),
                dummy_lstring_class(name='metamer', obs='dormant'),
                dummy_lstring_class(name='metamer', obs='dormant'),
                dummy_lstring_class(name='metamer', obs='large'),
                dummy_lstring_class(name='metamer', obs='small'),
                dummy_lstring_class(name='metamer', obs='medium'),
                dummy_lstring_class(name='metamer', obs='floral'),
                dummy_lstring_class(name='metamer', obs='trunk'),
                dummy_lstring_class(name='metamer', obs='new_shoot'),
            ]
    mtg.save(lstring, date, 3)

    mtg.close()
    print mtg
    os.remove(mtg.filename)

def test_leaves():
    l = leaves()

def test_trunk():
    t = trunk()
    t.init()
    t.save(1,1,1)
    t.close()
    os.remove(t.filename)

def test_counts():
    t = counts()
    try:
        t.save()
    except:
        assert True
    t.init()
    t.reset()
    t.save()
    t.save(date='1995')
    t.close()
    print t
    os.remove(t.filename)


def test_output():

    o = output(filename='test', tag='test', verbose=True)
    o.build_filename(date='1889') 
    o.init()
    o.init()
    o.advance(10.)
    o.advance(365.)
    try:
        o.save()
    except:
        assert True
    o.close()
