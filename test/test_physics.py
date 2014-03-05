from vplants.plantgl.all import Vector3, Vector4
from openalea.stocatree.physics import *
from openalea.stocatree.frame import Frame

def test_stress():
    torque = Vector3(100,100,500)
    radius = 0.1
    stress(torque, radius)

def test_rupture():
    torque = Vector3(0,0,50e5)
    radius = 1
    assert rupture(torque, radius)==False
    torque = Vector3(0,0,50e6)
    radius = 1
    assert rupture(torque, radius)==True



def test_second_moment_of_area_circle():
    print second_moment_of_area_circle(1)


def test_second_moment_of_area_circular_section():
    from openalea.stocatree.physics import _second_moment_of_area_circular_section
    _second_moment_of_area_circular_section(1, 1)


def test_second_moment_of_area_annular_section():
    print second_moment_of_area_annular_section(1, 1, 1)

def test_Frame():
    v1 = Vector3(2,1,1)
    v2 = Vector3(1,2,1)
    v3 = Vector3(1,1,2)
    f = Frame(v1, v2, v3)
    print f

def test_rotate_frame_at_branch():
    v1 = Vector3(2,1,1)
    v2 = Vector3(1,2,1)
    v3 = Vector3(1,1,2)
    frame = Frame(v1, v2, v3)
    rotate_frame_at_branch(frame, 45, 45)
    
def test_reorient_frame():
    v1 = Vector3(2,1,1)
    v2= Vector3(1,2,1)
    v3 = Vector3(1,1,2)
    rotation_velocity = Vector3(1,1,1)
    length = 1
    frame = Frame(v1, v2, v3)
    reorient_frame(frame, rotation_velocity, length)


if __name__ == "__main__":
    test_calculate_rotation_velocity()
    test_stress()
    test_rupture()
    test_second_moment_of_area_circle()    
    test_second_moment_of_area_circular_section()
    test_second_moment_of_area_annular_section()



def test_axis_angle():
    from openalea.stocatree.physics import _AxisAngle
    angle = 0.5
    v3 = Vector3(0,0.5,0.5)
    aa = _AxisAngle(v3, angle, check=True)
    aa.axis_angle_to_quaternion()

    w3 = Vector3(0.2,0.2,0.2)
    aa.rotate(w3)
    r1=aa._rotate1(w3)
    r2=aa._rotate2(w3)
    r3=aa._rotate3(w3)
    r4=aa._rotate4(w3)
    aa.angle = 0.
    r5=aa.rotate(w3)
    #assert r5==aa.v3
