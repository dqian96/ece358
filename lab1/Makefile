CXX = g++							# c++ compiler

CXXFLAGS = -g -Wall -MMD -std=c++11	# compiler flags
MAKEFILE_NAME = ${firstword ${MAKEFILE_LIST}}# makefile name


OBJECTS1 = utils.o main.o simulation.o queue.o
EXEC1 = main


OBJECTS = ${OBJECTS1}
DEPENDS = ${OBJECTS:.o=.d}
EXECS = ${EXEC1}

#############################################################

.PHONY : all clean

all : ${EXECS}				# build all executables

${EXEC1} : ${OBJECTS1}			# compile and link 1st executable
	${CXX} ${CXXFLAGS} $^ -o $@


run : ${EXEC1}
	./${EXEC1}


graph : run
	gnuplot -e "set terminal jpeg; set grid; set xlabel 'utilization'; set ylabel 'avg q size'; set title 'Average Q Size vs Utilization (MM1)'; set style data line; plot 'mm1AvgQueueSize.csv' u 1:2 w lp t 'MM1'" > mm1AvgQueueSize.jpeg
	gnuplot -e "set terminal jpeg; set grid; set xlabel 'utilization'; set ylabel 'proportion idle'; set title 'Proportion Idle vs Utilization (MM1)'; set style data line; plot 'mm1P1Idle.csv' u 1:2 w lp t 'MM1'" > mm1P1Idle.jpeg
	gnuplot -e "set terminal jpeg; set grid; set xlabel 'utilization'; set ylabel 'avg q size'; set title 'Avg Q Size vs Utilization (MM1K)'; set style data line; plot 'mm1KAvgQueueSize.csv' u 1:2 w lp t 'K=5', 'mm1KAvgQueueSize.csv' u 1:3 w lp t 'K=10', 'mm1KAvgQueueSize.csv' u 1:4 w lp t 'K=40', 'mm1KAvgQueueSize.csv' u 1:5 w lp t 'K=inf'" > mm1KAvgQueueSize.jpeg
	gnuplot -e "set terminal jpeg; set grid; set xlabel 'utilization'; set ylabel 'proportion loss'; set title 'Proportion Loss vs Utilization (MM1K)'; set style data line; plot 'mm1KPLoss.csv' u 1:2 w lp t 'K=5', 'mm1KPLoss.csv' u 1:3 w lp t 'K=10', 'mm1KPLoss.csv' u 1:4 w lp t 'K=40'" > mm1KPLoss.jpeg


#############################################################

-include ${DEPENDS}			# include *.d files containing program dependences

clean :					# remove files that can be regenerated
	rm -f *.d *.o *.csv *.jpeg ${EXECS}
