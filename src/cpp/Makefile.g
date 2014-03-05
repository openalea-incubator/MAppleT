COMPILER = g++
FLAGS    = -O3 -Werror -Wall -pedantic

lsys.dll: lsys.o calendar.o ini.o physics.o quaternion.o random.o sequences.o
	@echo Creating lsys.dll ...
	$(COMPILER) $(FLAGS) -shared \
	calendar.o ini.o lsys.o physics.o quaternion.o random.o sequences.o \
	-L$(VPSTAT)/lib -lstatistics -lrw  \
	-o lsys.dll

calendar.o: calendar.cpp calendar.hpp array.hpp constrained_value.hpp Makefile
	@echo Compiling calendar
	$(COMPILER) $(FLAGS) -c calendar.cpp

ini.o: ini.cpp ini.hpp Makefile
	@echo Compiling ini
	$(COMPILER) $(FLAGS) -c ini.cpp

lsys.o: lsys.i Makefile
	@echo Compiling lsys
	$(COMPILER) $(FLAGS) -I$(VPSTAT) -c lsys.i -o lsys.o

physics.o: physics.cpp physics.hpp quaternion.hpp units.hpp v3.hpp Makefile
	@echo Compiling physics
	$(COMPILER) $(FLAGS) -c physics.cpp

quaternion.o: quaternion.cpp quaternion.hpp constrained_value.hpp range.hpp v3.hpp Makefile
	@echo Compiling quaternion
	$(COMPILER) $(FLAGS) -c quaternion.cpp

random.o: random.cpp random.hpp range.hpp Makefile
	@echo Compiling random
	$(COMPILER) $(FLAGS) -c random.cpp

sequences.o: sequences.cpp sequences.hpp range.hpp Makefile
	@echo Compiling sequences
	$(COMPILER) $(FLAGS) -I$(VPSTAT) -c sequences.cpp

clean:
	del *.o *~ *.i *.dll *.log lsystem.bmp counts*.txt trunk*.dat mtg*.mtg lsys.exp
