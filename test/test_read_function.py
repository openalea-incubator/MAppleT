from openalea.stocatree.tools.read_function import ReadFunction,  _FSet


def test_read_function():
    func_leaf_area = ReadFunction('functions.fset', 'leaf_area')
    func_leaf_area.gety(0.5)
    try:
        func_leaf_area = ReadFunction('dummy.fset', 'leaf_area')
        assert False
    except:
        assert True

def test_fset():

    x = [0,1,2,3]
    y = [0,0.25,0.5,1]
    fset = _FSet(flip='on', x=x, y=y)
    print fset
    fset = _FSet(flip='off', x=x, y=y)
    print fset
    

    try:
        fset = _FSet(flip='dummy', x=x, y=y)
        assert False
    except:
        True



