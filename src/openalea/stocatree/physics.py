"""
.. topic:: summary

    The physics module implements functions to calculate the moment of inertia 
    and to reorient the frame with respect to torque effects.


    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :References:
        1. Colin Smith, Costes Evelyne, On the Simulation of Apple Trees Using 
           Statistical and Biomechanical Principles, INRIA technical report, 2007

    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.physics import *

.. testsetup::

    from openalea.stocatree.physics import *

.. note:: many functions have been reimplemented in optimisation.pyx

"""


from vplants.plantgl.all import Vector3, cross, Matrix3
import constants
import numpy
from math import cos, sin
try:
    import optimisation
except:
    print 'WARNING using non optimised code'
    import non_optimised as optimisation

from frame import Frame


error_tolerance = 0.0001

__all__ = [
    'second_moment_of_area_circle',
    'second_moment_of_area_annular_section',
    'rupture',
    'stress',
    'reorient_frame',
    'rotate_frame_at_branch']



def reorient_frame(initial_hlu, rotation_velocity, length):
    """Reorient frame

    The initial frame is an HLU (Heading Up Left, turtle axes) frame, made of tree orthogonal vectors that indicate the heading, 
    upwards and left directions of the beam.

    Then, the HLU frame is rotated around the rotation velocity vector.

    length is used to rotate the frame only when the product of rotation_velocity and length
    is large enough.

    :param initial_hlu: a `Frame` defining the initial HLU frame at the beginning of the season
    :param rotation_velocity:
    :param length: length of metamer

    :returns: a new rotated frame 

    .. todo:: describe the algorithm

    .. note:: this function has been optimised to used the rotate function from
        optimisation.pyx that computes the rotation of the AxisAngle around a
        given vector. It replaces the AxisAngle./quaternion of the origninal code of
        MappleT.

     ::

        import openalea.stocatree.optimisation as optimisation
        optimisation.rotate(hlu, Vector3, length)


    """
    h = Vector3(initial_hlu.heading)
    h.normalize()
    l = Vector3(initial_hlu.left)
    l.normalize()
    vl = rotation_velocity.normalize() #_ look at v3d length definition
    if abs(vl*length) >= 0.01:
        h = optimisation.rotate(rotation_velocity.x, rotation_velocity.y,
                   rotation_velocity.z, vl*length, h.x, h.y, h.z)
        l = optimisation.rotate(rotation_velocity.x, rotation_velocity.y, 
                   rotation_velocity.z, vl*length, l.x, l.y, l.z)
    h.normalize()
    l.normalize()
    return Frame(h, l, cross(h, l))


def second_moment_of_area_circle(radius):
    """Returns second moment of area of a circular cross section

    The internodes of the branches are assumed to be circular, with a radius
    :math:`r`, and so the moment of inertia for the cross-section bend around an
    axis on the same plane is :

    .. math::

        I_c = \dfrac{\pi}{4} r^4 = \dfrac{\pi}{64}D^4

    This is used for new shoots with no cambial layers.

    .. note:: This equation is useful in calculating the required strength of masts. 
        Taking the area moment of inertia calculated from the previous formula, 
        and entering it into Euler's formula gives the maximum force that a mast
        can theoretically withstand. 

        .. math::

            F = \dfrac{\pi ^2 E I}{l ^2} 

        where

            * E is [Young's modulus|Young (elastic) modulus of material]
            * :math:`\\textrm{I}` is the second moment of area of examined object
            * l is the length of panel

    :param radius: the radius in meters

    :Returns: :math:`I_c`

    :References: MappleT

    .. note::    this function is duplicated in a cython version inside optimisation.pyx

        >>> import openalea.stocatree.optimisation as optimisation
        >>> a = optimisation.second_moment_of_area_circle(1.)


    """
    #pi/4=0.7853981633974483
    return  0.7853981633974483 * radius * radius * radius * radius



def _second_moment_of_area_circular_section(radius, section):
    """Returns second moment of area (circular section)
    
    This is a particular case of annular section.

    This is used for code wood of a shoot under the cambial layers.

    :param radius: the radius in meters
    :param section: the section angle in radians

    .. math::

        \dfrac{2}{3}  r^3 \sin \dfrac{section}{2}
    """
    return (2.0 / 3.0) * radius *radius *radius * sin(section * 0.5)


def second_moment_of_area_annular_section(inner_radius, thickness, section):
    r"""Returns second moment of area (annular section)

    The annular cross section of an internode, with an inner **radius**
    :math:`r_i`, a **thickness** :math:`\theta` and a **section** :math:`\gamma`
    has a second moment of area defined by 

    .. math::

        I_s = \dfrac{1}{4}  \left( \left( r_i+ \theta \right)^4-r_i^4\right)\times(\gamma+\sin \gamma)


    This function is used within metamer classes to compute in association the reaction wood


    :param inner_radius: the inner radius in meters
    :param thickness: the thickness in meters
    :param section: the section angle in radians

    .. warning::    this function is duplicated in a cython version inside optimisation.pyx

        >>> import openalea.stocatree.optimisation as optimisation
        >>> a = optimisation.second_moment_of_area_annular_section(1., 0.1, 0.78)
    """
    assert section <= 2 * constants.pi
    return 0.125 * ((inner_radius+thickness)**4 - inner_radius**4) * \
            (section + sin(section))


def rotate_frame_at_branch(initial_hlu, branching_angle, phyllotactic_angle):
    """Rotate an initial frame around branching and phyllotactic angle

    Given an initial HLU frame, return a new frame after rotation around branching
    and phyllotactic angle.

    :param initial_hlu: the initial HLU frame
    :param branching_angle: the angle between main trunk and the branch.
    :param phyllotactic_angle: the angle related to phyllotaxy

    .. note:: this function has been optimised to used the rotate function from 
        optimisation.pyx that computes the rotation of the AxisAngle around a 
        given vector. It replaces the AxisAngle./quaternion of the origninal code of
        MappleT.
    .. note:: this function is not part of optimisation.pyx since it already use the 
        rotate function and is not called as much as the reorient_frame or rotate
        function itself.
    """

    hlu = Frame(initial_hlu.heading, initial_hlu.up, initial_hlu.left)

    hlu.heading = optimisation.rotate(
        initial_hlu.left.x, initial_hlu.left.y, initial_hlu.left.z, 
        branching_angle,
        initial_hlu.heading.x, initial_hlu.heading.y, initial_hlu.heading.z)
    hlu.up = optimisation.rotate(
        initial_hlu.left.x, initial_hlu.left.y, initial_hlu.left.z, 
        branching_angle,
        initial_hlu.up.x, initial_hlu.up.y, initial_hlu.up.z)
    hlu.heading.normalize()
    hlu.up.normalize()


    hlu.heading = optimisation.rotate(initial_hlu.heading.x, initial_hlu.heading.y, 
                         initial_hlu.heading.z, 
        phyllotactic_angle,
        hlu.heading.x, hlu.heading.y, hlu.heading.z)
    hlu.up = optimisation.rotate(
        initial_hlu.heading.x, initial_hlu.heading.y, initial_hlu.heading.z,
        phyllotactic_angle,
        hlu.up.x, hlu.up.y, hlu.up.z)

    hlu.heading.normalize()
    hlu.up.normalize()
    hlu.left = cross(hlu.up, hlu.heading)

    return hlu


def stress(torque, radius):
    """Stress. Not used for the moment
    """

    #si::torque<>             moment_of_bending     = torque.length();
    moment_of_bending     = torque.__norm__()

    #si::secondmomentofarea<> second_moment_of_area = constants::quarter_pi * 
    #std::pow(radius.value, 4);
    r4 = radius * radius * radius * radius
    second_moment_of_area = constants.quarter_pi * r4
    return  moment_of_bending * radius / second_moment_of_area


def rupture(torque, radius, modulus_of_rupture=50e6):
    """
    :param torque: v3d
    :param radius: si::length

    .. todo: not used for the moment
    """
    return stress(torque, radius) > modulus_of_rupture



class _AxisAngle(object):
    """
    .. deprecated:: 8981

    Kept in the svn archive because it implemented different version of the rotate function
    """
    def __init__(self, v3, angle, check=False):
        self.v3 = v3
        self.angle = angle
        if check:
            self.check()

    def check(self):
        assert isinstance(self.v3, Vector3)
        assert isinstance(self.angle, float) or isinstance(self.angle, int)

    def axis_angle_to_quaternion(self):
        r"""Transform an axis angle into a quaternion

        From wikipedia, Dec 2009, a quaternion representation of rotation 
        is written as a normalized  four dimensional vector 
        :math:`\hat{\mathbf{q}} = [q_1\ q_2\ q_3\ q_4]^T` 
        In terms of the Euler axis :math:`\hat{\mathbf{e}} = [e_x\ e_y\ e_z]^T` 
        and angle :math:`\theta` this vector's elements are expressed as follow:

        .. math::

            \begin{array}{lcl} 
                q_1 &=& e_x\sin(\theta/2)\\ 
                q_2 &=& e_y\sin(\theta/2)\\ 
                q_3 &=& e_z\sin(\theta/2)\\ 
                q_4 &=& \cos(\theta/2) 
            \end{array}

        The above definition follows the convention as used in (Wertz 1980) and (Markley 2003)

        """
        half_angle = self.angle * 0.5
        self.sin_half_angle = sin(half_angle)
        self.cos_half_angle = cos(half_angle)
        return numpy.array( [self.v3.x * self.sin_half_angle,
                             self.v3.y * self.sin_half_angle,
                             self.v3.z * self.sin_half_angle,
                             self.cos_half_angle])


    def rotate(self,v):
        if abs(self.angle) < 0.00001:
            return v
        res = self._rotate3(v)
        return res

    def _rotate1(self, v):
        """method of rotation that uses Quaternion method"""
        q = self.axis_angle_to_quaternion()

        """print '========'
        # orginal method 
        w = q[0] * v.x + q[1] * v.y + q[2] * v.z
        x = q[3] * v.x + q[1] * v.z - q[2] * v.y
        y = q[3] * v.y - q[0] * v.z + q[2] * v.x
        z = q[3] * v.z + q[0] * v.y - q[1] * v.x
        res = Vector3( w * q[0] + x * q[3] - y * q[2] + z * q[1],
                        w * q[1] + x * q[2] + y * q[3] - z * q[0],
                        w * q[2] - x * q[1] - y * q[0] + z * q[3]
                      )
        print res.x, res.y, res.z 
        """
        a = q[3]
        b=q[0]
        c=q[1]
        d=q[2]
        t2 =   a*b
        t3 =   a*c
        t4 =   a*d
        t5 =  -b*b
        t6 =   b*c
        t7 =   b*d
        t8 =  -c*c
        t9 =   c*d
        t10 = -d*d
        v1new = 2*( (t8 + t10)*v.x + (t6 -  t4)*v.y + (t3 + t7)*v.z ) + v.x
        v2new = 2*( (t4 +  t6)*v.x + (t5 + t10)*v.y + (t9 - t2)*v.z ) + v.y
        v3new = 2*( (t7 -  t3)*v.x + (t2 +  t9)*v.y + (t5 + t8)*v.z ) + v.z
        return Vector3(v1new, v2new, v3new)

    def _rotate2(self, v):
        """method of rotation that uses AxisAngle method only"""
        c =  cos(self.angle)
        t2 =  1 - c
        t3 =  self.v3.x*self.v3.x
        t6 =  t2*self.v3.x
        t7 =  t6*self.v3.y
        s =  sin(self.angle)
        t9 =  s*self.v3.z
        t11 = t6*self.v3.z
        t12 = s*self.v3.y
        t15 = self.v3.y* self.v3.y
        t19 = t2*self.v3.y*self.v3.z
        t20 = s*self.v3.x
        t24 = self.v3.z*self.v3.z
        R = Matrix3()
        R[0, 0] = c + t2*t3
        R[0, 1] = t7 - t9
        R[0, 2] = t11 + t12
        R[1, 0] = t7 + t9
        R[1, 1] = c + t2*t15
        R[1, 2] = t19 - t20
        R[2, 0] = t11 - t12
        R[2, 1] = t19 + t20
        R[2, 2] = c + t2*t24

        return R*v

    def _rotate3(self, v):
        """method of rotation based on PlantGL method.

        This method is about 4 times faster than rotate and 2 times faster than rotate2
        """
        from openalea.plantgl.scenegraph._pglsg import AxisRotation
        res = AxisRotation(self.v3, self.angle).getMatrix3()*v
        return res

    def _rotate4(self, v):
        
        return  optimisation.rotate(self.v3.x, self.v3.y, self.v3.z, 
                                    v.x, v.y, v.z, self.angle)




