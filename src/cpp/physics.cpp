// Needed to make the definitions in lintrfc.h (LPFG include file) compile
#include <cassert>
#include <cmath>

#include "constrained_value.hpp"
#include "physics.hpp"
#include "quaternion.hpp"

const double error_tolerance = 0.00001;

frame::frame(v3d heading, v3d left, v3d up) :
  heading(heading),
  left(left),
  up(up)
{}

v3d calculate_rotation_velocity(v3d torque, double rigidity) {
  assert(rigidity > error_tolerance);
  return torque / rigidity;
}

frame reorient_frame(const frame& initial_hlu, const v3d& rotation_velocity,
                     const si::length<>& length)
{
  v3d h = initial_hlu.heading; h.normalise();
  v3d l = initial_hlu.left;    l.normalise();

  double vl = rotation_velocity.length();

  axis_angle aa(rotation_velocity / vl, vl * length.value);

  h = rotate(h, aa);
  l = rotate(l, aa);

  h.normalise();
  l.normalise();

  return frame(h, l, h % l);
}

si::secondmomentofarea<> second_moment_of_area_circle(si::length<> radius) {
  return constants::quarter_pi * std::pow(radius.value, 4);
}

si::secondmomentofarea<> second_moment_of_area_circular_section(si::length<> radius,
                                                                double section) {
  return (2.0 / 3.0) * std::pow(radius.value, 3) * std::sin(section * 0.5);
}

si::secondmomentofarea<> second_moment_of_area_annular_section(si::length<> inner_radius,
                                                               si::length<> thickness,
                                                               double section) {
  return (2.0 / 3.0) * inner_radius.value * inner_radius.value * thickness.value
    * std::sin(section * 0.5);
}

frame rotate_frame_at_branch(const frame& initial_hlu,
                             double branching_angle,
                             double phyllotactic_angle)
{
  frame hlu = initial_hlu;

  hlu.heading = rotate(initial_hlu.heading,
                       axis_angle(initial_hlu.left, branching_angle));
  hlu.up      = rotate(initial_hlu.up,
                       axis_angle(initial_hlu.left, branching_angle));

  hlu.heading.normalise();
  hlu.up.normalise();

  hlu.heading = rotate(hlu.heading,
                       axis_angle(initial_hlu.heading, phyllotactic_angle));
  hlu.up      = rotate(hlu.up,
                       axis_angle(initial_hlu.heading, phyllotactic_angle));

  hlu.heading.normalise();
  hlu.up.normalise();

  hlu.left = hlu.up % hlu.heading;

  return hlu;
}

si::pressure<> stress(const v3d& torque, si::length<> radius) {
  si::torque<>             moment_of_bending     = torque.length();
  si::secondmomentofarea<> second_moment_of_area = constants::quarter_pi
    * std::pow(radius.value, 4);
  return  moment_of_bending * radius / second_moment_of_area;
}

bool rupture(const v3d& torque, si::length<> radius) {
  si::pressure<> modulus_of_rupture = 50E6;

  return stress(torque, radius) > modulus_of_rupture;
}
