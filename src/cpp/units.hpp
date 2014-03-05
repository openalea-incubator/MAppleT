#ifndef ___UNITS_HPP___
#define ___UNITS_HPP___

#include "dimnum.hh"
#include "si.hh"

namespace dimension {
  //              ln  ms  tm 
  typedef powers< 0,  0,  0,  0,  0,  0,  0> scalar;
  typedef powers<-3,  1,  0,  0,  0,  0,  0> density;
  typedef powers< 1,  1, -2,  0,  0,  0,  0> force;
  typedef powers< 2,  1, -2,  0,  0,  0,  0> torque;
  typedef powers<-1,  1, -2,  0,  0,  0,  0> pressure;
  typedef powers<-1,  1, -3,  0,  0,  0,  0> pressurepertime;
  typedef powers< 4,  0,  0,  0,  0,  0,  0> secondmomentofarea;
  typedef powers< 3,  1, -2,  0,  0,  0,  0> rigidity;
  typedef powers<-2,  1,  0,  0,  0,  0,  0> massperarea;
  typedef powers< 0,  1, -1,  0,  0,  0,  0> masspertime;
  typedef powers<-2,  0,  0,  0,  0,  0,  0> perarea;
  typedef powers< 1,  1,  0,  0,  0,  0,  0> lengthpermass; // might be wrong
}

stddeclare(dimensionless)

default(si, scalar,             none,                  1, 1, 0, "")
default(si, density,            kilogrampermetrecubed, 1, 1, 0, "kg/m^3")
default(si, force,              newton,                1, 1, 0, "N")
default(si, torque,             newtonmetre,           1, 1, 0, "Nm")
default(si, pressure,           pascal,                1, 1, 0, "Pa")
default(si, pressurepertime,    pascalpersecond,       1, 1, 0, "Pa/s")
default(si, secondmomentofarea, metre4,                1, 1, 0, "m^4")
default(si, rigidity,           pascalmetre4,          1, 1, 0, "Pa m^4")
default(si, massperarea,        kilogramspermetre2,    1, 1, 0, "kg/m^2")
default(si, masspertime,        kilogramspersecond,    1, 1, 0, "kg/s")
default(si, perarea,            permetre2,             1, 1, 0, "/m^2")
default(si, lengthpermass,      metreperkilogram,      1, 1, 0, "m/kg")

declare(si, length,        cm,                    1,        1,   -2, "cm")
declare(si, length,        mm,                    1,        1,   -3, "mm")
declare(si, time,          year,           31556926,        1,    0, "y")
declare(si, inverse_time,  perday,                1,    86400,    0, "d^-1")
declare(si, inverse_time,  peryear,               1, 31556926,    0, "y^-1")
declare(si, massperarea,   gramspermetre2,        1,     1000,    0, "g/m^2")
declare(si, area,          cm2,                   1,    10000,    0, "cm^2")
declare(si, masspertime,   gramsperday,           1, 86400000,    0, "g/d")
declare(si, perarea,       percm2,                1,    10000,    0, "/cm^2")
declare(si, lengthpermass, mmperg,                1,        1,    0, "mm/g")
declare(si, velocity,      mmperday,              1, 86400000,    0, "mm/day")
declare(si, pressure,      gigapascal,            1,        1,    9, "GPa")

#endif
