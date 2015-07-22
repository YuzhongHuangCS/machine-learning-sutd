CC			= g++
SRCS		= RandomForest.cpp
OBJS		= $(SRCS:.cpp=.o)
PROG		= $(SRCS:.cpp=.out)

SHARK_ROOT	= /home/hyz/Shark

CPPFLAGS	= -std=c++11 -Wall -fopenmp -march=native -O3 -DNDEBUG -DBOOST_UBLAS_NDEBUG
LDFLAGS		= -fopenmp
LDLIBS		= -lshark -lboost_serialization -lboost_system -lboost_filesystem -lboost_program_options

all: $(SRCS) $(PROG)

$(PROG): $(OBJS)
	$(CC) $(CPPFLAGS) $(OBJS) -o $@ $(LDFLAGS) $(LDLIBS)

.cpp.o:
	$(CC) $(CPPFLAGS) $< -c -o $@

clean:
	rm $(OBJS) $(PROG)
