#ifndef __ARRAY_HPP__
#define __ARRAY_HPP__

#include <stdexcept>
#include <iostream>

// An array class with bounds checking.
template <class T, unsigned int size>
class array {
public:
  array();
  array(const T& val);
  virtual ~array();

  T& at(unsigned int i);
  T& operator[](unsigned int i);
  T* c_data();

  array<T, size>& operator=(const array<T, size>& a);

private:
  T data[size];
};

template <class T, unsigned int size>
array<T, size>::array() {}

template <class T, unsigned int size>
array<T, size>::array(const T& val) {
  for (unsigned int i = 0; i < size; i++) data[i] = val;
}

template <class T, unsigned int size>
array<T, size>::~array() {}

template <class T, unsigned int size>
T& array<T, size>::at(unsigned int i) {
  if (i < size) return data[i];
  else throw std::out_of_range("Array index is out of range.");
}

template <class T, unsigned int size>
T& array<T, size>::operator[](unsigned int i) {
  return data[i];
}

template <class T, unsigned int size>
T* array<T, size>::c_data() {
  return data;
}

template <class T, unsigned int size>
array<T, size>& array<T, size>::operator=(const array<T, size>& a) {
  for (unsigned int i = 0; i < size; ++i) data[i] = a.data[i];
  return *this;
}

#endif
