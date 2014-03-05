from openalea.stocatree.tree import *

tolerance = 1e-16


def test_tree():
    from openalea.stocatree.tree import Tree
    tree= Tree()
    tree.phyllotactic_angle=3.14/2.
    tree.convert_to_degrees()
    tree.convert_to_radians()
    assert  tree.phyllotactic_angle>3.139/2. and tree.phyllotactic_angle<3.15/2.
    print tree

    tree.convert_to_degrees()
    tree.convert_to_radians()
