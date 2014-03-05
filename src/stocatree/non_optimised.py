#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

"""

from vplants.plantgl.all import Vector3, cross
from frame import Frame
from math import cos, sin, pow, fabs, acos


def rotate(v3x,  v3y,  v3z,  angle,  vx,  vy,  vz):
    c =  cos(angle)
    t2 =  1 - c
    t6 =  t2*v3x
    t7 =  t6*v3y
    s =  sin(angle)
    t9 =  s*v3z
    t11 = t6*v3z
    t12 = s*v3y
    t19 = t2*v3y*v3z
    t20 = s*v3x
    t24 = v3z*v3z
    R00 = c + t2*v3x*v3x
    R01 = t7 - t9
    R02 = t11 + t12
    R10 = t7 + t9
    R11 = c + t2*v3y*v3y
    R12 = t19 - t20
    R20 = t11 - t12
    R21 = t19 + t20
    R22 = c + t2*t24
    return Vector3(R00*vx+R01*vy+R02*vz, R10*vx+R11*vy+R12*vz, R20*vx+R21*vy+R22*vz)



def second_moment_of_area_annular_section(inner_radius, thickness, section):
    rt = inner_radius+thickness
    rt2 = rt*rt
    rt4 = rt2*rt2
    r = inner_radius
    r2 = r*r
    r4=r2*r2
    return  0.125 * (rt4 - r4)*(section + sin(section))

def second_moment_of_area_circle(radius):
    return 0.78539816339744828 * radius * radius * radius * radius


def get_new_radius(ra,rb, exponent=2.49, previous_rt=-1):
    rap = pow(ra, exponent)
    rbp = pow(rb, exponent)
    newrt =  pow(rap+rbp, 1./exponent)
    return newrt

def reorient_frame(initial_hlu, rotation_velocity, rv_norm, length):
    h = Vector3(initial_hlu.heading)
    h.normalize()
    l = Vector3(initial_hlu.left)
    l.normalize()

    #vl = rotation_velocity.normalize() #_ look at v3d length definition
    #vl is replaced by rv_norm

    if fabs(rv_norm*length) >= 0.01:
        h = rotate(rotation_velocity.x, rotation_velocity.y, rotation_velocity.z, rv_norm*length, h.x, h.y, h.z)
        l = rotate(rotation_velocity.x, rotation_velocity.y, rotation_velocity.z, rv_norm*length, l.x, l.y, l.z)
    h.normalize()
    l.normalize()
    return Frame(h, l, cross(h, l))

def max(a, b):
    if a>b:
        return a
    else:
        return b


def reaction_wood_target(up, heading, previous_heading):
    cos_gh  = Vector3(0.0, 0.0, 1.0) * heading
    cos_pu = previous_heading * up
    cos_ph = previous_heading * heading

    inclination = 0
    if cos_pu*cos_ph >= 0.0:
        try:
            inclination = acos(cos_ph)
        except:
            #pass
            print str(cos_ph)
    else:
        try:
            inclination = -acos(cos_ph)
        except:
            print str(cos_ph)
    percentage  = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination;
    r = 3.14159*2. * percentage;

    if (r < 0.0):
        r = 0.0
    elif (r > 3.14159):
        r = 3.141459

    return r

