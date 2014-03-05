#ifndef __PHYSICS_HPP__
#define __PHYSICS_HPP__

#include "units.hpp"
#include "v3.hpp"

struct frame {
  frame(v3d heading = v3d(), v3d left = v3d(), v3d up = v3d());

  v3d heading;
  v3d left;
  v3d up;
};

v3d                      calculate_rotation_velocity(v3d torque, double rigidity);
frame                    reorient_frame(const frame& initial_hlu, const v3d& rotation_velocity,
                                        const si::length<>& length);
si::secondmomentofarea<> second_moment_of_area_circle(si::length<> radius);
si::secondmomentofarea<> second_moment_of_area_circular_section(si::length<> radius,
                                                                double section);
si::secondmomentofarea<> second_moment_of_area_annular_section(si::length<> inner_radius,
                                                               si::length<> thickness,
                                                               double section);
frame                    rotate_frame_at_branch(const frame& initial_hlu, double branching_angle,
                                                double phyllotactic_angle);
bool                     rupture(const v3d& torque, si::length<> radius);

#endif
