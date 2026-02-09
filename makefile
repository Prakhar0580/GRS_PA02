# Compiler and Flags
CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lpthread -lm

# Part A Executables
SERVER_A = ServerA
CLIENT_A = ClientA

# Part B Executables
SERVER_B = ServerB
CLIENT_B = ClientB

# Source Files
SRC_SERVER_A = MT25005_PartA_Server.c
SRC_CLIENT_A = MT25005_PartA_Client.c
SRC_SERVER_B = MT25005_PartB_Server.c
SRC_CLIENT_B = MT25005_PartB_Client.c
BASH_SCRIPT = MT25005_PartC_bash.sh

# Default Target: Compile all parts
all: partA partB permissions

# Compile Part A
partA: $(SRC_SERVER_A) $(SRC_CLIENT_A)
	$(CC) $(CFLAGS) $(SRC_SERVER_A) -o $(SERVER_A) $(LDFLAGS)
	$(CC) $(CFLAGS) $(SRC_CLIENT_A) -o $(CLIENT_A) $(LDFLAGS)

# Compile Part B
partB: $(SRC_SERVER_B) $(SRC_CLIENT_B)
	$(CC) $(CFLAGS) $(SRC_SERVER_B) -o $(SERVER_B) $(LDFLAGS)
	$(CC) $(CFLAGS) $(SRC_CLIENT_B) -o $(CLIENT_B) $(LDFLAGS)

# Ensure the Bash script is executable
permissions:
	chmod +x $(BASH_SCRIPT)

# Clean up all binaries, results, and temp files
clean:
	rm -f $(SERVER_A) $(CLIENT_A) $(SERVER_B) $(CLIENT_B) perf_tmp.txt *.csv
	@echo "Cleanup complete."

# Run the Part C automation (requires sudo for namespaces/perf)
run_tests:
	sudo ./$(BASH_SCRIPT)