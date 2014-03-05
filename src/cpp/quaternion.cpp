#include <cassert>
#include <cmath>
#include <fstream>
#include "quaternion.hpp"
#include "range.hpp"

quaternion::quaternion(double w, double x, double y, double z) :
  w(w),
  x(x),
  y(y),
  z(z)
{}

void quaternion::set(double w, double x, double y, double z) {
  this->w = w;
  this->x = x;
  this->y = y;
  this->z = z;
}

void quaternion::zero() {
  x = 0.0;
  y = 0.0;
  z = 0.0;
  w = 0.0;
}

quaternion operator-(const quaternion& q) {
  return quaternion(q.w, -q.x, -q.y, -q.z);
}

quaternion operator*(const quaternion& a, const quaternion& b) {
  return quaternion(
    a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
    a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
    a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
    a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
  );
}

quaternion operator*(const quaternion& a, const v3d& b) {
  return quaternion(
    -a.x * b.x - a.y * b.y - a.z * b.z,
     a.w * b.x + a.y * b.z - a.z * b.y,
     a.w * b.y - a.x * b.z + a.z * b.x,
     a.w * b.z + a.x * b.y - a.y * b.x
  );
}

std::ostream& operator<<(std::ostream& os, const quaternion& q) {
  os << q.w << " + "
     << q.x << "i + "
     << q.y << "j + "
     << q.z << "k";
  return os;
}

quaternion vector_to_quaternion(const v3d& v) {
  return quaternion(0.0, v.x, v.y, v.z);
}

v3d quaternion_to_vector(const quaternion& q) {
  assert(std::fabs(q.w) < 0.01);
  return v3d(q.x, q.y, q.z);
}

quaternion axis_angle_to_quaternion(const axis_angle& a) {
  const double half_angle     = a.angle * 0.5;
  const double sin_half_angle = std::sin(half_angle);
  return quaternion(std::cos(half_angle), a.axis.x * sin_half_angle, a.axis.y * sin_half_angle, a.axis.z * sin_half_angle);
}

axis_angle quaternion_to_axis_angle(const quaternion& q) {
  assert(fabs(q.w) <= 1.0);

  axis_angle a;

  a.axis = v3d(q.x, q.y, q.z);
  a.axis /= std::sqrt(1.0 - q.w * q.w);

  a.angle = 2.0 * std::acos(q.w);

  return a;
}

v3d rotate(const v3d& v, const quaternion& q) {
  return quaternion_to_vector(q * v * -q);
}

v3d rotate(const v3d& v, const axis_angle& a) {
  if (std::fabs(a.angle) < 0.00001) return v;

  const quaternion q  = axis_angle_to_quaternion(a);
  const double     w = q.x * v.x + q.y * v.y + q.z * v.z;
  const double     x = q.w * v.x + q.y * v.z - q.z * v.y;
  const double     y = q.w * v.y - q.x * v.z + q.z * v.x;
  const double     z = q.w * v.z + q.x * v.y - q.y * v.x;

  return v3d(
    w * q.x + x * q.w - y * q.z + z * q.y,
    w * q.y + x * q.z + y * q.w - z * q.x,
    w * q.z - x * q.y - y * q.x + z * q.w
  );
}
