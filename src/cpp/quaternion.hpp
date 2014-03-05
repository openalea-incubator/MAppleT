#ifndef __QUATERNION_HPP__
#define __QUATERNION_HPP__

#include <ostream>

#include "constrained_value.hpp"
#include "v3.hpp"

// The implementation of this class is based on "Rotation
// Representations and Performance Issues" by David Eberly, found at
// http://www.geometrictools.com/Documentation/RotationIssues.pdf

class quaternion {
public:
  quaternion(double w, double x, double y, double t);

  double w;
  double x;
  double y;
  double z;

  void set(double w, double x, double y, double z);
  void zero();
};

struct axis_angle {
  axis_angle(v3d axis = v3d(), double angle = 0.0) :
    axis(axis),
    angle(angle)
  {}

  v3d    axis;
  double angle;
};

quaternion operator-(const quaternion& q);
quaternion operator*(const quaternion& a, const quaternion& b);
quaternion operator*(const quaternion& a, const v3d& b);

std::ostream& operator<<(std::ostream& os, const quaternion& q);

quaternion vector_to_quaternion(const v3d& v);
v3d        quaternion_to_vector(const quaternion& q);
quaternion axis_angle_to_quaternion(const axis_angle& a);
axis_angle quaternion_to_axis_angle(const quaternion& q);

v3d rotate(const v3d& v, const axis_angle& a);
v3d rotate(const v3d& v, const quaternion& q);

#endif
