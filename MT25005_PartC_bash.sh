#!/bin/bash

# 1. Compile the Server and Client
echo "Step 1: Compiling files..."
gcc MT25005_PartB_Server.c -o ServerB -lpthread -lm
gcc MT25005_PartB_Client.c -o ClientB -lm

# Initialize CSV for results
CSV_FILE="MT25005_PartC_bash.csv"

# --- FORMATTING IMPROVEMENT: Fixed width header ---
printf "%-10s %-10s %-10s %-15s %-15s %-15s\n" \
       "Mode" "Threads" "Size" "Cycles" "CacheMiss" "CtxSwitch" > $CSV_FILE

# Test Configuration
SIZES=(1024 4096 16384 65536)
THREADS=(1 2 3 4)
MODE=3 
DURATION=10 

for size in "${SIZES[@]}"; do
    for thread_count in "${THREADS[@]}"; do
        echo "------------------------------------------------"
        echo "Starting Test: Mode $MODE, Threads $thread_count, Size $size"

        # 2. Start Server and Perf
        sudo env LC_ALL=C perf stat \
            -e cycles,cache-misses,context-switches \
            -x, \
            sudo ip netns exec ns_server ./ServerB $MODE \
            2> perf_tmp.txt &
        
        PERF_PID=$!
        sleep 2 
        
        # 3. Launch Clients
        for ((i=1; i<=thread_count; i++)); do
            sudo ip netns exec ns_client ./ClientB $size $DURATION &
        done

        sleep $((DURATION + 2))

        # 4. Stop Session
        sudo kill -INT $PERF_PID
        wait $PERF_PID 2>/dev/null

        # 5. Extract results
        cycles=$(awk -F',' '$3=="cycles" {print $1}' perf_tmp.txt)
        misses=$(awk -F',' '$3=="cache-misses" {print $1}' perf_tmp.txt)
        switches=$(awk -F',' '$3=="context-switches" {print $1}' perf_tmp.txt)

        # Handle empty values
        cycles=${cycles:-0}
        misses=${misses:-0}
        switches=${switches:-0}
        
        # --- FORMATTING IMPROVEMENT: Fixed width data rows ---
        printf "%-10s %-10s %-10s %-15s %-15s %-15s\n" \
               "$MODE" "$thread_count" "$size" "$cycles" "$misses" "$switches" >> $CSV_FILE
        
        rm -f perf_tmp.txt
        echo "Run Complete."
    done
done

echo "Workflow complete. Results saved to $CSV_FILE"