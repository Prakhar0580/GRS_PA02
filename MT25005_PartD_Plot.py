import matplotlib.pyplot as plt
import numpy as np

# --- SYSTEM CONFIGURATION ---
SYSTEM_INFO = "System: Intel i5-1135G7 @ 2.40GHz, 16GB RAM, Ubuntu 22.04"

# --- HARDCODED DATA (Kept exactly as provided) ---
msg_sizes = [1024, 4096, 16384, 65536]
thread_counts = [1, 2, 3, 4]

# Data provided (40 values)
throughput_gbps = [2.2908 , 2.1500 , 2.1592 , 1.9577 , 2.1400 , 1.9838 , 1.7824 , 1.9957 , 1.8635 , 1.9080 , 1.9778 , 2.0068 , 2.0146 ,  1.7761 ,  1.7632 , 1.7586 , 1.6070 , 1.5948, 1.6066, 1.5982 , 1.9144 , 1.8981, 1.9298, 1.7396, 1.7167 , 1.7448 ,  1.6335 , 1.6176 , 1.6069 , 1.5902 , 1.8504 , 1.9335, 1.9584 , 1.7567 , 1.7269 , 1.7801 , 1.6206 , 1.6085 , 1.6138 , 1.6312]     
latency_us = [3.58, 3.81,  3.79, 4.18 , 3.83 , 4.13 , 4.60 , 4.10 ,  4.40 , 4.29 , 16.57 , 16.33 ,  16.26 , 18.45 , 18.58 , 18.63 , 20.39 , 20.55  ,  20.40 , 20.50 , 68.47 , 69.06 , 67.92  , 75.34 ,  76.35 , 75.12 , 80.24 ,  81.03, 81.57 , 82.42 ,  283.33 , 271.16 , 267.73 , 298.46 , 303.61 , 294.53 , 323.51 ,  325.96 , 324.89 , 321.42 ]  

# Data provided (16 values)
cache_misses = [737068 ,   694599 , 688163 , 744233 , 684437 , 717500 , 725480 ,  696533 ,  695418  , 775444 , 692358 , 725757 , 729660, 713052 , 721353  ,  765523 ] 
cpu_cycles = [ 45764588 , 42173686,  44456803,  53494208 ,  43431137 ,   44049079  , 43747135 ,  42473481 ,  43199409 ,  54916924 ,  43101071 , 40945312 , 46594167 ,  41174770 , 50171139 , 42085129 ] 

# --- DATA PROCESSING (Averaging to match dimensions) ---

# Plot 1: Average Throughput per Message Size (4 points)
# Groups of 10 from the 40 values
avg_throughput = [np.mean(throughput_gbps[i:i+10]) for i in range(0, 40, 10)]

# Plot 2: Average Latency per Thread Count (4 points)
# Groups of 10 from the 40 values
avg_latency = [np.mean(latency_us[i:i+10]) for i in range(0, 40, 10)]

# Plot 3: Average Cache Misses per Message Size (4 points)
# Groups of 4 from the 16 values
avg_cache = [np.mean(cache_misses[i:i+4]) for i in range(0, 16, 4)]

# Plot 4: Average CPU Cycles per Byte Transferred (4 points)
avg_cycles = [np.mean(cpu_cycles[i:i+4]) for i in range(0, 16, 4)]
cycles_per_byte = [c / s for c, s in zip(avg_cycles, msg_sizes)]

# --- PLOTTING ---
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.3)
fig.suptitle(f'Performance Analysis - Mode 3 (Zero-Copy)\n{SYSTEM_INFO}', fontsize=16)

# Plot 1: Throughput vs Message Size
axs[0, 0].plot(msg_sizes, avg_throughput, marker='o', color='b', label='Avg Throughput')
axs[0, 0].set_title('Throughput vs Message Size')
axs[0, 0].set_xlabel('Message Size (Bytes)')
axs[0, 0].set_ylabel('Throughput (Gbps)')
axs[0, 0].grid(True)
axs[0, 0].legend()

# Plot 2: Latency vs Thread Count
axs[0, 1].plot(thread_counts, avg_latency, marker='s', color='r', label='Avg Latency')
axs[0, 1].set_title('Latency vs Thread Count')
axs[0, 1].set_xlabel('Thread Count')
axs[0, 1].set_ylabel('Latency (us)')
axs[0, 1].grid(True)
axs[0, 1].legend()

# Plot 3: Cache Misses vs Message Size
axs[1, 0].bar([str(s) for s in msg_sizes], avg_cache, color='orange', label='Avg L1 Misses')
axs[1, 0].set_title('Cache Misses vs Message Size')
axs[1, 0].set_xlabel('Message Size (Bytes)')
axs[1, 0].set_ylabel('Number of Misses')
axs[1, 0].grid(axis='y')
axs[1, 0].legend()

# Plot 4: CPU Cycles per Byte Transferred
axs[1, 1].plot(msg_sizes, cycles_per_byte, marker='^', color='g', label='Efficiency')
axs[1, 1].set_title('CPU Cycles per Byte Transferred')
axs[1, 1].set_xlabel('Message Size (Bytes)')
axs[1, 1].set_ylabel('Cycles/Byte')
axs[1, 1].grid(True)
axs[1, 1].legend()

plt.savefig('MT25005_Performance_Plots.png')
print("Plots generated successfully using averaged values.")
plt.show()