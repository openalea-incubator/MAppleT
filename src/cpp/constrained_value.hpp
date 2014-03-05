#ifndef __CONSTRAINED_VALUE_HPP__
#define __CONSTRAINED_VALUE_HPP__

#include "constants.hpp"

// A class to constrain a POD type to a range.  Based on "Constrained
// Value Types Using Polices", Christopher Diggins, C/C++ User's
// Journal, December 2004.  This implementation includes some
// additional features and policies not found Diggin's implementation.

template <typename constraints_policy>
class constrained_value {
public:

  typedef constrained_value<constraints_policy> self;
  typedef typename constraints_policy::value    value;

  constrained_value() : m() {}

  constrained_value(const self& x) {
    constraints_policy::assign(x.get_value(), m);
  } 

  constrained_value(const value& x) {
    constraints_policy::assign(x, m);
  }

  value get_value() const {
    return m;
  }

  operator value() {
    return m;
  }

  self& operator=(const self& x) {
    constraints_policy::assign(x.get_value(), m);
    return *this;
  }

  self& operator=(const value& x) {
    constraints_policy::assign(x, m);
    return *this;
  }

  self& operator+=(const self& x) {
    constraints_policy::assign(m + x.get_value(), m);
    return *this;
  }

  self& operator+=(const value& x) {
    constraints_policy::assign(m + x, m); return *this;
  }

  self& operator-=(const self& x) {
    constraints_policy::assign(m - x.get_value(), m); return *this;
  }

  self& operator-=(const value& x) {
    constraints_policy::assign(m - x, m); return *this;
  }

  self& operator*=(const self& x) {
    constraints_policy::assign(m * x.get_value(), m); return *this;
  }

  self& operator*=(const value& x) {
    constraints_policy::assign(m * x, m); return *this;
  }

  self& operator/=(const self& x) {
    constraints_policy::assign(m / x.get_value(), m); return *this;
  }

  self& operator/=(const value& x) {
    constraints_policy::assign(m / x, m); return *this;
  }

private:
  value m;     
};          

// Policies on what to do when a constrained value is out of range
namespace cv_policies {
  struct throwing {
    template <typename T> 
    static void on_below(const T& rvalue, T& lvalue, const T& min, const T& max) {
      throw 0;
    }

    template <typename T>
    static void on_above(const T& rvalue, T& lvalue, const T& min, const T& max) {
      throw 0;
    }
  };

  struct saturating {
    template <typename T> 
    static void on_below(const T& rvalue, T& lvalue, const T& min, const T& max) {
      lvalue = min;
    }

    template <typename T> 
    static void on_above(const T& rvalue, T& lvalue, const T& min, const T& max) {
      lvalue = max;
    }
  };

  struct periodic {
    template <typename T> 
    static void on_below(const T& rvalue, T& lvalue, const T& min, const T& max) {
      const T range = max - min;
      lvalue = rvalue;
      while (lvalue < min) lvalue += range;
    }

    template <typename T> 
    static void on_above(const T& rvalue, T& lvalue, const T& min, const T& max) {
      const T range = max - min;
      lvalue = rvalue;
      while (lvalue >= max) lvalue -= range;
    }
  };
}

// Some commonly used constrained value types
namespace cv_definitions {
  template <int min, int max, typename invalid_range = cv_policies::saturating>
  struct ranged_int {
    typedef int value;
    static int get_min() {
      return min;
    }

    static int get_max() {
      return max;
    }

    static void assign(const value& rvalue, value& lvalue) {  
      if (rvalue < min)
	invalid_range::on_below(rvalue, lvalue, min, max);
      else if (rvalue > max)
	invalid_range::on_above(rvalue, lvalue, min, max);
      else
	lvalue = rvalue; 
    }
  };

  template <typename invalid_range = cv_policies::saturating>
  struct double_0_to_1 {
    typedef double value;
    static void assign(const value& rvalue, value& lvalue) {
      if (rvalue < 0.0)
	invalid_range::on_below(rvalue, lvalue, 0.0, 1.0);
      else if (rvalue > 1.0)
	invalid_range::on_above(rvalue, lvalue, 0.0, 1.0);
      else
	lvalue = rvalue; 
    }
  };

  template <typename invalid_range = cv_policies::periodic>
  struct double_0_to_360 {
    typedef double value;
    static void assign(const value& rvalue, value& lvalue) {
      if (rvalue < 1.0)
	invalid_range::on_below(rvalue, lvalue, 0.0, 360.0);
      else if (rvalue >= 360.0)
	invalid_range::on_above(rvalue, lvalue, 0.0, 360.0);
      else
	lvalue = rvalue; 
    }
  };

  template <typename invalid_range = cv_policies::periodic>
  struct double_1_to_365 {
    typedef double value;
    static void assign(const value& rvalue, value& lvalue) {
      if (rvalue < 1.0)
	invalid_range::on_below(rvalue, lvalue, 0.0, 365.0);
      else if (rvalue >= 365.0)
	invalid_range::on_above(rvalue, lvalue, 0.0, 365.0);
      else
	lvalue = rvalue; 
    }
  };

  template <typename invalid_range = cv_policies::periodic>
  struct double_0_to_2pi {
    typedef double value;
    static void assign(const value& rvalue, value& lvalue) {
      if (rvalue < 0.0)
	invalid_range::on_below(rvalue, lvalue, 0.0, constants::two_pi);
      else if (rvalue >= constants::two_pi)
	invalid_range::on_above(rvalue, lvalue, 0.0, constants::two_pi);
      else
	lvalue = rvalue;
    }
  };
}

// Short aliases for commonly used constrained value types
typedef constrained_value<cv_definitions::double_0_to_1  <> > d_0_1;
typedef constrained_value<cv_definitions::double_0_to_360<> > d_0_360;
typedef constrained_value<cv_definitions::double_1_to_365<> > d_1_365;
typedef constrained_value<cv_definitions::double_0_to_2pi<> > d_0_2pi;

#endif
