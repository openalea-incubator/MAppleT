#ifndef __RANGE_HPP__
#define __RANGE_HPP__

// Adapted from "Syntactical Aspertame: Recreational Overloading",
// CUJ, Feb 2006.


// Check if a value is in an closed range.
template <typename T>
bool range_closed(const T& minimum, const T& maximum, const T& value) {
  return (value >= minimum and value <= maximum);
}

// Check if a value is in an open range.
template <typename T>
bool range_open(const T& minimum, const T& maximum, const T& value) {
  return (value > minimum and value < maximum);
}

// Check if a value is in a C-style range (closed on the bottom, open on the top)
template <typename T>
bool range_c(const T& minimum, const T& maximum, const T& value) {
  return (value >= minimum and value < maximum);
}

// Check if a value is in a Fortran-style range (open on the botton, closed on the top)
template <typename T>
bool range_f(const T& minimum, const T& maximum, const T& value) {
  return (value > minimum and value <= maximum);
}

#endif
