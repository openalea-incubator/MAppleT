#include <cctype>
#include <cstring>

#include <fstream>

#include "ini.hpp"

bool ini::exists(std::string key, const ini::values& v) {
  return v.find(key) != v.end();
}

void ini::read(std::string filename, ini::values& v) {
  std::ifstream file(filename.c_str());

  if (!file) throw 0;

  file >> std::ws;

  while (not file.eof()) {
    file >> std::ws;

    // Test for a comment
    if (file.peek() == ';' or file.peek() == '#') {
      file.ignore(1024, '\n');
      continue;
    }

    std::string key;
    do {
      char c;
      file.get(c);

      if (std::isspace(c)) {
	file >> std::ws;
	continue;
      }

      if (c == '=') break;

      key += c;
    } while (not file.eof());

    file >> std::ws;

    std::string value;
    getline(file, value);

    file >> std::ws;

    v[key] = value;
  }
}
