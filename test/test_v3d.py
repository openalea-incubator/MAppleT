from vplants.plantgl.all import Vector3, Vector4, cross, norm, normSquared

# could use also ext.geom ? 
tol = 1e-12


def test_vector3():
    tropism = Vector3(0,0.1,0)
    tropism.y += .1;
    assert tropism.y == 0.2
    assert tropism.x == 0.
    assert tropism.z == 0


def test_vector3_cross():
    """equivalent of % operator in v3 mapplet"""
    v1 = Vector3(1.0, 0, 0)
    v4 = Vector3(4.0, 5, -1)
    assert cross(v4,v1) == Vector3(0, -1, -5)


def test_operator():
    v1 = Vector3(1.0, 0, 0)
    v2 = Vector3(0, 1, 0)
    assert v1+v2 == Vector3(1,1,0)
    assert v1-v2 == Vector3(1,-1,0)
    assert v1*2 == Vector3(2,0,0)


def test_norm():
    """norm is equivalent to length in v3 mapplet"""
    from math import sqrt
    v=Vector3(0,4,4);
    v.normalize();
    assert v == Vector3(0, sqrt(2)/2, sqrt(2)/2)
    #v = v.__norm__()
    v = norm(v)
    assert v>1-tol and v<1+tol


def test_normSquared():
    """normSquared is equivalent to length_sq in v3 mapplet"""
    from math import sqrt
    v=Vector3(1,2,3);
    assert 14==normSquared(v)
    #assert 14==v.__normSquared__()



