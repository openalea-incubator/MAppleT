from openalea.stocatree.fruit import Fruit, AppleFruit



def test_fruit_state():
    # test set_state/get_state
    f = Fruit()
    f.state = 'flower'
    assert f._state=='flower'
    try:
        f.state = 'dummy'
        assert False
    except: 
        assert True

    assert f.state=='flower'

def test_fruit_compute_mass():
    f = Fruit()
    try:
       f.compute_mass()
       assert False
    except:
        assert NotImplementedError


def test_apple_fruit_state():
    # test set_state/get_state
    f = AppleFruit()
    f.state = 'flower'
    assert f._state=='flower'
    try:
        f.state = 'dummy'
        assert False
    except: 
        assert True

    assert f.state=='flower'

def test_apple_fruit_attributes():
    f = AppleFruit()
    assert f._flower_duration ==10
    assert f._probability == 0.3
    assert f._lost_time ==28
    assert f._max_relative_growth_rate == 0.167

def test_apple_fruit_compute_mass():
    f = AppleFruit()
    f.age = 50
    mass = f.compute_mass()

