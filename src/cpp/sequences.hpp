#ifndef __SEQUENCES_HPP__
#define __SEQUENCES_HPP__

#include <string>
#include <utility>

class Hidden_semi_markov;

Hidden_semi_markov* hsm_init(std::string filename, std::string& err_msg);
void         destroy_hsm(Hidden_semi_markov* hsm);
void         check_probabilities();
unsigned int non_parametric_distribution(double const* probabilities, unsigned int length);
unsigned int generate_bounded_hsm_sequence(Hidden_semi_markov* hsm, std::pair<unsigned int, unsigned int>* seq,
					   unsigned int lower_bound, unsigned int upper_bound);
unsigned int generate_short_sequence(std::pair<unsigned int, unsigned int>* seq);
unsigned int generate_floral_sequence(std::pair<unsigned int, unsigned int>* seq);
unsigned int generate_trunk(std::pair<unsigned int, unsigned int>* seq);
unsigned int generate_random_draw_sequence(std::pair<unsigned int, unsigned int>* seq);
unsigned int terminal_fate(unsigned int code, unsigned int parent_code);

#endif
