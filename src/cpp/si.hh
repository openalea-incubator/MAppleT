#ifndef si_hh__
#define si_hh__

default(si, length,              meter,                  1,  1,	0, "m")
default(si, mass,                kilogram,               1,  1,	0, "kg")
default(si, time,                second,                 1,  1,	0, "s")
default(si, current,             ampere,                 1,  1,	0, "A")
default(si, temperature,         kelvin,                 1,  1,	0, "K")
default(si, amount_of_substance, mol,                    1,  1,	0, "mol")
default(si, luminous_intensity,  candela,                1,  1,	0, "cd")
default(si, area,                metersquared,           1,  1,	0, "m^2")
default(si, velocity,            meterpersecond,         1,  1,	0, "m/s")
default(si, acceleration,        meterpersecond2,        1,  1,	0, "m/s^2")

default(si, energy,              joule,                  1,  1,   0, "J")
default(si, entropy,             joulekelvininv,         1,  1,   0, "J/K")

default(si, inverse_time,        hertz,                  1,  1,   0, "Hz")

// derived units
declare(si, length,              millimeter,             1,  1,  -3, "mm")
declare(si, length,              centimeter,             1,  1,  -2, "cm")
declare(si, length,              decimeter,              1,  1,  -1, "dm")

declare(si, time,                minute,                60,  1,   0, "min")
declare(si, time,                hour,                3600,  1,   0, "hr")
declare(si, time,                day,                86400,  1,   0, "d")
declare(si, time,                millisecond,            1, 1000, 0, "msec")

#endif
