#include "calendar.hpp"
#include <stdio.h>
#include "v3.hpp"
#include "quaternion.hpp"
#include "random.hpp"
#include "physics.hpp"
#include "sequences.hpp"
#include "constants.hpp"
#include <assert.h>

#include "stat_tool/stat_tools.h"
#include "stat_tool/markovian.h"
#include "stat_tool/curves.h"
#include "sequence_analysis/sequences.h"
#include "sequence_analysis/sequence_label.h"
#include "sequence_analysis/semi_markov.h"
#include "sequence_analysis/hidden_semi_markov.h"
#include "sequence_analysis/variable_order_markov.h"
#include "sequence_analysis/hidden_variable_order_markov.h"



using namespace std;

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


int main()
{
    cout << "------------------- test convert to day"<<endl;
    cout << "convert_to_day(11,1)"<<convert_to_day(11, 1)<<endl;
    cout << "convert_to_day(4,15)"<<convert_to_day(4, 15)<<endl;
    cout << "convert_to_day(5,15)"<<convert_to_day(5, 15)<<endl;
    cout << "convert_to_day(10,29)"<<convert_to_day(10, 29)<<endl;
    cout << "convert_to_day(10,30)"<<convert_to_day(10, 30)<<endl;
    cout << "convert_to_day(11,1)"<<convert_to_day(11, 1)<<endl;
    cout << "convert_to_day(11,15)"<<convert_to_day(11, 15)<<endl;
    cout << "convert_to_day(12,15)"<<convert_to_day(12, 15)<<endl;
    

    cout << "-------------------- test month_to_day"<<endl;
    calendar<daily_data> cal;

    cal.reset_time();
    cal.current_year = 1994;

    cout << "Current year="<<cal.year()<<endl;
    cal.reset_time();
    cout << "Current year=" << cal.year()<<endl;
    cal.current_year = 1994;
    
    cal.increment = 1;

    cout << "increment=" <<cal.increment <<endl;;
    cal.advance();
    cal.advance();
    cal.advance();

    assert(cal.current_time ==3);
    cout << "current time1="<<cal.current_time<<endl;
    cal.current_time = 364;
    cout << "current time2="<<cal.current_time<<endl;
    cal.advance();
    assert(cal.current_time ==0);
    assert(cal.current_year ==1995);

    cout << "current time3="<<cal.current_time<<endl;
    cal.current_time = 364.9;
    cal.increment = 0.1;
    cout << "current time4="<<cal.current_time<<endl;
    cal.advance();
    cout << "current time5="<<cal.current_time<<endl;
    cout << "current year="<<cal.current_year<<endl;
    assert(cal.current_year==1996);


    unsigned int day;
    unsigned int month;
    cal.current_time = 300;
    day_and_month((unsigned int)cal.current_time, day, month);
    cout << day <<" " <<month<<endl;
    cal.current_time = 31;
    day_and_month((unsigned int)cal.current_time, day, month);
    cout << day <<" " <<month<<endl;
    cal.current_time = 31+28;
    day_and_month((unsigned int)cal.current_time, day, month);
    cout << day <<" " <<month<<endl;
    cal.current_time = 31+28+31;
    day_and_month((unsigned int)cal.current_time, day, month);
    cout << day <<" " <<month<<endl;

    cout << "-------------------- test v3d"<<endl;
    v3d v1(1.0, 0, 0);
    v3d v2(0, 1.0, 0);
    v3d v3(0, 0, 1);
    v3d v4(4, 5, -1.);
    
    cout << v1+v2+v3<<endl;
    cout << v1*v2<<endl;
    cout << v1*4.<<endl;
    cout << v4 % v1<<endl;
    v3d v5(1, 2, 3);
    cout << "-- norm and normsqured of v5(1,2,3)"<<endl; 
    cout << v5<<endl;
    cout << v5.length()<<endl;
    cout << v5.length_sq()<<endl;
    cout << "-- compute distance from v5 to v1"<<endl; 
    cout << v5.distance(v3)<<endl;
    

    cout << "-------------------- random generator"<<endl;
    seed_random_number_generator(1);
    for (int i=0; i<10; i++){cout << random(-0.3, 0.3) <<endl;}
    seed_random_number_generator(5);
    for (int i=0; i<10; i++){
        cout << i*0.1 <<" "<<boolean_event(i*0.1) <<endl;
        }
    cout << "random(2)="<<random((int unsigned)2)<<endl;
    cout << "random(2)="<<random((int unsigned)2)<<endl;
    cout << "random(2)="<<random((int unsigned)2)<<endl;
    cout << "random(2)="<<random((int unsigned)2)<<endl;
    cout << "-------------------- quaternion funcitonal"<<endl;
    v3d h(1,0,0); h.normalise();
    v3d l(0,1,0); l.normalise();
    v3d rotation_velocity(0.4, 0.5, 0.6);
    double vl = rotation_velocity.length();
    double length = 2.;
    axis_angle aa(rotation_velocity / vl, vl * length);
    cout << "before rotation before normalisation"<<endl;
    cout <<h<<endl;
    cout <<l<<endl;
    cout <<rotation_velocity<<endl;
    cout <<rotation_velocity/vl<<endl;
    cout << "vl="<<vl<< endl;
    cout << "aa.axis="<<aa.axis <<endl;
    cout << "aa.angle="<<aa.angle <<endl;

    h = rotate(h, aa);
    l = rotate(l, aa);
    cout << "after rotation before normalisation"<<endl;
    cout <<h<<endl;
    cout <<l<<endl;
    cout << "after rotation and normalisation"<<endl;

    h.normalise();
    l.normalise();

    cout <<h<<endl;
    cout <<l<<endl;
  
    cout << " ----------------------------- axis angle "<<endl;
    h = v3d(1,0,0);
    axis_angle aaa(h, 90.);
    cout << "aaa.axis="<<aaa.axis <<endl;
    cout << "aaa.angle="<<aaa.angle <<endl;
    cout << axis_angle_to_quaternion(aaa) <<endl;
   
    cout << "quaternion algebra"<<endl; 
    quaternion q1(1, 1, 0, 0);
    quaternion q2(1, 0, 1, 0);
    cout << q1*q2<<endl;
    cout << -q2<<endl;
    cout << q1*h<<endl;

    cout <<"--------------------------- physics"<<endl;
    cout << " NEED to FIND A WAY TO COMPILE WITHOUT SEG FAULT WHEN INCLUDING PHYSICS.O"<<endl;   


    std::string error_message;

    Hidden_semi_markov * hsm=hsm_init("fmodel_fuji_5_15_y3_96.txt", error_message);
    if (not hsm) {
       cout << error_message.c_str() <<endl;
    }
    cout << hsm <<endl;
  
}
