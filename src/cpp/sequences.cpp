#include <cassert>

#include <sstream>
#include <utility>

#include "stat_tool/stat_tools.h"
#include "stat_tool/markovian.h"
#include "stat_tool/curves.h"
#include "sequence_analysis/sequences.h"
#include "sequence_analysis/sequence_label.h"
#include "sequence_analysis/semi_markov.h"
#include "sequence_analysis/hidden_semi_markov.h"
#include "sequence_analysis/variable_order_markov.h"
#include "sequence_analysis/hidden_variable_order_markov.h"


#include "random.hpp"
#include "sequences.hpp"
#include "range.hpp"

namespace {
  static const double prob_1995_large [] = {0.500, 0.167, 0.000, 0.333};
  static const double prob_1995_medium[] = {0.000, 0.000, 0.000, 1.000};
  static const double prob_1995_small [] = {0.500, 0.000, 0.000, 0.500};
  static const double prob_1995_floral[] = {0.400, 0.000, 0.600, 0.000};

  static const double prob_1996_large [] = {0.246, 0.185, 0.000, 0.569};
  static const double prob_1996_medium[] = {0.016, 0.238, 0.032, 0.714};
  static const double prob_1996_small [] = {0.066, 0.067, 0.317, 0.550};
  static const double prob_1996_floral[] = {0.317, 0.250, 0.434, 0.000};

  static const double prob_1997_large [] = {0.351, 0.106, 0.010, 0.532};
  static const double prob_1997_medium[] = {0.123, 0.148, 0.063, 0.666};
  static const double prob_1997_small [] = {0.015, 0.094, 0.453, 0.438};
  static const double prob_1997_floral[] = {0.182, 0.249, 0.569, 0.000};

  static const double prob_1998_large [] = {0.213, 0.082, 0.000, 0.705};
  static const double prob_1998_medium[] = {0.027, 0.046, 0.016, 0.911};
  static const double prob_1998_small [] = {0.000, 0.024, 0.205, 0.771};
  static const double prob_1998_floral[] = {0.003, 0.413, 0.584, 0.000};

  static const double prob_1999_large [] = {0.100, 0.050, 0.000, 0.850};
  static const double prob_1999_medium[] = {0.000, 0.020, 0.130, 0.850};
  static const double prob_1999_small [] = {0.000, 0.000, 0.375, 0.625};
  static const double prob_1999_floral[] = {0.008, 0.325, 0.667, 0.000};

  static const double prob_2000_large [] = {0.000, 0.100, 0.000, 0.900};
  static const double prob_2000_medium[] = {0.000, 0.050, 0.050, 0.900};
  static const double prob_2000_small [] = {0.000, 0.000, 0.350, 0.650};
  static const double prob_2000_floral[] = {0.000, 0.200, 0.800, 0.000};
}

unsigned int terminal_fate(unsigned int code, unsigned int year) {
  unsigned int index = 0;

  switch (year) {
  case 1994:
  case 1995:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_1995_large,  4); break;
    case 2: index = non_parametric_distribution(prob_1995_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_1995_small,  4); break;
    case 4: index = non_parametric_distribution(prob_1995_floral, 4); break;
    }
    break;
  case 1996:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_1996_large,  4); break;
    case 2: index = non_parametric_distribution(prob_1996_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_1996_small,  4); break;
    case 4: index = non_parametric_distribution(prob_1996_floral, 4); break;
    }
    break;
  case 1997:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_1997_large,  4); break;
    case 2: index = non_parametric_distribution(prob_1997_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_1997_small,  4); break;
    case 4: index = non_parametric_distribution(prob_1997_floral, 4); break;
    }
    break;
  case 1998:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_1998_large,  4); break;
    case 2: index = non_parametric_distribution(prob_1998_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_1998_small,  4); break;
    case 4: index = non_parametric_distribution(prob_1998_floral, 4); break;
    }
    break;
  case 1999:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_1999_large,  4); break;
    case 2: index = non_parametric_distribution(prob_1999_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_1999_small,  4); break;
    case 4: index = non_parametric_distribution(prob_1999_floral, 4); break;
    }
    break;
  default:
    switch (code) {
    case 1: index = non_parametric_distribution(prob_2000_large,  4); break;
    case 2: index = non_parametric_distribution(prob_2000_medium, 4); break;
    case 3: index = non_parametric_distribution(prob_2000_small,  4); break;
    case 4: index = non_parametric_distribution(prob_2000_floral, 4); break;
    }
    break;
  }

  assert(index > 0 and index < 5);

  return index;
}

void reverse_sequence(std::pair<unsigned int, unsigned int>* seq, unsigned int length) {
  const unsigned int half_length = length / 2;
  for (unsigned int i = 0; i < half_length; ++i)
    std::swap(seq[i], seq[length - i]);
}

void assert_sum_is_one(double const* probabilities, const unsigned int length, const double error = 0.001) {
  double sum = 0.0;

  for (unsigned int i = 0; i < length; ++i)
    sum += probabilities[i];

  assert(sum >= 1.0 - error and sum <= 1.0 + error);
}

void check_probabilities() {
  assert_sum_is_one(prob_1995_large,  4);
  assert_sum_is_one(prob_1995_medium, 4);
  assert_sum_is_one(prob_1995_small,  4);
  assert_sum_is_one(prob_1995_floral, 4);
  assert_sum_is_one(prob_1996_large,  4);
  assert_sum_is_one(prob_1996_medium, 4);
  assert_sum_is_one(prob_1996_small,  4);
  assert_sum_is_one(prob_1996_floral, 4);
  assert_sum_is_one(prob_1997_large,  4);
  assert_sum_is_one(prob_1997_medium, 4);
  assert_sum_is_one(prob_1997_small,  4);
  assert_sum_is_one(prob_1997_floral, 4);
  assert_sum_is_one(prob_1998_large,  4);
  assert_sum_is_one(prob_1998_medium, 4);
  assert_sum_is_one(prob_1998_small,  4);
  assert_sum_is_one(prob_1998_floral, 4);
  assert_sum_is_one(prob_1999_large,  4);
  assert_sum_is_one(prob_1999_medium, 4);
  assert_sum_is_one(prob_1999_small,  4);
  assert_sum_is_one(prob_1999_floral, 4);
  assert_sum_is_one(prob_2000_large,  4);
  assert_sum_is_one(prob_2000_medium, 4);
  assert_sum_is_one(prob_2000_small,  4);
  assert_sum_is_one(prob_2000_floral, 4);
}

unsigned int non_parametric_distribution(double const* probabilities, unsigned int length) {
  const double target     = random(1.0);
  double       cumulation = 0.0;
  unsigned int i          = 0;

  while (i < length and cumulation < target)
    cumulation += probabilities[i++];

  return i;
}

Hidden_semi_markov* hsm_init(std::string filename, std::string& err_msg) {
  Format_error error;
  std::ostringstream str;
  Hidden_semi_markov* hsm = 0;

  hsm = hidden_semi_markov_ascii_read(error , filename.c_str());
  str << error;

  err_msg = str.str();

  return hsm;
}

Hidden_variable_order_markov* hvm_init(std::string filename) {
  Format_error error;
  std::ostringstream str;
  Hidden_variable_order_markov* hvm = 0;

  hvm = hidden_variable_order_markov_ascii_read(error , filename.c_str());
  str << error;

  return hvm;
}

unsigned int generate_hsm_sequence(Hidden_semi_markov* hsm, std::pair<unsigned int, unsigned int>* seq) {
  // This data should not be producing sequences longer than 100
  // elements
  const int sequence_length = 100;

  // Generate a Markov sequence
  Semi_markov_iterator smiter(hsm);
  int** sequence = smiter.simulation(sequence_length, true);
  const int processes = hsm->get_nb_output_process() + 1;

  int i = 0;
  for (; i < sequence_length; ++i) {
    if (sequence[0][i] == 6) break;
    seq[i].first  = sequence[0][i];
    seq[i].second = sequence[1][i];
  }

  // Delete the sequence matrix
  for (int i = 0; i < processes; ++i)
    delete[] sequence[i];
  delete[] sequence;

  reverse_sequence(seq, i - 1);

  return i - 1;
}

unsigned int generate_bounded_hsm_sequence(Hidden_semi_markov* hsm, std::pair<unsigned int, unsigned int>* seq, unsigned int lower_bound, unsigned int upper_bound) {
  unsigned int length = upper_bound + 1; // defines a max length for the sequence (cf lsystem.l)
  do
    length = generate_hsm_sequence(hsm, seq);
  while (not range_f(lower_bound, upper_bound, length));

  return length;
}

unsigned int generate_short_sequence(std::pair<unsigned int, unsigned int>* seq) {
  std::pair<unsigned int, unsigned int> p(0, 0);
  seq[0] = p;
  seq[1] = p;
  seq[2] = p;
  seq[3] = p;
  return 4;
}

unsigned int generate_floral_sequence(std::pair<unsigned int, unsigned int>* seq) { 
  std::pair<unsigned int, unsigned int> p(0,  0);
  std::pair<unsigned int, unsigned int> s(0, 12);
  
  seq[0] = p;
  seq[1] = p;
  seq[2] = p;
  seq[3] = p;

  return 4;
}

unsigned int generate_trunk(std::pair<unsigned int, unsigned int>* seq) { // The sequence of the
                                                                          // trunk is fixed
  const unsigned int max_length = 60;
  const unsigned int number     =  2;

  // two observed trunk sequences of length 60
  static const unsigned int trunk_sequences[number][max_length] = {
    {0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 3, 0, 3,  0, 0, 0, 0, 1,  0, 0, 1, 0, 4,  0, 0, 0, 0, 4,  0, 0, 0, 0, 0,  0, 4, 4, 0, 3,  0, 0, 0, 0, 9}, 
//     {0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 4,  0, 0, 1, 0, 1,  1, 0, 1, 1, 0,  2, 0, 0, 0, 0,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 4,  0, 1, 0, 0, 1,  1, 0, 1, 1, 0,  2, 0, 0, 0, 0,  9, 9, 9, 9, 9},
//     {0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0, 0, 0, 4,  0, 1, 0, 0, 1,  1, 0, 1, 1, 0,  2, 0, 0, 0, 0,  9, 9, 9, 9, 9,  9, 9, 9, 9, 9,  9, 9, 9, 9, 9,  9, 9, 9, 9, 9,  9, 9, 9, 9, 9}
  };

  unsigned int select_trunk = random(number);
  unsigned int i            = 0;

  for (; i < max_length; ++i) {
    if (trunk_sequences[select_trunk][i] == 9)
      break;
    seq[i].first  = 10;
    seq[i].second = trunk_sequences[select_trunk][i];
  }

  reverse_sequence(seq, i - 1);

  return i;
}

unsigned int generate_random_draw_sequence(std::pair<unsigned int, unsigned int>* seq) {
  const unsigned int max_length = 65;
  const unsigned int number     =  9;

  static const int second_year_branches[number][max_length] = { // an alternative to the long shoot
                                                                // model of the 2nd year. Usually
                                                                // not used.
    {0, 0, 0, 0, 0, 3, 2, 2, 1, 1,  0, 0, 0, 0, 2, 0, 1, 1, 4, 1,  4, 4, 4, 4, 4, 4, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 4, 0, 0, 4, 0, 4,  0, 0, 4, 0, 0, 0, 0, 0, 0, 0,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 3,  3, 0, 0, 0, 0, 0, 4, 4, 4, 4,  4, 3, 0, 4, 4, 4, 0, 4, 0, 4,  4, 0, 0, 4, 0, 0, 0, 2, 3, 0,  0, 0, 3, 3, 3, 3, 0, 0, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0, 0, 0, 3, 0, 3,  4, 0, 1, 4, 4, 1, 0, 4, 0, 1,  4, 4, 0, 4, 4, 4, 4, 4, 4, 0,  4, 4, 0, 0, 0, 1, 0, 4, 4, 4,  0, 4, 0, 4, 0, 0, 0, 3, 0, 1,  0, 0, 0, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0, 0, 0, 2, 2, 4,  1, 1, 4, 3, 1, 0, 0, 4, 0, 0,  4, 0, 0, 4, 0, 4, 4, 4, 4, 4,  4, 4, 4, 0, 0, 3, 0, 0, 0, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0, 0, 3, 2, 3, 0,  0, 3, 3, 0, 0, 0, 1, 2, 0, 1,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 4, 0, 4, 0, 0, 4,  0, 0, 0, 0, 0, 0, 9, 9, 9, 9,  9, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 4, 3, 2, 4, 4, 0,  2, 0, 3, 0, 2, 0, 0, 4, 0, 4,  4, 4, 4, 4, 0, 0, 0, 0, 0, 0,  0, 4, 0, 4, 4, 0, 0, 0, 0, 4,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 3, 0, 2, 3, 0, 0, 0, 3, 2,  0, 0, 9, 9, 9},
    {0, 0, 0, 0, 1, 4, 0, 4, 0, 3,  0, 0, 1, 3, 2, 0, 0, 0, 0, 0,  0, 0, 4, 0, 0, 0, 3, 0, 0, 1,  1, 0, 0, 3, 4, 0, 4, 0, 0, 4,  0, 4, 0, 0, 0, 0, 0, 1, 0, 3,  0, 1, 0, 0, 0, 0, 1, 9, 9, 9,  9, 9, 9, 9, 9},
    {0, 0, 0, 0, 0, 3, 0, 3, 3, 0,  3, 0, 0, 0, 0, 0, 0, 0, 3, 0,  1, 0, 0, 4, 0, 4, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 4, 0, 0, 1, 0, 0, 1, 1, 1,  1, 9, 9, 9, 9, 9, 9, 9, 9, 9,  9, 9, 9, 9, 9}
  };

  unsigned int select_branch = random(number);
  unsigned int i             = 0;

  for (; i < max_length; ++i) {
    if (second_year_branches[select_branch][i] == 9)
      break;
    seq[i].first  = 10;
    seq[i].second = second_year_branches[select_branch][i];
  }

  reverse_sequence(seq, i - 1);

  return i;
}

void destroy_hsm(Hidden_semi_markov* hsm) {
  delete hsm;
}
