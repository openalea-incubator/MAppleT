#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: optimisation.pyx summary

    A Cython module that duplicates pure python functions so as to optimise
    running time of the stocatree Lsystem.

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $

In principle, the c-file corresponding to this cython module and its compiled
code are automatically create when running::

    python setup.py install

However, if for some reason, you need to compile it yourself, here is the procedure.
First, you need to get the c code::

    cython optimisation.pyx;

Then, under linux, compile the code as follows::

    gcc -O2   -I/usr/include/python2.5 -c optimisation.c -o optimisation.o
    gcc -O2 -shared optimisation.o -L/usr/lib -lpython2.5 -o optimisation.so

or under windows::


    mingw32-g++.exe  -O2   -D:\Python26\include -c optimisation.c -o optimisation.o
    ming232-g++.exe -O2 -shared optimisation.o -LD:\Python26\libs -lpython26 -o optimisation.so

The following functions have been rewritten:

   * get_new_radius as in :meth:`~openalea.stocatree.pipe.get_new_radius`
   * second_moment_of_area_circle` as in :meth:`~openalea.stocatree.physics.second_moment_of_area_circle`.
   * second_moment_of_area_annular_section as in :meth:`~openalea.stocatree.physics.second_moment_of_area_annular_section`
   * reorient_frame as in :meth:`~openalea.stocatree.physics.reorient_frame`. 
   * reaction_wood_target as in :meth:`~openalea.stocatree.metamer.reaction_wood_target`

In addition, the following functions are available from this module only :

   * rotate see explanation here below.
   * max : a simple max function that returns max between two double.

:rotate:

The **rotate** function returns a vector, which is the rotation of an initial vector :math:`v` around
another vector :math:`w` by an angle :math:`\\alpha`. This function is called as follows::

    newvector = rotate(vx,vy,vz, angle, wx,wy,wz)

and is equivalent to the following PlantGL implementation::

    from openalea.plantgl.scenegraph._pglsg import AxisRotation
    newvector = AxisRotation(Vector3(vx,vy,vz), angle).getMatrix3()*w

:max:
::

    >>> max(1,2)
    2
    
    
.. seealso:: :mod:`~openalea.stocatree.physics` for details documentation of 
    the following functions

"""

from vplants.plantgl.all import Vector3, cross
from frame import Frame

cdef extern from "math.h":
    float sinf(float theta)
    float cosf(float theta)
    float acosf(float theta)
    float powf(float x, float exp)
    float fabsf(float x)

def rotate(float v3x, float v3y, float v3z, float angle, float vx, float vy, float vz):
    cdef float c =  cosf(angle)
    cdef float t2 =  1 - c
    cdef float t6 =  t2*v3x
    cdef float t7 =  t6*v3y
    cdef float s =  sinf(angle)
    cdef float t9 =  s*v3z
    cdef float t11 = t6*v3z
    cdef float t12 = s*v3y
    cdef float t19 = t2*v3y*v3z
    cdef float t20 = s*v3x
    cdef float t24 = v3z*v3z
    cdef float R00 = c + t2*v3x*v3x
    cdef float R01 = t7 - t9
    cdef float R02 = t11 + t12
    cdef float R10 = t7 + t9
    cdef float R11 = c + t2*v3y*v3y
    cdef float R12 = t19 - t20
    cdef float R20 = t11 - t12
    cdef float R21 = t19 + t20
    cdef float R22 = c + t2*t24
    return Vector3(R00*vx+R01*vy+R02*vz, R10*vx+R11*vy+R12*vz, R20*vx+R21*vy+R22*vz)



cdef double _second_moment_of_area_annular_section(double inner_radius, double thickness, double section):
    cdef double rt = inner_radius+thickness
    cdef double rt2 = rt*rt
    cdef double rt4 = rt2*rt2
    cdef double r = inner_radius
    cdef double r2 = r*r
    cdef double r4=r2*r2
    return  0.125 * (rt4 - r4)*(section + sinf(section))

def second_moment_of_area_annular_section(double inner_radius, double thickness, double section):
    return _second_moment_of_area_annular_section(inner_radius, thickness, section)


cdef double _second_moment_of_area_circle(double radius):
    return 0.78539816339744828 * radius * radius * radius * radius

def second_moment_of_area_circle(double radius):
    return _second_moment_of_area_circle(radius)


cdef double _get_new_radius(double ra,double rb, double exponent, double previous_rt):
    cdef double rap = powf(ra, exponent)
    cdef double rbp = powf(rb, exponent)
    cdef double newrt =  powf(rap+rbp, 1./exponent)
    return newrt

def get_new_radius(double ra, double rb, double exponent=2.49, double previous_rt=-1):
    return _get_new_radius(ra,rb,exponent, previous_rt)

def reorient_frame(initial_hlu, rotation_velocity, double rv_norm, double length):
    h = Vector3(initial_hlu.heading)
    h.normalize()
    l = Vector3(initial_hlu.left)
    l.normalize()
    #cdef double vl = rv.normalize() #_ look at v3d length definition
    #vl is replaced by rv_norm

    if fabsf(rv_norm*length) >= 0.01:
        h = rotate(rotation_velocity.x, rotation_velocity.y, rotation_velocity.z, rv_norm*length, h.x, h.y, h.z)
        l = rotate(rotation_velocity.x, rotation_velocity.y, rotation_velocity.z, rv_norm*length, l.x, l.y, l.z)
    h.normalize()
    l.normalize()
    return Frame(h, l, cross(h, l))

cdef double _max(double a, double b):
    if a>b:
        return a
    else:
        return b


def max(double a, double b):
    return _max(a,b)



cdef double _reaction_wood_target(up, heading, previous_heading):
    cdef double cos_gh  = Vector3(0.0, 0.0, 1.0) * heading
    cdef double cos_pu = previous_heading * up
    cdef double cos_ph = previous_heading * heading
    cdef double inclination, percentage, r

    if cos_pu*cos_ph >= 0.0:
        inclination = acosf(cos_ph)
    else:
        inclination = -acosf(cos_ph)
    percentage  = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination;
    r = 3.14159*2. * percentage;

    if (r < 0.0):
        r = 0.0
    elif (r > 3.14159):
        r = 3.141459

    return r

def reaction_wood_target(up, heading, previous_heading):
    return _reaction_wood_target(up, heading, previous_heading)
