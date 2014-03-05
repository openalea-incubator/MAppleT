#ifndef __CALENDAR_HPP__
#define __CALENDAR_HPP__

#include "array.hpp"
#include "constrained_value.hpp"

// A convenience function to transform a day in a particular month to
// a day in in the year
int convert_to_day(int month, int day);

// A convenience function to transform a day in the year to the
// corresponding day and month
void day_and_month(unsigned int t, unsigned int& day, unsigned int& month);

// A container for information in each day of the year.
template <typename daily_data, unsigned int year_length = 365>
class calendar : public array<daily_data, year_length> {
public:
  calendar() :
    array<daily_data, year_length>(),
    current_year(0),
    current_time(0.0),
    increment(1.0)
  {}

private:
  struct double_0_to_yl {
    typedef double value;
    static void assign(const value& rvalue, value& lvalue) {
      if (rvalue < 0.0)
        cv_policies::periodic::on_below(rvalue, lvalue, 0.0, double(year_length));
      else if (rvalue >= double(year_length))
        cv_policies::periodic::on_above(rvalue, lvalue, 0.0, double(year_length));
      else
        lvalue = rvalue; 
    }
  };

public:
  // The time (in days) out of the year in the periodic range [0.0,
  // year_length) (i.e. for a year of 365 days, day 364.9 + 0.1 ==
  // 0.0).
  typedef constrained_value<double_0_to_yl> year_fraction;

  unsigned int  current_year;
  year_fraction current_time;
  year_fraction increment;

  unsigned int year() const {
    return current_year;
  }

  void advance() {
    year_fraction old_time = current_time;
    current_time += increment;
    if (current_time < old_time) current_year++;
  }

  const daily_data& current_data() {
    return array<daily_data, year_length>::operator[]((unsigned int)current_time);
  }

  unsigned int length() const {
    return year_length;
  }

  void reset_time() {
    current_year = 0;
    current_time = 0.0;
  }
};

#endif
