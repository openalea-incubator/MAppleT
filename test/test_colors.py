from openalea.stocatree.colors import *


def test_colors():

    colors = Colors()
    assert colors.red == 2
    colors.observation.get_color('dormant')==2

def test_year():
    y = year()
    y.set_colors()
    y.get_color(1994, starting_year=1994)


def test_zone():
    y = zone()
    y.set_colors()
    y.get_color('small')
    try:
        y.get_color('dummy')
        assert False

    except:
        assert True


def test_reaction_wood():
    y = reaction_wood()
    y.set_colors()
    y.get_color(1.)


def test_observation():
    y = observation()
    y.set_colors()
    y.get_color('large')
    try:
        y.get_color('dummy')
        assert False
    except:
        assert True


def test_colorInterface():
    c = colorInterface()
    try:
        c.set_colors()
        assert False
    except:
        assert True
    try:
        c.get_color()
        assert False
    except:
        assert True
