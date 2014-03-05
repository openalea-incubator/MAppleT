/*********************************************************************
 * PMAppleT 2
 * -------------------------------------------------------------------
 *
 * This L-system is a simulation of the growth of an apple tree.  The
 * topology (rammification pattern) is governed by Markov models
 * (after the model created by Michael Renton) and the form is
 * governed by biomechanical principles (after the model created by
 * Julia Taylor-Hell).  The parameters are selected to generate trees
 * similar to thise of the Fuji cultivar.
 *
 *********************************************************************/

#include <cassert>
#include <climits>
#include <cmath>
#include <ctime>

#include <algorithm>
#include <iomanip>
#include <iterator>
#include <fstream>
#include <string>
#include <sstream>
#include <utility>
#include <vector>

#include "calendar.hpp"
#include "constants.hpp"
#include "ini.hpp"
#include "constrained_value.hpp"
#include "physics.hpp"
#include "quaternion.hpp"
#include "random.hpp"
#include "sequences.hpp"
#include "units.hpp"
#include "v3.hpp"

#include <lpfgall.h>

// The codes for the production groups
#define initialisation    0
#define update_parameters 1
#define update_structure  2
#define statistics        3
#define physics           4
#define write_l_string    5
#define write_mtg         6

namespace options {
  // Selection of what property should be rendered on the shoots
  //   bark          - use a bark-like colour
  //   observations  - colour encoding of the observations in the
  //                   sequences extracted from the Markov models
  //   zones         - colour encoding of the zones in the
  //                   sequences extracted from the Markov models
  //   reaction_wood - colour relative to the amount of reaction
  //                   wood in the outermost cambial layer
  //   years         - colour encoding the year of metamer appearance
  namespace render {
    enum {
      bark,
      observations,
      zones,
      reaction_wood,
      year
    } mode = bark;
  }

  // Set to true to override the Markov models with a pool draw for
  // the second year shoots
  const bool second_year_draws = false;

  // Select which data to write to files during the simulation
  //   sequences - The sequences of observations generated from
  //               the Markov models
  //   l_string  - The L-string
  //   counts    - The numbers of shoots generated per length
  //               category
  //   trunk     - Properties regarding the metamer adjacent to
  //               the root
  //   mtg       - An MTG representation of the tree
  namespace output {
    const bool sequences = false;
    const bool l_string  = false;
    const bool counts    = false;
    const bool trunk     = false;
    const bool mtg       = true;
  }

  // Set the simulation to end on the first day of a specified year
  const bool         end_on_year = true;
  const unsigned int end_year    = 2000;

  // Enable rupturing in branches
  const bool ruptures = false;

  // Set the trunk on a stake - for all the trunk metamers to remain
  // vertical
  const bool stake = true;

  // Disable the rotation calculations
  const bool disable_rotations = false; // disable mechanics (computation of bending) 

  // Read the parameters from the file "values.ini"
  const bool read_parameters_from_file = false;
}

// Define the indices for the colours used in the graphical output.
// The indices refer to entries to the material file specified as a
// command line option when lpfg is invoked.
namespace colours {
  const unsigned int background = 0;
  const unsigned int error      = 1;

  namespace observation {
    const unsigned int dormant = 2;
    const unsigned int large   = 3;
    const unsigned int medium  = 4;
    const unsigned int small   = 5;
    const unsigned int floral  = 6;
  }

  namespace zone {
    const unsigned int dormant_start =  7;
    const unsigned int small         =  8;
    const unsigned int diffuse       =  9;
    const unsigned int medium        = 10;
    const unsigned int floral        = 11;
    const unsigned int dormant_end   = 12;
    const unsigned int none          = 13;
  }

  const unsigned int fruit       = 14;
  const unsigned int leaf        = 15;
  const unsigned int autumn_leaf = 16;
  const unsigned int petal       = 17;
  const unsigned int stamen      = 18;
  const unsigned int bark        = 19;
  const unsigned int ground      = 20;

  namespace reaction_wood {
    const unsigned int none = 32;
    const unsigned int pi   = 47;
  }

  namespace year {
    const unsigned int base = 48;
    const unsigned int max  = 56;
  }
}

namespace observation {
  const unsigned int dormant   =  0;
  const unsigned int large     =  1;
  const unsigned int medium    =  2;
  const unsigned int small     =  3;
  const unsigned int floral    =  4;
  const unsigned int trunk     = 10;
  const unsigned int new_shoot = 11;
}

namespace zone {
  const unsigned int dormant_start =  0;
  const unsigned int small         =  1;
  const unsigned int diffuse       =  2;
  const unsigned int medium        =  3;
  const unsigned int floral        =  4;
  const unsigned int dormant_end   =  5;
  const unsigned int none          = 10;
}

namespace markov {
  const unsigned int  max_sequence_length = 100;
  const unsigned int  maximum_length      =  70;
  const unsigned int  minimum_length      =   4;
  Hidden_semi_markov* hsm_medium          =   0;
  Hidden_semi_markov* hsm_long            =   0;
  Hidden_semi_markov* hsm_short           =   0;
  Hidden_semi_markov* hsm_96_medium       =   0;
  Hidden_semi_markov* hsm_97_medium       =   0;
  Hidden_semi_markov* hsm_98_medium       =   0;
  Hidden_semi_markov* hsm_95_long         =   0;
  Hidden_semi_markov* hsm_96_long         =   0;
  Hidden_semi_markov* hsm_97_long         =   0;
  Hidden_semi_markov* hsm_98_long         =   0;
}

namespace world {
  const v3d gravity = v3d(0.0, -9.81, 0.0); // in m s^-2
}

namespace tree {
  unsigned int         growth_units                    = 0;
  const double         phyllotactic_angle              = -144.0 / 180.0 * constants::pi;
  const double         branching_angle                 =  -45.0 / 180.0 * constants::pi;
  const double         floral_branching_angle          =  -10.0 / 180.0 * constants::pi;
  v3d                  tropism                         = v3d(0.0, 0.1, 0.0); // in N
  const frame          initial_hlu                     = frame(v3d( 0.0, 1.0, 0.0),
                                                               v3d( 0.0, 0.0, 1.0),
                                                               v3d(-1.0, 0.0, 0.0));
  const double         spur_death_probability          = 0.3;
  const double         inflorescence_death_probability = 0.2;
  const unsigned int   preformed_leaves                = 8;
  unsigned int         fruits                          = 0;
  si::length<unit::cm> trunk_radius                    = 0.0;
  si::area<unit::cm2>  trunk_cross_sectional_area      = 0.0;
  si::perarea<>        fruit_load                      = 0.0;
  unsigned int         end_terminal_expansion          = convert_to_day(11, 1);
}

namespace wood {
  const si::density<unit::kilogrampermetrecubed> density                           = 1000.0;
  const double                                   reaction_wood_rate                =    0.5;
  si::scalar<>                                   reaction_wood_inertia_coefficient =    0.1;
  si::pressure<unit::gigapascal>                 youngs_modulus                    =    1.0;
}

namespace internode {
  const si::length<unit::mm> min_length        =  0.1;
  const si::time<unit::day>  elongation_period = 10.0;
  const si::time<unit::day>  plastochron       =  3.0;

  si::velocity<> growth_rate(unsigned int zone) {
    // Hypothesis: the elongation rate of an internode depends
    // the zone in which it appears
    switch (zone) {
    case zone::none:          return si::length<unit::cm>(3.0) / internode::elongation_period;
    case zone::dormant_start: return si::length<unit::cm>(0.5) / internode::elongation_period;
    case zone::small:         return si::length<unit::cm>(1.0) / internode::elongation_period;
    case zone::diffuse:       return si::length<unit::cm>(2.3) / internode::elongation_period;
    case zone::medium:        return si::length<unit::cm>(2.7) / internode::elongation_period;
    case zone::floral:        return si::length<unit::cm>(3.0) / internode::elongation_period;
    case zone::dormant_end:   return si::length<unit::cm>(0.6) / internode::elongation_period;
    default:                  return si::length<unit::cm>(2.0) / internode::elongation_period;
    }
  }
}

namespace pipe {
  double                             exponent                = 2.49;
  double                             exponent_invert         = 1.0 / pipe::exponent;

  const si::velocity<unit::mmperday> terminal_expansion_rate = 0.02;

  namespace max_terminal_radius {
    const si::length<unit::mm> minimum      = 0.75;
    const si::length<unit::mm> maximum      = 6.0;
    const si::length<unit::mm> radius_range = maximum - minimum;
    const si::scalar<>         length_range = markov::maximum_length - markov::minimum_length;

    // Hypothesis: a terminal apex expands to a maximum size based
    // on the number of leaves in a shoot
    si::length<> target(unsigned int length) {
      assert(length >= markov::minimum_length);
      return minimum + radius_range * si::scalar<>(length - markov::minimum_length) / length_range;
    }
  }
}

namespace leaf {
  const si::inverse_time<unit::perday>        fall_probability =   0.1;
  const si::time<unit::day>                   maturation       =  12.0;
  const si::massperarea<unit::gramspermetre2> mass_per_area    = 220.0;
  const si::area<unit::cm2>                   max_area         =  30.0;
  const si::area<unit::cm2>                   min_final_area   =  10.0;
  const si::area<unit::cm2>                   area_range       = max_area - min_final_area;
  si::length<unit::mm>                        petiole_radius   =   0.6;
}

namespace fruit {
  const si::time<unit::day>            flower_duration          =  10.0;
  double                               probability              =   0.3;
  si::masspertime<unit::gramsperday>   max_absolute_growth_rate =   1.8;
  const si::inverse_time<unit::perday> max_relative_growth_rate =   0.167;
  const si::time<unit::day>            lost_time                =  28.0;
  const si::time<unit::day>            max_age                  = 147.0;
}

namespace cambial {
  unsigned int no_layer = UINT_MAX;

  struct layer {
    layer() :
      under(no_layer),
      thickness(0.0),
      reaction_wood(0)
    {}

    unsigned int             under;
    si::length<>             thickness;
    double                   reaction_wood;
  };

  std::vector<layer> pool;

  unsigned int new_layer(unsigned int under = no_layer) {
    layer l;
    l.under = under;
    try {
      pool.push_back(l);
    }
    catch (...) {
      Printf("Additional memory for the cambial layers could not be allocated."
             "The simulation will now be halted.\n");
      Stop();
    }
    return pool.size() - 1;
  }

  layer& get(unsigned int i) {
    assert(i != no_layer);
    return pool.at(i);
  }

  void initialise_pool() {
    pool.clear();
    pool.reserve(10000);
  }

  si::length<> radius(unsigned int layer_index) {
    si::length<> r = 0.0;
    while (layer_index != no_layer) {
      r += pool[layer_index].thickness;
      layer_index = pool[layer_index].under;
    }
    return r;
  }
}

namespace output {
  namespace sequences {
    std::ofstream file;
    std::string   filename = "seq";
  }

  namespace l_string {
    std::ofstream file;
    std::string   filename = "l-string.lstr";

    const si::inverse_time<unit::peryear> frequency = 4.0;
    const si::time<>                      period    = si::scalar<>(1.0) / frequency;
    si::time<>                            elapsed   = 0.0;
  }

  namespace trunk {
    std::ofstream file;
    std::string   filename = "trunk";
  }

  namespace counts {
    std::ofstream file;
    std::string   filename = "counts";

    unsigned int shorts       = 0;
    unsigned int mediums      = 0;
    unsigned int longs        = 0;
    unsigned int florals      = 0;
    unsigned int len_16_to_25 = 0;
    unsigned int len_26_to_40 = 0;
    unsigned int len_over_40  = 0;
  }

  namespace mtg {
    std::ofstream file;
    std::string   filename = "mtg";
    std::string   date;

    const si::inverse_time<unit::peryear> frequency = 1.0;
    const si::time<>                      period    = si::scalar<>(1.0) / frequency;
    si::time<>                            elapsed   = 0.0;

    const unsigned int columns        = 10;
    unsigned int       current_column =  0;

    std::ostream_iterator<char> tab_iterator(file);

    void write_leading_tabs() {
      std::fill_n(tab_iterator, current_column, '\t');
    }

    void write_trailing_tabs() {
      std::fill_n(tab_iterator, columns - current_column, '\t');
    }

    void write_header() {
      file << "# MTG generated by MAppleT 2\n"
           << "#\n"
           << "# Symbols\n"
           << "#   T - tree\n"
           << "#   G - start of a growth unit of a vegetative shoot\n"
           << "#   I - start of a growth unit of an inflorescence\n"
           << "#   M - a metamer\n"
           << "# Features\n"
           << "#   date    - observation date\n"
           << "#   year    - year of creation\n"
           << "#   radius  - radius of an metemer in millimetres\n"
           << "#   length  - length of an metamer in millimetres\n"
           << "#   x, y, z - coordinates, in metres,  of the end of the internode in space\n\n"
           << "CODE:\tFORM-A\n"
           << "CLASSES:\n"
           << "SYMBOL\tSCALE\tDECOMPOSITION\tINDEXATION\tDEFINITION\n"
           << "$\t0\tFREE\tFREE\tEXPLICIT\n"
           << "T\t1\tLINEAR\tFREE\tEXPLICIT\n"
           << "G\t2\t<-LINEAR\tFREE\tEXPLICIT\n"
           << "I\t2\t<-LINEAR\tFREE\tEXPLICIT\n"
           << "M\t3\tNONE\tFREE\tEXPLICIT\n"
           << "\n"
           << "DESCRIPTION:\n"
           << "LEFT\tRIGHT\tRELTYPE\t MAX\n"
           << "G\tG,I\t+\t?\n"
           << "G\tG,I\t<\t1\n"
           << "I\tG,I\t+\t?\n"
           << "I\tG,I\t<\t1\n"
           << "M\tM\t+\t?\n"
           << "M\tM\t<\t1\n"
           << "\n"
           << "FEATURES:\n"
           << "NAME\tTYPE\n"
           << "TopDia\tREAL\n"
           << "XX\tREAL\n"
           << "YY\tREAL\n"
           << "ZZ\tREAL\n"
           << "date\tDD/MM/YY\n"
           << "year\tINT\n"
           << "length\tREAL\n"
           << "\n"
           << "MTG:\n"
           << "TOPO";
      write_trailing_tabs();
      file << "\tTopDia\tXX\tYY\tZZ\tdate\tyear\tlength\n";
    }
  }
}

namespace simulation {
  struct daily_data {
    daily_data() :
      bud_break(false),
      new_cambial_layer(false),
      pre_harvest(false),
      harvest(false),
      leaf_fall(false),
      leaf_forced_fall(false)
    {}

    bool bud_break;
    bool new_cambial_layer;
    bool pre_harvest;
    bool harvest;
    bool leaf_fall;
    bool leaf_forced_fall;
  };

  calendar<daily_data> cal;
  unsigned int         bud_break         = convert_to_day( 4, 15);
  unsigned int         new_cambial_layer = convert_to_day( 5, 15);
  unsigned int         pre_harvest       = convert_to_day(10, 29);
  unsigned int         harvest           = convert_to_day(10, 30);
  unsigned int         autumn            = convert_to_day(11,  1);
  unsigned int         leaf_fall_start   = convert_to_day(11, 15);
  unsigned int         leaf_fall_end     = convert_to_day(12, 15);
  unsigned int         phase             = initialisation;
  bool                 error             = false;
  unsigned int         seed              = 1163078257; //std::time(0);
  si::time<unit::day>  base_dt           = 0.5;
  si::time<unit::day>  dt                = base_dt;
  unsigned int         number            = 0;

  namespace rotation_convergence {
    const unsigned int steps = 2; // Runge-Kutta order 2
    const double       step  = 1.0 / double(steps);
  }

  namespace render {
    si::time<unit::day> period  = 1.0;
    si::time<>          elapsed = 0.0;
  }

  void next_phase(unsigned int p) {
    phase = p;
    UseGroup(p);
  }
}

struct apex_data {
  apex_data(frame hlu = frame(), unsigned int observation = observation::trunk) :
    sequence_position(0),
    observation(observation),
    parent_observation(observation::new_shoot),
    hlu(hlu),
    trunk(false)
  {}

  int sequence_position;

  std::pair<unsigned int, unsigned int> sequence[markov::max_sequence_length];

  unsigned int observation;
  unsigned int parent_observation;

  frame hlu;

  bool trunk;

  si::length<> radius;
  si::length<> target_radius; // maximum radius of a meristem
};

struct metamer_data {
  metamer_data(bool floral = false, unsigned int number = 0, frame hlu = frame(),
               unsigned int zone = zone::none, unsigned int observation = 9, double p_angle = 0.0,
               double b_angle = 0.0) :
    number(number),
    observation(observation),
    zone(zone),
    hlu(hlu),
    length(internode::min_length),
    radius(leaf::petiole_radius),
    cumulated_mass(),
    cumulated_torque(),
    developped(false),
    phyllotactic_angle(p_angle),
    branching_angle(b_angle),
    age(0.0),
    year(0),
    rigidity(0.0),
    fruit_state(floral ? flower : no_flower),
    fruit_mass(0.0),
    leaf_state(leaf),
    leaf_mass(0.0),
    trunk(false),
    pre_harvest_mass(),
    pre_harvest_radius(),
    pre_harvest_rotation()
  {
    // The conditional on 'number' is to get around a bug in LPFG.
    // LPFG creates lots of temporary instances of objects that are
    // never used.  We only want the constructor to have an effect
    // when the object is one that is actually used in the structure
    // and not a temporary object.
    if (number) {
      season_initial_heading = hlu.heading;
      external_layer = cambial::new_layer();
      cambial::get(external_layer).thickness = radius;
    }
  }

  unsigned int number; // rank in the Markovian sequence, starting from 1
  unsigned int observation; 
  unsigned int zone;

  frame          hlu;
  si::length<>   length;
  si::length<>   radius;
  si::mass<>     cumulated_mass;
  v3d            cumulated_torque;
  v3d            rotation_memory; // remaining rotation after harvest
  v3d            rotation_velocity; // = acting_rotation + rotation_memory
  v3d            acting_rotation; // due to mass and tropism actions
  v3d            position;        // absolute
  bool           developped;      // to avoid more than 1 lateral shoot
  d_0_2pi        phyllotactic_angle; // azimuth / parent metamer (around h)
  d_0_2pi        branching_angle;
  si::time<>     age;
  unsigned int   year;
  si::rigidity<> rigidity;
  v3d            season_initial_heading; // used to compute reaction wood
  unsigned int   external_layer; // index in vector cambial::pool

  enum {
    no_flower,
    flower,
    fruit,
    fruit_scar
  } fruit_state;

  si::mass<> fruit_mass;

  enum {
    leaf,
    leaf_scar
  } leaf_state;

  si::mass<> leaf_mass;

  bool trunk; // is it on the trunk 

  si::mass<>   pre_harvest_mass; // used to compute rotation_memory
  si::length<> pre_harvest_radius;
  v3d          pre_harvest_rotation;
};

struct growth_unit_data { // used for MTG output
  growth_unit_data(unsigned index = 0, unsigned int year = 0, bool inflorescence = false) :
    index(index),
    year(year),
    inflorescence(inflorescence)
  {}

  unsigned int index;
  unsigned int year;
  bool         inflorescence;
};

unsigned int length_pool() {
  // Probabilities for selecting the length of long shoots
  double pool_1995[] = {0.111, 0.222, 0.667};
  double pool_1996[] = {0.538, 0.346, 0.116};
  double pool_1997[] = {0.830, 0.170, 0.000};
  double pool_1998[] = {0.940, 0.060, 0.000};
  double pool_1999[] = {0.965, 0.035, 0.000};

  switch (simulation::cal.year()) {
  case 1994:
  case 1995: return non_parametric_distribution(pool_1995, 3);
  case 1996: return non_parametric_distribution(pool_1996, 3);
  case 1997: return non_parametric_distribution(pool_1997, 3);
  case 1998: return non_parametric_distribution(pool_1998, 3);
  default:   return non_parametric_distribution(pool_1999, 3);
  }
}

// Generation of sequences from Markov chains, based directly on the work
// of Michael Renton
unsigned int generate_sequence(unsigned int observation,
                               std::pair<unsigned int, unsigned int>* sequence)
{
  switch (observation) {
  case observation::trunk:  return generate_trunk(sequence);
  case observation::small:  return generate_short_sequence(sequence);
  case observation::floral: return generate_floral_sequence(sequence);
  case observation::medium: return generate_bounded_hsm_sequence(markov::hsm_medium,
                                                                 sequence, 5, 15);
  case observation::large:
    if (options::second_year_draws and simulation::cal.year() == 1995)
      return generate_random_draw_sequence(sequence);
    else
      switch (length_pool()) {
      case 1: return generate_bounded_hsm_sequence(markov::hsm_long, sequence, 15, 26);
      case 2: return generate_bounded_hsm_sequence(markov::hsm_long, sequence, 26, 41);
      case 3: return generate_bounded_hsm_sequence(markov::hsm_long, sequence, 41,
                                                   markov::maximum_length);
      default:
        Printf("ERROR: Bad length pool category.\n");
        simulation::error = true;
      }
  default:
    simulation::error = true;
    Printf("ERROR: A bad sequence observation (%d)"
           "was passed to generate_sequence().\n", observation);
    return 0;
  }
}

// The expolinear model of fruit growth (Lakso et al., 1995)
si::mass<> fruit_mass(si::time<> age) { // default mass unit = kg, time unit = second, ...
  si::time<> fruit_age = std::min<si::time<> >(age - fruit::flower_duration, fruit::max_age);
  si::mass<> r = fruit::max_absolute_growth_rate / fruit::max_relative_growth_rate;
  si::scalar<> i = std::log(1.0 + std::exp((fruit::max_relative_growth_rate
                                            * (fruit_age - fruit::lost_time)).value));
  return r * i;
}

si::area<> leaf_area(si::time<> age, unsigned int number) {
  si::scalar<> maturity = age / leaf::maturation;

  if (maturity.value > 1.0) maturity = 1.0;

  // Hypothesis: The growth dynamic of a leaf's area follows
  // an S-curve
  si::scalar<> relative_area = func(_leaf_area, float(maturity.value));

  // Hypothesis: The first leaves are preformed and smaller.  The
  // smallest is at the base and they increase linearly in size to
  // the neoformed leaves.
  if (number >= tree::preformed_leaves)
    return leaf::max_area * relative_area;
  else
    return relative_area * (si::scalar<>(double(number) / double(tree::preformed_leaves))
                            * leaf::area_range + leaf::min_final_area);
}

si::mass<> leaf_mass(si::area<> a) {
  return a * leaf::mass_per_area;
}

void organ_activity(metamer_data& m) { // for fruits and leaves
  switch (m.fruit_state) {
  case metamer_data::no_flower:
    if (simulation::cal.current_data().harvest)
      m.fruit_state = metamer_data::fruit_scar;
    break;
  case metamer_data::flower:
    if (m.age > fruit::flower_duration) {
      if (boolean_event(fruit::probability)) {
        m.fruit_state = metamer_data::fruit;
        ++tree::fruits;
      }
      else
        m.fruit_state = metamer_data::fruit_scar;
    }
    break;
  case metamer_data::fruit:
    if (simulation::cal.current_data().harvest) {
      m.fruit_state = metamer_data::fruit_scar;
      m.fruit_mass = 0.0;
    }
    else
      m.fruit_mass = fruit_mass(m.age - fruit::flower_duration);
    break;
  case metamer_data::fruit_scar:
    m.fruit_mass = 0.0;
  }

  if (m.leaf_state != metamer_data::leaf_scar) {
    if (simulation::cal.current_data().leaf_fall) {
      if (boolean_event((leaf::fall_probability * simulation::dt).value))
        m.leaf_state = metamer_data::leaf_scar;
    }
    else if (simulation::cal.current_data().leaf_forced_fall)
      m.leaf_state = metamer_data::leaf_scar;

    if (m.leaf_state == metamer_data::leaf)
      m.leaf_mass = leaf_mass(leaf_area(m.age, m.number));
  }
}

// The reaction wood is proportional to the change in inclination
// over a season (Almeras, 2001).
// Hypothesis: The reactino wood is also proportional to the
// inclination from gravity.
double reaction_wood_target(const v3d& up, const v3d& heading, const v3d& previous_heading) {
  double cos_gh = v3d(0.0, 1.0, 0.0) * heading;

  double cos_pu      = previous_heading * up;
  double cos_ph      = previous_heading * heading;
  double inclination = (cos_pu * cos_ph >= 0.0) ? acos(cos_ph) : -acos(cos_ph);
  double percentage  = 0.1635 * (1.0 - cos_gh) - 0.1778 * inclination; 
  double r           = constants::two_pi * percentage;

  if (r < 0.0)
    r = 0.0;
  else if (r > constants::pi)
    r = constants::pi;

  return r;
}

void calculate_rotation_velocity(metamer_data& m) {
  if (options::disable_rotations or (options::stake and m.trunk)) {
    m.rotation_velocity = v3d();
    return;
  }

  // Calculate the rotation velocity (Taylor-Hell, 2005)
  m.acting_rotation
    = calculate_rotation_velocity(m.cumulated_torque, m.rigidity.value);

  // Hypothesis: the shape memory is proportional to the mass
  // removed (inspired by Almeras. 2002)
  if (simulation::cal.current_data().harvest) {
    si::scalar<> delta_mass = (m.pre_harvest_mass - m.cumulated_mass) / m.pre_harvest_mass;
    m.rotation_memory = m.pre_harvest_rotation * delta_mass.value;
  }

  v3d new_rotation_velocity = m.acting_rotation + m.rotation_memory;

  // Hypothesis: The total rotation velocity is the sum of the acting
  // rotation and the shape memory
  m.rotation_velocity = simulation::rotation_convergence::step * new_rotation_velocity
    + (1.0 - simulation::rotation_convergence::step) * m.rotation_velocity;
}

void update_metamer_parameters(metamer_data& m) {
  m.age += simulation::dt;

  if (m.year < simulation::cal.year() and simulation::cal.current_data().new_cambial_layer) {
    m.external_layer = cambial::new_layer(m.external_layer);
    m.season_initial_heading = m.hlu.heading;
  }

  if (cambial::get(m.external_layer).under != cambial::no_layer) {
    double r = reaction_wood_target(m.hlu.up, m.hlu.heading, m.season_initial_heading);
    if (r > cambial::get(m.external_layer).reaction_wood)
      cambial::get(m.external_layer).reaction_wood += wood::reaction_wood_rate
        * simulation::dt.value * (r - cambial::get(m.external_layer).reaction_wood);
  }

  organ_activity(m);

  if (m.age < internode::elongation_period)
    m.length += internode::growth_rate(m.zone) * simulation::dt;

  si::secondmomentofarea<> second_moment_of_area = second_moment_of_area_circle(m.radius);

  cambial::layer* l = &cambial::get(m.external_layer);
  while (l->under != cambial::no_layer) {
    second_moment_of_area += wood::reaction_wood_inertia_coefficient
      * second_moment_of_area_annular_section(cambial::radius(l->under), l->thickness,
                                              l->reaction_wood);
    l = &cambial::get(l->under);
  }

  m.rigidity = second_moment_of_area * wood::youngs_modulus;

  if (simulation::cal.current_data().pre_harvest) {
    m.pre_harvest_mass = m.cumulated_mass;
    m.pre_harvest_rotation = m.rotation_velocity;
  }

  if (simulation::cal.current_data().bud_break)
    m.pre_harvest_radius = m.radius;
}

template <typename T> T clamp_if_near_zero(const T& val, const T& tolerance = 0.0001) {
  return (val < tolerance and val > -tolerance) ? T() : val;
}

void clamp_v3d_components_if_near_zero(v3d& v) {
  v.x = clamp_if_near_zero(v.x);
  v.y = clamp_if_near_zero(v.y);
  v.z = clamp_if_near_zero(v.z);
}

module apex(apex_data);
module branch();
module growth_unit(growth_unit_data);
module initialisation_error_sentinel();
module metamer(metamer_data);
module root();

Start: {
  simulation::error = false;

  check_probabilities();  // check for stochastic matrices' validity representing succession prob on
                          // a given axis

  if (options::read_parameters_from_file) {
    ini::values values;
    ini::read("values.ini", values);

    try {
      // This is where the parameters are read from values.ini.  New
      // variables to read from the file can be added here.  Make sure
      // that any variables read from a file are not qualified as 'const'.
      ini::get(values, "counter",        simulation::number);
      ini::get(values, "seed",           simulation::seed);
      ini::get(values, "youngs_modulus", wood::youngs_modulus);
      ini::get(values, "pipe_exponent",  pipe::exponent);
      ini::get(values, "petiole_radius", leaf::petiole_radius);
      ini::get(values, "fruit_prob",     fruit::probability);
      ini::get(values, "fruit",          fruit::max_absolute_growth_rate);
      ini::get(values, "reaction_wood",  wood::reaction_wood_inertia_coefficient);

      if (ini::exists("tropism", values))
        tree::tropism.y = ini::get<double>(values, "tropism");
    }
    catch (std::logic_error le) {
      Printf("ERROR: There was an error in the parameter file (%s)\n", le.what());
      simulation::error = true;
    }

    pipe::exponent_invert = 1.0 / pipe::exponent;
  }

  simulation::cal.reset_time();

  // This is the initial simulation year, it is set to 1994 to match
  // the observerved trees in the Markov models
  simulation::cal.current_year = 1994;

  simulation::cal[simulation::bud_break].bud_break                 = true;
  simulation::cal[simulation::new_cambial_layer].new_cambial_layer = true;
  simulation::cal[simulation::pre_harvest].pre_harvest             = true;
  simulation::cal[simulation::harvest].harvest                     = true;

  for (unsigned int i = simulation::leaf_fall_start; i < simulation::leaf_fall_end; ++i)
    simulation::cal[i].leaf_fall = true;

  simulation::cal[simulation::leaf_fall_end].leaf_forced_fall = true;

  simulation::cal.increment = simulation::dt.value;

  simulation::phase = initialisation;

  Printf("The seed is %d\n", simulation::seed);

  seed_random_number_generator(simulation::seed);

  std::string error_message;

  // Initialise the Markov chains from files.  Different statistical models
  // can be used by changing the file names here.  N.b., errors in the Markov
  // chain files are the most common reason for an initialisation error.
  markov::hsm_96_medium = hsm_init("fmodel_fuji_5_15_y3_96.txt", error_message);
  if (not markov::hsm_96_medium) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }
  markov::hsm_97_medium = hsm_init("fmodel_fuji_5_15_y4_97.txt", error_message);
  if (not markov::hsm_97_medium) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }
  markov::hsm_98_medium = hsm_init("fmodel_fuji_5_15_y5_98.txt", error_message);
  if (not markov::hsm_98_medium) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }

  markov::hsm_95_long = hsm_init("fmodel_fuji_y12.txt", error_message);
  if (not markov::hsm_95_long) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }
  markov::hsm_96_long = hsm_init("fmodel_fuji_16_65_y3_96.txt", error_message);
  if (not markov::hsm_96_long) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }
  markov::hsm_97_long = hsm_init("fmodel_fuji_16_65_y4_97.txt", error_message);
  if (not markov::hsm_97_long) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }
  markov::hsm_98_long = hsm_init("fmodel_fuji_16_65_y5_98.txt", error_message);
  if (not markov::hsm_98_long) {
    simulation::error = true;
    Printf("%s\n", error_message.c_str());
  }

  if (options::output::sequences) {
    std::ostringstream seedstr;
    seedstr << simulation::seed;
    output::sequences::filename += seedstr.str();
    output::sequences::filename += ".txt";
    output::sequences::file.open(output::sequences::filename.c_str());
    if (not output::sequences::file)
      simulation::error = true;
    else
      output::sequences::file << "1 VARIABLE\n\nVARIABLE 1 : VALUE\n\n";
  }

  if (options::output::l_string) {
    output::l_string::file.open(output::l_string::filename.c_str());
    if (not output::l_string::file) simulation::error = true;
    output::l_string::elapsed = 0.0;
  }

  if (options::output::trunk) {
    std::ostringstream seedstr;
    seedstr << '_' << simulation::number << '_' << simulation::seed;
    output::trunk::filename += seedstr.str();
    output::trunk::filename += ".dat";
    output::trunk::file.open(output::trunk::filename.c_str());
    if (not output::trunk::file) simulation::error = true;
  }

  if (options::output::counts) {
    std::ostringstream seedstr;
    seedstr << '_' << simulation::number << '_' << simulation::seed;
    output::counts::filename += seedstr.str();
    output::counts::filename += ".txt";
    output::counts::file.open(output::counts::filename.c_str());
    if (!output::counts::file) simulation::error = true;

    output::counts::shorts       = 0;
    output::counts::mediums      = 0;
    output::counts::longs        = 0;
    output::counts::florals      = 0;
    output::counts::len_16_to_25 = 0;
    output::counts::len_26_to_40 = 0;
    output::counts::len_over_40  = 0;
  }

  tree::growth_units               = 0;
  tree::fruits                     = 0;
  tree::trunk_cross_sectional_area = 0.0;
  tree::fruit_load                 = 0.0;
}

StartEach: {
  // Selection of the Markov model by year.  If the initial year
  // is changed, or different Markov models are used, this should
  // be changed accordingly.
  switch (simulation::cal.year()) {
  case 1994:
  case 1995:
    markov::hsm_medium = markov::hsm_96_medium;
    markov::hsm_long   = markov::hsm_95_long;
    break;
  case 1996:
    markov::hsm_medium = markov::hsm_96_medium;
    markov::hsm_long   = markov::hsm_96_long;
    break;
  case 1997:
    markov::hsm_medium = markov::hsm_97_medium;
    markov::hsm_long   = markov::hsm_97_long;
    break;
  default:
    markov::hsm_medium = markov::hsm_98_medium;
    markov::hsm_long   = markov::hsm_98_long;
  }
}

EndEach: {
  if (simulation::error) {
    Printf("An error was encountered.  The simulation was aborted.\n");
    Stop();
  }

  if (options::end_on_year
      and options::end_year == simulation::cal.year()
      and simulation::cal.current_time > 1.0) {
    Printf("The simulation has ended on January 1st, %d\n", options::end_year);
    Stop();
  }

  // This switch controls the selection of which group of
  // productions to apply.  The general sequence is
  //
  //   initialisation --> update parameters --> output (L-string or MTG) --> physics
  //     --> statistics --> update structure --> update parameters
  //
  // Rendering happens after 'update parameters'.  'output' is only
  // called conditionally; mostly, the simulation goes straight from
  // 'output parameters' to 'physics'

  switch (simulation::phase) {
  case initialisation:
    simulation::next_phase(update_parameters);
    break;
  case update_parameters:
    simulation::render::elapsed += simulation::dt;

    if (simulation::render::elapsed >= simulation::render::period) {
      simulation::render::elapsed -= simulation::render::period;
      DisplayFrame();

      unsigned int d     = (unsigned int)(simulation::cal.current_time) + 1;
      unsigned int day   = 0;
      unsigned int month = 0;
      day_and_month(d, day, month);
      Printf("%d/%d/%d\n", day, month, simulation::cal.year());

      if (options::output::trunk) {
        output::trunk::file
          << day << '/' << month << '/' << simulation::cal.year() << '\t'
          << tree::trunk_radius << '\t'
          << tree::trunk_cross_sectional_area << std::endl;
      }
    }

    {
      static unsigned int numerical_resolution_counter = 0;

      if (++numerical_resolution_counter < simulation::rotation_convergence::steps)
        simulation::dt = 0.0;
      else {
        simulation::dt = simulation::base_dt;
        numerical_resolution_counter = 0;
      }
    }

    simulation::cal.increment = simulation::dt.value;
    simulation::cal.advance();

    if (simulation::cal.current_data().harvest)
      tree::fruits = 0;

    if (options::output::mtg) {
      output::mtg::elapsed += simulation::dt;
      if (output::mtg::elapsed >= output::mtg::period) {
        output::mtg::elapsed = 0.0;
        simulation::next_phase(write_mtg);
        break;
      }
    }

    if (options::output::l_string) {
      output::l_string::elapsed += simulation::dt;
      if (output::l_string::elapsed >= output::l_string::period) {
        output::l_string::elapsed = 0.0;
        simulation::next_phase(write_l_string);
        break;
      }
    }

    if (options::output::counts
        and simulation::cal.current_time >= 365.0 - simulation::dt.value) {
      output::counts::file
        << output::counts::shorts  << "\t"
        << output::counts::longs   << "\t"
        << output::counts::florals << "\t"
        << "0\t"
        << output::counts::mediums << "\t"
        << output::counts::len_16_to_25 << "\t"
        << output::counts::len_26_to_40 << "\t"
        << output::counts::len_over_40  << std::endl;

      output::counts::shorts       = 0;
      output::counts::mediums      = 0;
      output::counts::longs        = 0;
      output::counts::florals      = 0;
      output::counts::len_16_to_25 = 0;
      output::counts::len_26_to_40 = 0;
      output::counts::len_over_40  = 0;
    }

    simulation::next_phase(physics);
    Backward();
    break;
  case statistics:
    simulation::next_phase(update_structure);
    break;
  case physics:
    simulation::next_phase(statistics);
    Forward();
    break;
  case update_structure:
    simulation::next_phase(update_parameters);
    break;
  case write_l_string:
    output::l_string::file << "\n";
  case write_mtg:
    simulation::next_phase(physics);
    Backward();
    break;
  default:
    Printf("ERROR: An unknown simulation phase was encountered.\n");
    Stop();
  }
}

End: {
  destroy_hsm(markov::hsm_96_medium);
  destroy_hsm(markov::hsm_97_medium);
  destroy_hsm(markov::hsm_98_medium);
  destroy_hsm(markov::hsm_95_long);
  destroy_hsm(markov::hsm_96_long);
  destroy_hsm(markov::hsm_97_long);
  destroy_hsm(markov::hsm_98_long);

  output::sequences::file.close();

  clock_t sim_time = std::clock() / CLOCKS_PER_SEC;

  Printf("The simulation took %d minutes and %d seconds.\n",
         sim_time / 60, sim_time % 60);
}

derivation length: INT_MAX;

axiom: initialisation_error_sentinel();

ignore: growth_unit;

// The L-system starts with this group.  If there were any errors
// in the initialisations in Start, pruduce an error message;
// otherwise, start the simulation.
group initialisation:

initialisation_error_sentinel(): {
  if (simulation::error)
    produce SetColor(colours::error) Label("ERROR");
  else {
    apex_data a = apex_data(frame(tree::initial_hlu));
    a.trunk = true;
    produce root() apex(a);
  }
}

// Update the parameters of each metamer (age, reaction woord,
// organs, length, rigidity & shape memory) and perform the
// geometric reconstruction (rotation and placement of each metamer)
group update_parameters:

metamer(ml) branch() << metamer(m): {
  update_metamer_parameters(m);

  m.hlu = rotate_frame_at_branch(ml.hlu, ml.branching_angle,  ml.phyllotactic_angle);
  m.hlu = reorient_frame(m.hlu, m.rotation_velocity, m.length);

  m.position = ml.position + m.length.value * m.hlu.heading;

  produce metamer(m);
}

metamer(ml) << metamer(m): {
  update_metamer_parameters(m);

  m.hlu = reorient_frame(ml.hlu, m.rotation_velocity, m.length);

  m.position = ml.position + m.length.value * m.hlu.heading;

  produce metamer(m);
}

metamer(m): {
  update_metamer_parameters(m);

  m.position = m.length.value * m.hlu.heading;

  produce metamer(m);
}

// Calculate the width (by the pipe model), cumulated mass, cumulated torque and
// rotation velocity of each metamer
group physics:

root() >> metamer(m): {
  tree::trunk_radius = m.radius;
  tree::trunk_cross_sectional_area = constants::pi * m.radius * m.radius;
  tree::fruit_load = si::scalar<>(tree::fruits) / tree::trunk_cross_sectional_area;
}

metamer(m) >> SB() branch() metamer(mb) EB() metamer(mr): {
  si::length<> radius = std::pow(std::pow(mb.radius.value, pipe::exponent)
                                 + std::pow(mr.radius.value, pipe::exponent),
                                 pipe::exponent_invert);

  if (m.leaf_state == metamer_data::leaf)
    radius = std::pow(std::pow(radius.value, pipe::exponent)
                      + std::pow(si::length<>(leaf::petiole_radius).value, pipe::exponent),
                      pipe::exponent_invert);

  m.radius = std::max(radius, m.radius);

  cambial::get(m.external_layer).thickness = m.radius
    - cambial::radius(cambial::get(m.external_layer).under);

  m.cumulated_mass = constants::pi * m.radius * m.radius * m.length * wood::density
    + m.fruit_mass + m.leaf_mass + mr.cumulated_mass + mb.cumulated_mass;

  m.cumulated_torque
    = ((mb.hlu.heading * mb.length.value)  // Colin's v3d: % = cross product
       % (world::gravity * si::mass<unit::kilogram>(mb.cumulated_mass).value))
    + ((mr.hlu.heading * mr.length.value)
       % (world::gravity * si::mass<unit::kilogram>(mr.cumulated_mass).value))
    + mb.cumulated_torque + mr.cumulated_torque
    + (m.length.value * m.hlu.heading) % tree::tropism;

  calculate_rotation_velocity(m);

  produce metamer(m);
}

metamer(m) >> metamer(mr): {
  si::length<> radius = mr.radius;

  if (m.leaf_state == metamer_data::leaf)
    radius = std::pow(std::pow(mr.radius.value, pipe::exponent)
                      + std::pow(si::length<>(leaf::petiole_radius).value, pipe::exponent),
                       pipe::exponent_invert);

  m.radius = std::max(radius, m.radius);

  cambial::get(m.external_layer).thickness = m.radius
    - cambial::radius(cambial::get(m.external_layer).under);

  m.cumulated_mass = constants::pi * m.radius * m.radius * m.length * wood::density
    + m.fruit_mass + m.leaf_mass + mr.cumulated_mass;

  m.cumulated_torque
    = ((mr.hlu.heading * mr.length.value)
       % (world::gravity * si::mass<unit::kilogram>(mr.cumulated_mass).value))
    + mr.cumulated_torque
    + (m.length.value * m.hlu.heading) % tree::tropism;

  calculate_rotation_velocity(m);

  produce metamer(m);
}

metamer(m) >> apex(a): {
  si::length<> radius = a.radius;

  if (m.leaf_state == metamer_data::leaf)
    radius = std::pow(std::pow(a.radius.value, pipe::exponent)
                      + std::pow(si::length<>(leaf::petiole_radius).value, pipe::exponent),
                       pipe::exponent_invert);

  m.radius = std::max(radius, m.radius);

  cambial::get(m.external_layer).thickness = m.radius
    - cambial::radius(cambial::get(m.external_layer).under);

  m.cumulated_mass = constants::pi * m.radius * m.radius * m.length * wood::density
    + m.fruit_mass + m.leaf_mass;

  m.cumulated_torque = (m.length.value * m.hlu.heading) % tree::tropism;

  calculate_rotation_velocity(m);

  produce metamer(m);
}

apex(a): {
  if (a.sequence_position == 0 and a.radius < a.target_radius)
    a.radius += pipe::terminal_expansion_rate * simulation::dt;
  produce apex(a);
}

// Generate new sequences
group statistics:

apex(a): {
  if (a.sequence_position == 0 and a.observation != observation::dormant and
      (a.parent_observation == observation::floral or simulation::cal.current_data().bud_break)) {

    unsigned int old_observation = a.observation;
    a.sequence_position          = generate_sequence(a.observation, a.sequence);

    if (a.observation == observation::trunk)
      a.observation = observation::large;
    else if (a.observation == observation::small and boolean_event(tree::spur_death_probability))
      a.observation = observation::dormant;
    else if (a.observation == observation::floral)
      a.observation = observation::dormant;
    else
      a.observation = terminal_fate(a.observation, simulation::cal.year());

    a.parent_observation = old_observation; // one int

    if (options::output::counts)
      switch (a.parent_observation) {
      case observation::floral: ++output::counts::florals; break;
      case observation::small:  ++output::counts::shorts;  break;
      case observation::medium: ++output::counts::mediums; break;
      case observation::large:
        ++output::counts::longs;
        if (a.sequence_position < 26)
          ++output::counts::len_16_to_25;
        else if (a.sequence_position < 41)
          ++output::counts::len_26_to_40;
        else
          ++output::counts::len_over_40;
      }

    a.radius = 0.0;
    a.target_radius = pipe::max_terminal_radius::target(a.sequence_position);

    if (options::output::sequences and
        simulation::cal.year() < 1999 and
        (a.parent_observation == observation::large or a.parent_observation == observation::medium))
      for (int i = a.sequence_position - 1; i >= 0; --i)
        output::sequences::file << a.sequence[i].second << (i > 0 ? ' ' : '\n');

    produce growth_unit(growth_unit_data(++tree::growth_units, simulation::cal.year(),
                                         a.parent_observation == observation::floral))
      apex(a);
  }
  else
    produce apex(a);
}

// Add new apices (terminal and lateral) and metamers
// to the structure
group update_structure:

metamer(m) < apex(a): {
  if (a.sequence_position > 0 and m.age >= internode::plastochron) {
    a.sequence_position--;

    double branching_angle = tree::branching_angle;
    branching_angle += random(-0.1, 0.1);
    bool flower = a.sequence_position == 0 and a.parent_observation == observation::floral;
    unsigned int number = m.year == simulation::cal.year() ? m.number + 1 : 1;
    metamer_data
      mn(metamer_data(flower, number, a.hlu, a.sequence[a.sequence_position].first,
                      a.sequence[a.sequence_position].second,
                      m.phyllotactic_angle + tree::phyllotactic_angle + random(-0.1, 0.1),
                      branching_angle));
    mn.trunk = a.trunk;
    mn.year = simulation::cal.year();

    produce metamer(mn) apex(a);
  }
  else produce apex(a);
}

apex(a): {
  if (a.sequence_position > 0) {
    a.sequence_position--;

    double branching_angle = tree::branching_angle;
    branching_angle += random(-0.1, 0.1);
    bool flower = a.sequence_position == 0 and a.parent_observation == observation::floral;

    metamer_data
      m(metamer_data(flower, 1, a.hlu, a.sequence[a.sequence_position].first,
                       a.sequence[a.sequence_position].second,
                       tree::phyllotactic_angle + random(-0.1, 0.1), branching_angle));
    m.trunk = a.trunk;
    m.year = simulation::cal.year();

    produce metamer(m) apex(a);
  }
  else produce apex(a);
}

metamer(m) > metamer(mr) apex(a): { // case of a floral immediate lateral axis: should be treated as
                                    // laterals and not as terminals
  if (not m.developped and a.parent_observation == observation::floral
      and a.sequence_position == 0) {
    m.developped = true;

    if (boolean_event(tree::inflorescence_death_probability))
      produce metamer(m);

    m.branching_angle = tree::floral_branching_angle + random(-0.1, 0.1);

    frame hlu
      = rotate_frame_at_branch(m.hlu, m.branching_angle, m.phyllotactic_angle);

    unsigned int observation = terminal_fate(observation::floral, simulation::cal.year());

    apex_data sylleptic_apex(hlu, observation);
    sylleptic_apex.parent_observation = observation::floral;

    produce metamer(m) SB() branch() apex(sylleptic_apex) EB();
  }
}

metamer(m): {
  if (options::ruptures and rupture(m.cumulated_torque, m.radius)) {
    Printf("EXTRAORDINARY EVENT: There was a rupture in the system.\n");
    produce Cut();
  }

  if (m.observation != observation::dormant and
      not m.developped and
      simulation::cal.current_data().bud_break) {
    m.developped = true;

    frame hlu
      = rotate_frame_at_branch(m.hlu, m.branching_angle, m.phyllotactic_angle);

    apex_data a(hlu, m.observation);

    produce metamer(m) SB() branch() apex(a) EB();
  }
  else produce metamer(m);
}

// Write the module names out to a file
group write_l_string:

root(): {
  unsigned int day   = 0;
  unsigned int month = 0;
  unsigned int year  = simulation::cal.year();

  day_and_month((unsigned int)simulation::cal.current_time, day, month);

  output::l_string::file
    << std::setw(2) << std::setfill('0') << day   << '/'
    << std::setw(2) << std::setfill('0') << month << '/'
    << std::setw(2) << std::setfill('0') << year
    << '\t'
    << "R";

  produce root();
}

growth_unit(u): {
  output::l_string::file << "G";
  produce growth_unit(u);
}

metamer(m): {
  output::l_string::file << "I";
  produce metamer(m);
}

SB(): {
  output::l_string::file << "[";
  produce SB();
}

EB(): {
  output::l_string::file << "]";
  produce EB();
}

// Write an MTG out to a file
group write_mtg:

root(): {
  std::ostringstream str, date;

  unsigned int day   = 0;
  unsigned int month = 0;
  unsigned int year  = simulation::cal.year();

  day_and_month((unsigned int)simulation::cal.current_time, day, month);

  std::string filename;
  str << output::mtg::filename << '_'
      << simulation::number << '_'
      << simulation::seed << '_'
      << std::setw(2) << std::setfill('0') << year  << '_'
      << std::setw(2) << std::setfill('0') << month << '_'
      << std::setw(2) << std::setfill('0') << day
      << ".mtg";
  filename = str.str();

  date << std::setw(2) << std::setfill('0') << year  << '/'
       << std::setw(2) << std::setfill('0') << month << '/'
       << std::setw(2) << std::setfill('0') << day % 100;
  output::mtg::date = date.str();

  if (output::mtg::file) {
    output::mtg::file << std::endl << std::endl;
    output::mtg::file.close();
  }

  output::mtg::file.clear();
  output::mtg::file.open(filename.c_str());

  if (!output::mtg::file) {
    Printf("ERROR: The file %s to write the MTG could not be opened.\n", filename.c_str());
    Stop();
  }

  output::mtg::write_header();

  output::mtg::current_column = 1;

  output::mtg::file << "/T1\t";
  output::mtg::write_trailing_tabs();
  output::mtg::file
    << std::scientific
    << '\t' << std::setprecision(4) << std::left << tree::trunk_radius.value * 2000.0
    << '\t' << std::setprecision(4) << std::left << 0.0
    << '\t' << std::setprecision(4) << std::left << 0.0
    << '\t' << std::setprecision(4) << std::left << 0.0
    << '\t' << output::mtg::date
    << '\t' << 1994
    << '\t' << std::setprecision(4) << std::left << 0.0
    << '\n';

  produce root();
}

branch() < growth_unit(u): {
  ++output::mtg::current_column;
  if (output::mtg::current_column > output::mtg::columns) {
    Printf("ERROR: Not enough columns were allocated for the MTG file.\n");
    Stop();
  }
  output::mtg::write_leading_tabs();
  output::mtg::file << '+' << (u.inflorescence ? 'I' : 'G') << u.index;
  output::mtg::write_trailing_tabs();
  output::mtg::file << "\t\t\t\t\t" << output::mtg::date << '\t' << u.year << '\n';

  produce growth_unit(u);
}

growth_unit(u): {
  output::mtg::write_leading_tabs();
  output::mtg::file << (u.index == 1 ? "/" : "^<") << (u.inflorescence ? 'I' : 'G') << u.index;
  output::mtg::write_trailing_tabs();
  if (u.index == 1)
    output::mtg::file
      << std::scientific
      << '\t' << std::setprecision(4) << std::left << tree::trunk_radius.value * 2000.0
      << '\t' << std::setprecision(4) << std::left << 0.0
      << '\t' << std::setprecision(4) << std::left << 0.0
      << '\t' << std::setprecision(4) << std::left << 0.0
      << '\t' << output::mtg::date
      << '\t' << u.year
      << '\t' << std::setprecision(4) << std::left << 0.0
      << '\n';
  else
    output::mtg::file << "\t\t\t\t\t" << output::mtg::date << '\t' << u.year << '\n';

  produce growth_unit(u);
}

metamer(m): {
  clamp_v3d_components_if_near_zero(m.position);

  output::mtg::write_leading_tabs();
  output::mtg::file << (m.number == 1 ? "^/M" : "^<M") << m.number;
  output::mtg::write_trailing_tabs();
  output::mtg::file
    << std::scientific
    << '\t' << std::setprecision(4) << std::left << m.radius.value * 2000.0
    << '\t' << std::setprecision(4) << std::left << m.position.x
    << '\t' << std::setprecision(4) << std::left << m.position.y
    << '\t' << std::setprecision(4) << std::left << m.position.z
    << '\t' << output::mtg::date
    << '\t' << m.year
    << '\t' << std::setprecision(4) << std::left << m.length.value * 1000.0
    << '\n';

  produce metamer(m);
}

apex(a): {
  assert(output::mtg::current_column > 0);
  --output::mtg::current_column;

  produce apex(a);
}

group 0:

// Graphical rendering of the tree
interpretation:

root(): {
  produce SB() SetColor(colours::ground) Surface(ground_surface, 10.0) EB();
}

metamer(m): {
  unsigned int shoot_colour = colours::error;

  switch (options::render::mode) {
  case options::render::bark:
    shoot_colour = colours::bark;
    break;
  case options::render::observations:
    switch (m.observation) {
    case observation::dormant: shoot_colour = colours::observation::dormant; break;
    case observation::large:   shoot_colour = colours::observation::large;   break;
    case observation::medium:  shoot_colour = colours::observation::medium;  break;
    case observation::small:   shoot_colour = colours::observation::small;   break;
    case observation::floral:  shoot_colour = colours::observation::floral;  break;
    default:
      shoot_colour = colours::error;
      Printf("ERROR: Bad observation %d\n", m.observation);
    }
    break;
  case options::render::zones:
    switch (m.zone) {
    case zone::dormant_start:
      shoot_colour = colours::zone::dormant_start;
      break;
    case zone::small:
      shoot_colour = colours::zone::small;
      break;
    case zone::diffuse:
      shoot_colour = colours::zone::diffuse;
      break;
    case zone::medium:
      shoot_colour = colours::zone::medium;
      break;
    case zone::floral:
      shoot_colour = colours::zone::floral;
      break;
    case zone::dormant_end:
      shoot_colour = colours::zone::dormant_end;
      break;
    case zone::none:
      shoot_colour = colours::zone::none;
      break;
    default:
      shoot_colour = colours::error;
      Printf("ERROR: Bad zone %d\n", m.zone);
    }
    break;
  case options::render::reaction_wood:
    shoot_colour = (unsigned int)((cambial::get(m.external_layer).reaction_wood / constants::pi)
                                  * (colours::reaction_wood::pi - colours::reaction_wood::none)
                                  + colours::reaction_wood::none);
    break;
  case options::render::year:
    shoot_colour = std::min(colours::year::base + m.year - 1994, colours::year::max);
    break;
  }

  nproduce
    SetHead(float(m.hlu.heading.x), float(m.hlu.heading.y), float(m.hlu.heading.z),
            float(m.hlu.up.x), float(m.hlu.up.y), float(m.hlu.up.z))
    SetWidth(float(m.radius.value)) SetColor(shoot_colour) F(float(m.length.value));

  if (m.fruit_state == metamer_data::flower) {
    nproduce
      SB()
      RollL(float(m.phyllotactic_angle * 180.0 / constants::pi))
      Up(45)
      SetColor(colours::stamen)
      SetWidth(0.0025f)
      SB()
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB() RollL(72.0)
      SB() Up(15) F(0.0125f) EB()
      EB()
      SetColor(colours::petal)
      Surface(petal_surface, 0.02f) RollL(144.0)
      Surface(petal_surface, 0.02f) RollL(144.0)
      Surface(petal_surface, 0.02f) RollL(144.0)
      Surface(petal_surface, 0.02f) RollL(144.0)
      Surface(petal_surface, 0.02f)
      EB();
  }
  else if (m.fruit_state == metamer_data::fruit) {
    double r = m.fruit_mass.value * 0.15;
    nproduce
      SB() RollL(float(m.phyllotactic_angle * 180.0 / constants::pi))
      Down(90.0f) f(float(r)) SetColor(colours::fruit) Sphere(float(r)) EB();
  }

  if (m.leaf_state == metamer_data::leaf) {
    double r = m.leaf_mass.value * 100.0;
    nproduce
      SB();

    if (simulation::cal.current_time < simulation::autumn)
      nproduce SetColor(colours::leaf);
    else
      nproduce SetColor(colours::autumn_leaf);

    nproduce RollL(float(m.phyllotactic_angle * 180.0 / constants::pi))
      Up(90.0f) SetWidth(0.002f) F(float(r * 0.1)) RollToVert()
      Surface(leaf_surface, float(r)) EB();
  }

  produce;
}
