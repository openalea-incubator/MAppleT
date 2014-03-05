#ifndef __RANDOM_HPP__
#define __RANDOM_HPP__

void         seed_random_number_generator(unsigned int seed);
double       random(double scale);
unsigned int random(unsigned int scale);
double       random(double low, double high);
bool         boolean_event(double probability);

#endif
