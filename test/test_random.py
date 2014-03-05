import openalea.stocatree.srandom as srandom

N = 100
def test_uniform_random():
    for i in range(1,N):
        a = srandom.random(-1, 1)
        assert a >=-1
        assert a <=1

    try:
        srandom.random(-1,1,1,1,1,1)
        assert False
    except:
        assert True
    
    try:
        srandom.random('rubbish')
        assert False
    except:
        assert True

def test_uniform_random_scaled():
    for i in range(1,N):
        a = srandom.random(5.)
        assert a >=0
        assert a <=5

def test_uniform_random_int():
    for i in range(1,N):
        a = srandom.random(5)
        print a
        assert a >=0
        assert a <=5


def test_boolean_event():
    for i in range(1,10):
        print i*0.1, " ", srandom.boolean_event(0.5)


test_boolean_event()
