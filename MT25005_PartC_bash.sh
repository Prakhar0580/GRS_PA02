# #!/bin/bash

# # 1. Compile the Server and Client
# echo "Step 1: Compiling files..."
# gcc MT25005_PartB_Server.c -o ServerB -lpthread -lm
# gcc MT25005_PartB_Client.c -o ClientB -lm

# # Initialize CSV for results
# CSV_FILE="MT25005_PartC_bash.csv"

# # --- FORMATTING IMPROVEMENT: Fixed width header ---
# printf "%-10s %-10s %-10s %-15s %-15s %-15s\n" \
#        "Mode" "Threads" "Size" "Cycles" "CacheMiss" "CtxSwitch" > $CSV_FILE

# # Test Configuration
# SIZES=(1024 4096 16384 65536)
# THREADS=(1 2 3 4)
# MODE=3 
# DURATION=10 

# for size in "${SIZES[@]}"; do
#     for thread_count in "${THREADS[@]}"; do
#         echo "------------------------------------------------"
#         echo "Starting Test: Mode $MODE, Threads $thread_count, Size $size"

#         # 2. Start Server and Perf
#         sudo env LC_ALL=C perf stat \
#             -e cycles,cache-misses,context-switches \
#             -x, \
#             sudo ip netns exec ns_server ./ServerB $MODE \
#             2> perf_tmp.txt &
        
#         PERF_PID=$!
#         sleep 2 
        
#         # 3. Launch Clients
#         for ((i=1; i<=thread_count; i++)); do
#             sudo ip netns exec ns_client ./ClientB $size $DURATION &
#         done

#         sleep $((DURATION + 2))

#         # 4. Stop Session
#         sudo kill -INT $PERF_PID
#         wait $PERF_PID 2>/dev/null

#         # 5. Extract results
#         cycles=$(awk -F',' '$3=="cycles" {print $1}' perf_tmp.txt)
#         misses=$(awk -F',' '$3=="cache-misses" {print $1}' perf_tmp.txt)
#         switches=$(awk -F',' '$3=="context-switches" {print $1}' perf_tmp.txt)

#         # Handle empty values
#         cycles=${cycles:-0}
#         misses=${misses:-0}
#         switches=${switches:-0}
        
#         # --- FORMATTING IMPROVEMENT: Fixed width data rows ---
#         printf "%-10s %-10s %-10s %-15s %-15s %-15s\n" \
#                "$MODE" "$thread_count" "$size" "$cycles" "$misses" "$switches" >> $CSV_FILE
        
#         rm -f perf_tmp.txt
#         echo "Run Complete."
#     done
# done

# echo "Workflow complete. Results saved to $CSV_FILE"

# ------------------------------------------------------------

#!/bin/bash

#!/bin/bash

#CSV_FILE="MT25005_PartC_Results.csv"
SIZES=(1024 4096 16384 65536)
THREADS=(1 2 3 4)
MODES=(1 2 3) 
DURATION=10
#!/bin/bash

CSV_FILE="MT25005_PartC_Results.csv"
SIZES=(1024 4096 16384 65536)
THREADS=(1 2 3 4)
MODES=(1 2 3) # 1: 2-Copy, 2: 1-Copy, 3: Zero-Copy
DURATION=10

# Compile
gcc MT25005_PartB_Server.c -o ServerB -lpthread
gcc MT25005_PartB_Client.c -o ClientB

# CSV Header
echo "Mode,ThreadCount,MsgSize,Throughput_Gbps,Latency_us,CPUCycles,L1_Misses,LLC_Misses,CtxSwitches" > $CSV_FILE

for mode in "${MODES[@]}"; do
    for size in "${SIZES[@]}"; do
        for threads in "${THREADS[@]}"; do
            echo "Testing: Mode $mode, Size $size, Threads $threads"

            # Start Server with Perf in background
            sudo ip netns exec ns_server perf stat \
                -e cycles,L1-dcache-load-misses,LLC-load-misses,context-switches \
                -x, -o perf_data.tmp \
                sudo ./ServerB $mode &
            SERVER_PID=$!
            sleep 2

            # Run Clients and capture application metrics
            for ((i=1; i<=threads; i++)); do
                sudo ip netns exec ns_client ./ClientB $size $DURATION > "client_$i.tmp" &
            done
            
            sleep $((DURATION + 2))

            # Kill Server and Perf
            sudo pkill -INT perf
            sudo pkill -9 ServerB
            wait $SERVER_PID 2>/dev/null

            # Aggregate App Metrics (Sum Throughput, Avg Latency)
            total_thr=$(awk -F',' '{sum+=$1} END {print sum}' client_*.tmp)
            avg_lat=$(awk -F',' '{sum+=$2} END {print sum/NR}' client_*.tmp)

            # Extract Hardware Metrics
            cycles=$(awk -F',' '/cycles/ {print $1}' perf_data.tmp)
            l1_miss=$(awk -F',' '/L1-dcache-load-misses/ {print $1}' perf_data.tmp)
            llc_miss=$(awk -F',' '/LLC-load-misses/ {print $1}' perf_data.tmp)
            ctx_sw=$(awk -F',' '/context-switches/ {print $1}' perf_data.tmp)

            # Append to CSV
            echo "$mode,$threads,$size,$total_thr,$avg_lat,$cycles,$l1_miss,$llc_miss,$ctx_sw" >> $CSV_FILE
            
            # Cleanup for next iteration
            rm -f *.tmp
        done
    done
done

echo "Done. Results in $CSV_FILE"