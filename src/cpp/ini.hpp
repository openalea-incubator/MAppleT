#ifndef __INI_HPP__
#define __INI_HPP__

#include <map>
#include <sstream>

namespace ini {
  typedef std::map<std::string, std::string> values;

  bool exists(std::string key, const values& v);
  void read(std::string filename, values& v);

  template <class T> T get(values& v, std::string key) {
    std::istringstream s(v[key]);
    T val;
    s >> val;
    return val;
  }

  template <class T> void get(values& v, std::string key, T& var) {
    if (exists(key, v)) var = get<T>(v, key);
  }
}

#endif
