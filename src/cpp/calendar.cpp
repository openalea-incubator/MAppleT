#include <cassert>
#include "calendar.hpp"

int convert_to_day(int month, int day) {
  assert(month > 0 and  month <= 12);
  assert(day > 0);

  switch (month) {
  case  1: assert(day <= 31); return   0 + day - 1;
  case  2: assert(day <= 28); return  31 + day - 1;
  case  3: assert(day <= 31); return  59 + day - 1;
  case  4: assert(day <= 30); return  90 + day - 1;
  case  5: assert(day <= 31); return 120 + day - 1;
  case  6: assert(day <= 30); return 151 + day - 1;
  case  7: assert(day <= 31); return 181 + day - 1;
  case  8: assert(day <= 31); return 212 + day - 1;
  case  9: assert(day <= 30); return 243 + day - 1;
  case 10: assert(day <= 31); return 273 + day - 1;
  case 11: assert(day <= 30); return 304 + day - 1;
  case 12: assert(day <= 31); return 334 + day - 1;
  default: return -1;
  }
}

void day_and_month(unsigned int t, unsigned int& day, unsigned int& month) {
  while (t > 365) t -= 365;

       if (t > 334) {day = t - 334; month = 12;}
  else if (t > 304) {day = t - 304; month = 11;}
  else if (t > 273) {day = t - 273; month = 10;}
  else if (t > 243) {day = t - 243; month =  9;}
  else if (t > 212) {day = t - 212; month =  8;}
  else if (t > 181) {day = t - 181; month =  7;}
  else if (t > 151) {day = t - 151; month =  6;}
  else if (t > 120) {day = t - 120; month =  5;}
  else if (t >  90) {day = t - 90;  month =  4;}
  else if (t >  59) {day = t - 59;  month =  3;}
  else if (t >  31) {day = t - 31;  month =  2;}
  else if (t >   0) {day = t;       month =  1;}
}
