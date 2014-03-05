COMPILER = c++ -fpermissive  -O3 -Werror -Wall -pedantic



STATTOOL=/home/cokelaer/Work/virtualplants/trunk/vplants/stat_tool/build-scons
SEQUENCE=/home/cokelaer/Work/virtualplants/trunk/vplants/sequence_analysis/build-scons/
TOOL=/home/cokelaer/Work/virtualplants/trunk/vplants/tool/build-scons/
LIB=-L${TOOL}/lib -L${STATTOOL}/lib -L${SEQUENCE}/lib -lvpstat_tool -lvpsequence -lvptool
INCLUDE=-I${TOOL}/include -I${STATTOOL}/include -I${SEQUENCE}/include

calendar: array.hpp constrained_value.hpp
	@echo Compiling calendar
	g++ -o calendar.o -c calendar.cpp

test_quaternion: quaternion
	g++ test_quaternion.cc quaternion.o random.o sequences.o -lm ${LIB} ${INCLUDE}

test_sequences: sequences random
	g++ test_sequences.cc random.o sequences.o -lm ${LIB} ${INCLUDE}

test: calendar random quaternion physics ini 
	g++ test.cc calendar.o random.o quaternion.o sequences.o ini.o -lm ${LIB} ${INCLUDE}
	
ini: 
	@echo Compiling ini
	g++ -o ini.o -c ini.cpp

physics: 
	@echo Compiling physics
	$(COMPILER) -o physics.o -c physics.cpp

quaternion: 
	@echo Compiling quaternion
	g++ -o quaternion.o -c quaternion.cpp

random:  
	@echo Compiling random	
	g++ -o random.o -c random.cpp

sequences: 
	@echo Compiling sequences
	g++ -o sequences.o -c sequences.cpp ${INCLUDE}

all: calendar ini physics random sequences quaternion

clean:
	rm *.o *~ *.i *.dll *.log lsystem.bmp counts*.txt trunk*.dat mtg*.mtg lsys.exp
