CC			= g++
CFLAGS		= -std=c++11 -Wall -O2 -march=native
LINKFLAGS	= 
SRCS		= main.cpp
OBJS		= $(SRCS:.cpp=.o)
PROG		= main.out

all: $(SRCS) $(PROG)

$(PROG): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@ $(INCFLAGS) $(LINKFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) $< -c -o $@ $(INCFLAGS)

depend:
	makedepend $(INCFLAGS) -Y $(SRCS)

clean:
	rm $(OBJS) $(PROG)
