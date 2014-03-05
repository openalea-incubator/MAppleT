#include <cassert>
#include <cstdlib>

#include "random.hpp"

// Comment the following line in to use the random number generator
// from the Boost library instead of the standard library.  The Boost
// library is usually faster, but most people don't have it installed.
// To keep this maximally portable, the default is to use the standard
// library.

// #define __USE_BOOST_FOR_RANDOM_NUMBERS__

#ifdef __USE_BOOST_FOR_RANDOM_NUMBERS__

#include <boost/random.hpp>

namespace {
  boost::minstd_rand generator(1);
  boost::uniform_real<> uni_dist(0, 1);
  boost::variate_generator<boost::minstd_rand&, boost::uniform_real<> > uni(generator, uni_dist);
}

void seed_random_number_generator(unsigned int seed) {
  generator.seed(seed);

  // It appears that the first value of sequences that start with
  // close seeds are also close.  So, the sequence is reseeded 10
  // times to add some noise to the initial values.  This is probably
  // overkill (the second values of each sequence appear sufficiently
  // random), but it is certain to behave.
  for (unsigned int i = 0; i < 10; ++i)
    generator.seed(random(UINT_MAX));
  for (unsigned int i = 0; i < 10; ++i)
    random(UINT_MAX);
}

#else

inline double uni() {
  return rand() / double(RAND_MAX + 1.);
}

#endif

void seed_random_number_generator(unsigned int seed) {
  std::srand(seed);
}

double random(double scale) {
  return scale * uni();
}

unsigned int random(unsigned int scale) {
  return (unsigned int)(scale * uni());
}

double random(double low, double high) {
  double range = high - low;
  return low + range * uni();
}

bool boolean_event(double probability) {
  assert(probability >= 0.0 and probability <= 1.0);
  return uni() < probability;
}
