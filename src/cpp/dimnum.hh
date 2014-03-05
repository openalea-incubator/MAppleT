/*
  $Id: dimnum.hh,v 1.16 2006/04/10 07:56:30 kp229 Exp $

  Template library for dimension-full numbers in C++.
  Copyright (C) 2001  Kasper Peeters <k.peeters@damtp.cam.ac.uk>

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; version 2.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

*/

// Slightly modified by Colin (look for CTS)
// May be replace by the library QUAN: quan.sourceforge.net

#ifndef dimensions_hh__
#define dimensions_hh__

#include <string>
#include <map>
#include <iostream>
#include <stdexcept>
#include <cmath>
#include <cassert>
#include <cstdlib>

#ifdef _MSC_VER
#pragma warning(disable:4189)

typedef unsigned __int64 dn_ulong;
typedef __int64          dn_long;
#else
typedef uint64_t dn_ulong;
typedef int64_t  dn_long;
#endif

// Conversion uses num/den*10^pw + off.

template<dn_ulong num, dn_ulong den, int pw=0, dn_ulong off=0>
class conversion {
public:
  static const dn_ulong n=num;
  static const dn_ulong d=den;
  static const int  p=pw;
  static const dn_ulong offset=off;  // eg. for conversion kelvin->celcius (not yet implemented)
};

template<int length, int mass, int time, int current, int temperature, int amount, int intensity>
class powers {
public:
  static const int d1=length;
  static const int d2=mass;
  static const int d3=time;
  static const int d4=current;
  static const int d5=temperature;
  static const int d6=amount;
  static const int d7=intensity;
};

// for default conversion factors; this is a 'dim without value'.
template<int length, int mass, int time, int current, int temperature, int amount, int intensity, class base>
class cfactor : public powers<length,mass,time,current,temperature,amount,intensity>, public base {};

// the value class. The 'base' class can be another 'dim' or a 'cfactor'.
template<int length, int mass, int time, int current, int temperature, int amount, int intensity, class base=cfactor<length,mass,time,current,temperature,amount,intensity,conversion<1,1> > >
class dim : public powers<length,mass,time,current,temperature,amount,intensity>,
            public conversion<base::n, base::d, base::p> {
public:
  dim() : value(0) {};
  dim(double val) : value(val) {};
  ~dim() 
  {
    // Compile-time check that the base class has the same dimensions.
    //  Assignment to a dummy variable so that it passes on g++ with high-warning levels.
    powers<length,mass,time,current,temperature,amount,intensity> const *x =
      static_cast<powers<length,mass,time,current,temperature,amount,intensity> const *>(static_cast<base const *>(0));
    // CTS - a little hack to both get a clean compile and force a runtime check
    assert(x == 0);
  }

  double value;
};

class set7 {
public:
  set7() :
    d1(0), d2(0), d3(0), d4(0), d5(0), d6(0), d7(0), n(0), d(0), p(0) {}
  set7(int d1, int d2, int d3, int d4, int d5, int d6, int d7, dn_ulong n, dn_ulong d, int p) :
    d1(d1), d2(d2), d3(d3), d4(d4), d5(d5), d6(d6), d7(d7), n(n), d(d), p(p) {}
  int d1,d2,d3,d4,d5,d6,d7;
  dn_ulong n;
  dn_ulong d;
  int  p;
};

static std::map<std::string, set7> s2d;

// Conversion macros from one base to another (see also one more in the operator>>).
#define dn_convert(bto,bfrom,val)				\
  double((val*pow(10.0,bfrom::p-bto::p)				\
		    *(((bfrom::n)*bto::d)/	\
		      ((bfrom::d)*bto::n))))

#define dn_tosi(val,b)						\
  double((val*b::n*pow(10.0,b::p)/(b::d)))

template<int m, int l, int s, int c, int t, int a, int i, class base1>
dim<m,l,s,c,t,a,i,base1> operator*(const double& val, const dim<m,l,s,c,t,a,i,base1>& aa) 
{
  return dim<m,l,s,c,t,a,i,base1>(val*aa.value);
}

template<int m, int l, int s, int c, int t, int a, int i, class base1>
dim<m,l,s,c,t,a,i,base1> operator*(const int& val, const dim<m,l,s,c,t,a,i,base1>& aa) 
{
  return dim<m,l,s,c,t,a,i,base1>(val*aa.value);
}

template<class base1, class base2,
	 int l, int m, int s, int c, int t, int a, int i>
dim<m,l,s,c,t,a,i,base1> operator+(const dim<m,l,s,c,t,a,i,base1>& aa, 
					const dim<m,l,s,c,t,a,i,base2>& bb) 
{
  return dim<m,l,s,c,t,a,i,base1>(aa.value + dn_convert(base1,base2,bb.value));
}

template<class base1, class base2,
	 int l, int m, int s, int c, int t, int a, int i>
dim<m,l,s,c,t,a,i,base1> operator-(const dim<m,l,s,c,t,a,i,base1>& aa, 
					const dim<m,l,s,c,t,a,i,base2>& bb) 
{
  return dim<m,l,s,c,t,a,i,base1>(aa.value - dn_convert(base1,base2,bb.value));
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator<(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value < dn_convert( base1, base2, bb.value);
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator>(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value > dn_convert( base1, base2, bb.value);
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator<=(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value <= dn_convert( base1, base2, bb.value);
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator>=(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value >= dn_convert( base1, base2, bb.value);
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator==(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value == dn_convert( base1, base2, bb.value);
}

template< class base1, class base2, int l, int m, int s, int c, int t, int a, int i>
bool operator!=(const dim<m,l,s,c,t,a,i,base1>& aa, const dim<m,l,s,c,t,a,i,base2>& bb) {
  return aa.value != dn_convert( base1, base2, bb.value);
}

template< class base1, int l1, int m1, int s1, int c1, int t1, int a1, int i1,
	  class base2, int l2, int m2, int s2, int c2, int t2, int a2, int i2>
dim<l1+l2,m1+m2,s1+s2,c1+c2,t1+t2,a1+a2,i1+i2> 
operator*(const dim<l1,m1,s1,c1,t1,a1,i1,base1>& aa,
	  const dim<l2,m2,s2,c2,t2,a2,i2,base2>& bb)
{
  return dim<l1+l2, m1+m2, s1+s2, c1+c2, t1+t2, a1+a2, i1+i2>(
								   dn_tosi(aa.value,base1)*dn_tosi(bb.value,base2) );
}

template< class base1, int l1, int m1, int s1, int c1, int t1, int a1, int i1,
	  class base2, int l2, int m2, int s2, int c2, int t2, int a2, int i2>
dim<l1-l2,m1-m2,s1-s2,c1-c2,t1-t2,a1-a2,i1-i2> 
operator/(const dim<l1,m1,s1,c1,t1,a1,i1,base1>& aa,
	  const dim<l2,m2,s2,c2,t2,a2,i2,base2>& bb)
{
  return dim<l1-l2, m1-m2, s1-s2, c1-c2, t1-t2, a1-a2, i1-i2>(
								   dn_tosi(aa.value,base1)/dn_tosi(bb.value,base2) );
}

// partial specialisation for conversion factors without name
template<int l, int m, int s, int c, int t, int a, int i, dn_ulong nn, dn_ulong dd, int pw>
std::ostream& operator<<(std::ostream& str, const dim<l,m,s,c,t,a,i,cfactor<l,m,s,c,t,a,i,conversion<nn,dd,pw> > >& val) 
{
  //  str << "non-named: ";
  str << val.value;
  if(m!=0) {
    str << " kg";
    if(m!=1)
      str << "^" << m;
  }
  if(l!=0) {
    str << " m";
    if(l!=1)
      str << "^" << l;
  }
  if(s!=0) {
    str << " s";
    if(s!=1)
      str << "^" << s;
  }
  if(c!=0) {
    str << " A";
    if(c!=1)
      str << "^" << c;
  }
  if(t!=0) {
    str << " K";
    if(t!=1)
      str << "^" << t;
  }
  if(a!=0) {
    str << " mol";
    if(a!=1)
      str << "^" << a;
  }
  if(i!=0) {
    str << " cd";
    if(i!=1)
      str << "^" << i;
  }
  return str;
}

template<int l, int m, int s, int c, int t, int a, int i, class base>
std::ostream& operator<<(std::ostream& str, const dim<l,m,s,c,t,a,i,base>& val)
{
  str << val.value << " " << base::abbr();
  return str;
}

template< int l, int m, int s, int c, int t, int a, int i, class base>
std::istream& operator>>(std::istream& str, dim<l,m,s,c,t,a,i,base>& val)
{
  double tmp;
  str >> tmp;
  set7 acdim(0,0,0,0,0,0,0,1,1,0);
  std::string nm;
  while(str>>nm) {
    if(atof(nm.c_str())!=0) // FIXME: we have to scan single characters
      break;
    std::map<std::string, set7>::iterator fnd=s2d.find(nm);
    if(!(fnd==s2d.end())) {
      acdim.d1+=(*fnd).second.d1;
      acdim.d2+=(*fnd).second.d2;
      acdim.d3+=(*fnd).second.d3;
      acdim.d4+=(*fnd).second.d4;
      acdim.d5+=(*fnd).second.d5;
      acdim.d6+=(*fnd).second.d6;
      acdim.d7+=(*fnd).second.d7;
      acdim.n*=(*fnd).second.n;
      acdim.d*=(*fnd).second.d;
      acdim.p =(*fnd).second.p;
    }
    else throw std::logic_error("unknown unit encountered");
  }
  if(acdim.d1!=l) throw std::logic_error("length dimension does not match");
  if(acdim.d2!=m) throw std::logic_error("mass dimension does not match");
  if(acdim.d3!=s) throw std::logic_error("time dimension does not match");
  if(acdim.d4!=c) throw std::logic_error("current dimension does not match");
  if(acdim.d5!=t) throw std::logic_error("temperature dimension does not match");
  if(acdim.d6!=a) throw std::logic_error("amount_of_substance dimension does not match");
  if(acdim.d7!=i) throw std::logic_error("luminous_intensity dimension does not match");

  val.value=tmp;
  val.value*=double(pow(10.0,acdim.p-base::p)*base::d)/double(base::n)*double(acdim.n)/acdim.d;
  return str;
}

// Declare classes in the 'unit::' namespace, ie. those which are used
// in the 'base' parameter of the dimensionful number classes, as well
// as one const instance of this class in the 'syst::' namespace.
//
// declare(syst,tt,name,nn,dd,txt) leads to the declaration of
//
//    class unit::name;                       (and a helper unit::name_)
//    const class unit::name syst::name       (explicit instance)

#define declare_(syst,tt,name,nn,dd,pw,txt)				\
  namespace unit {							\
      class name ## _ : public cfactor<dimension::tt::d1,dimension::tt::d2,dimension::tt::d3, dimension::tt::d4,dimension::tt::d5,dimension::tt::d6, dimension::tt::d7, conversion<nn, dd, pw> > { \
	  name ## _() {							\
	  }								\
      };								\
      class name : public dim<dimension::tt::d1,dimension::tt::d2,dimension::tt::d3, dimension::tt::d4,dimension::tt::d5,dimension::tt::d6, dimension::tt::d7, name ## _ > { \
      public:								\
	  name() {							\
	    this->value=1;						\
	    s2d[txt]=set7(dimension::tt::d1,dimension::tt::d2,dimension::tt::d3,dimension::tt::d4,dimension::tt::d5,dimension::tt::d6,dimension::tt::d7,nn,dd,pw); \
	  }								\
	  static const char* abbr() {						\
	    return txt;							\
	  }								\
      };								\
  }									\


// #ifndef DIMNUM_MAKE_LIBRARY
#define declare(syst,tt,name,nn,dd,pw,txt)     \
  declare_(syst,tt,name,nn,dd,pw,txt)	       \
  namespace syst {			       \
      const unit::name name;		       \
  }					       \

#define default(syst,tt,name,nn,dd,pw,txt)				\
  declare(syst,tt,name,nn,dd,pw,txt)					\
  namespace syst {							\
      template<class base1=unit::name>					\
      class tt : public dim< dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base1> { \
      public:								\
	  tt() {}							\
	  tt(double val) { this->value=val; }				\
	  tt(const dim< dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base1>& val) { \
	    this->value=val.value;					\
	  }								\
	  template<class base2>						\
	  tt(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	    this->value=dn_convert(base1,base2,val.value);		\
	  }								\
	  template<class base2>						\
	  tt& operator+=(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	    this->value+=dn_convert(base1,base2,val.value);		\
	    return *this;						\
	  }								\
	  template<class base2>						\
	  tt& operator-=(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	    this->value-=dn_convert(base1,base2,val.value);		\
	    return *this;						\
	  }								\
      };								\
  }									\

// Define a templated class corresponding to a dimensionful number, in the
// dn:: namespace. Ie. dn::length< class base>.

#define stddeclare(tt)							\
  namespace dn {							\
    template< class base1>					\
    class tt : public dim< dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base1> {	\
    public:								\
      tt() {}								\
      tt(double val) {this->value = val;}					\
      tt(const dim< dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base1>& val) { \
	this->value=val.value;						\
      }									\
      template<class base2>					\
      tt(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	this->value=dn_convert(base1,base2,val.value);		\
      }									\
      template<class base2>					\
      tt& operator+=(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	this->value+=dn_convert(base1,base2,val.value);		\
      }									\
      template<class base2>					\
      tt& operator-=(const dim<dimension::tt::d1, dimension::tt::d2, dimension::tt::d3, dimension::tt::d4, dimension::tt::d5, dimension::tt::d6, dimension::tt::d7, base2>& val) { \
	this->value-=dn_convert(base1,base2,val.value);		\
      }									\
    };									\
  }

namespace dimension {
  // take from SIunits/dims.dat.
  typedef powers<0,0,0,0,0,0,0>   dimensionless;
  typedef powers<1,0,0,0,0,0,0>   length;
  typedef powers<0,1,0,0,0,0,0>   mass;
  typedef powers<0,0,1,0,0,0,0>   time;
  typedef powers<0,0,0,1,0,0,0>   current;
  typedef powers<0,0,0,0,1,0,0>   temperature;
  typedef powers<0,0,0,0,0,1,0>   amount_of_substance;
  typedef powers<0,0,0,0,0,0,1>   luminous_intensity;

  typedef powers<-1,0,0,0,0,0,0>  inverse_length;
  typedef powers<0,0,-1,0,0,0,0>  inverse_time;
  typedef powers<1,0,-1,0,0,0,0>  velocity;
  typedef powers<2,0,0,0,0,0,0>   area;
  typedef powers<1,0,-2,0,0,0,0>  acceleration;

  typedef powers<2,1,-2,0, 0,0,0> energy;
  typedef powers<2,1,-2,0,-1,0,0> entropy;
}

stddeclare(length)
stddeclare(mass)
stddeclare(time)
stddeclare(current)
stddeclare(temperature)
stddeclare(amount_of_substance)
stddeclare(luminous_intensity)

#endif
