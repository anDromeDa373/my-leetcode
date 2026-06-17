CC      = cc
CFLAGS  = -Wall -Wextra -std=c11 -O2
TARGET  = ../lct
SRC     = main.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)
