#ifndef __V3_HPP__
#define __V3_HPP__

#include <istream>
#include <ostream>
#include <cmath>
// A point/vector class for three dimensions.  It is set up to have
// similar interface to the V3 template class from LPFG.  Thus, it
// can be used as a replacement for situations where V3d from LPFG
// cannot be used.

template <class T> class v3 {
public:
  v3(const T& x = T(), const T& y = T(), const T& z = T()) :
    x(x), y(y), z(z)
  {}
  virtual ~v3() {}

  v3<T> operator= (const v3<T>& p);
  v3<T> operator+ (const v3<T>& p) const;
  v3<T> operator- (const v3<T>& p) const;
  v3<T> operator+=(const v3<T>& p);
  v3<T> operator-=(const v3<T>& p);
  v3<T> operator*=(const T& s);
  v3<T> operator/=(const T& s);

  T operator*(const v3<T>& p) const;
  v3<T> operator%(const v3<T>& p) const;

  v3<T> proj(const v3<T>& p) const;
  T        proj_length(const v3<T>& p) const;

  void normalise();
  void normalise(T l);
  T distance(const v3<T>& p) const;
  T distance_sq(const v3<T>& p) const;

  T length() const;
  T length_sq() const;

  void zero();

  T x;
  T y;
  T z;
};

template <class T>
v3<T> v3<T>::operator= (const v3<T>& p) {
  x = p.x;
  y = p.y;
  z = p.z;

  return *this;
}

template <class T>
v3<T> v3<T>::operator+ (const v3<T>& p) const {
  return v3<T>(this->x + p.x, this->y + p.y, this->z + p.z);
}
 
template <class T>
v3<T> v3<T>::operator- (const v3<T>& p) const {
  return v3<T>(this->x - p.x, this->y - p.y, this->z - p.z);
}

template <class T>
v3<T> operator- (const v3<T>& p) {
  return (v3<T>() - p);
}

template <class T>
v3<T> operator* (const v3<T>& p, const T& s) {
  return v3<T>(p.x * s, p.y * s, p.z * s);
}

template <class T>
v3<T> operator* (const T& s, const v3<T>& p) {
  return v3<T>(p.x * s, p.y * s, p.z * s);
}

template <class T>
v3<T> operator/ (const v3<T>& p, const T& s) {
  return v3<T>(p.x / s, p.y / s, p.z / s);
}

template <class T>
v3<T> operator/ (const T& s, const v3<T>& p) {
  return v3<T>(p.x / s, p.y / s, p.z / s);
}

template <class T>
v3<T> v3<T>::operator+=(const v3<T>& p) {
  *this = *this + p;
  return *this;
}

template <class T>
v3<T> v3<T>::operator-=(const v3<T>& p) {
  *this = *this - p;
  return *this;
}

template <class T>
v3<T> v3<T>::operator*=(const T& s) {
  *this = *this * s;
  return *this;
}

template <class T>
v3<T> v3<T>::operator/=(const T& s) {
  *this = *this / s;
  return *this;
}

template <class T>
T v3<T>::operator*(const v3<T>& p) const {
  T ret
    = x * p.x
    + y * p.y
    + z * p.z;
  return ret;
}

template <class T>
v3<T> v3<T>::operator%(const v3<T>& p) const {
  return v3<T>(y * p.z - z * p.y, z * p.x - x * p.z, x * p.y - y * p.x);
}

template <class T>
v3<T> v3<T>::proj(const v3<T>& p) const {
  return ((*this * p) / p.length_sq()) * p;
}

template <class T>
T v3<T>::proj_length(const v3<T>& p) const {
  return fabs(*this * p) / p.length();
}

template <class T>
void v3<T>::normalise() {
  T length = sqrt((x * x) + (y * y) + (z * z));

  x /= length;
  y /= length;
  z /= length;
}

template <class T>
void v3<T>::normalise(T l) {
  T length = sqrt((x * x) + (y * y) + (z * z));

  x /= length; x *= l;
  y /= length; y *= l;
  z /= length; z *= l;
}


template <class T>
T v3<T>::distance(const v3<T>& p) const {
  return sqrt((x - p.x) * (x - p.x) +
              (y - p.y) * (y - p.y) +
              (z - p.z) * (z - p.z));
}

template <class T>
T v3<T>::distance_sq(const v3<T>& p) const {
  return ((x - p.x) * (x - p.x) +
          (y - p.y) * (y - p.y) +
          (z - p.z) * (z - p.z));
}

template <class T>
T v3<T>::length() const {
  return sqrt((x * x) + (y * y) + (z * z));
}

template <class T>
T v3<T>::length_sq() const {
  return (x * x) + (y * y) + (z * z);
}

template <class T>
void v3<T>::zero() {
  x = T();
  y = T();
  z = T();
}

template <class T>
std::istream& operator>>(std::istream& is, v3<T>& p) {
  T x = T(), y = T(), z = T();
  is >> std::ws >> x >> std::ws >> y >> std::ws >> z;
  p.x = x;
  p.y = y;
  p.z = z;
  return is;
}

template <class T>
std::ostream& operator<<(std::ostream& os, const v3<T>& p) {
  os << p.x << " " << p.y << " " << p.z;
  return os;
}

template <class T>
bool operator==(const v3<T>& a, const v3<T>& b) {
  if (a.x != b.x) return false;
  if (a.y != b.y) return false;
  if (a.z != b.z) return false;
  return true;
}

template <class T>
bool operator!=(const v3<T>& a, const v3<T>& b) {
  if ((a.x == b.x) && (a.y == b.y) && (a.z == b.z)) return false;
  else return true;
}

typedef v3<double> v3d;
typedef v3<float>  v3f;

#endif
