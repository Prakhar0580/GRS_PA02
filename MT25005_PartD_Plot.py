# import matplotlib.pyplot as plt
# import numpy as np

# # --- SYSTEM CONFIGURATION ---
# SYSTEM_INFO = "AMD Ryzen-5 4000 Series @ 2.40GHz, 16GB RAM, Ubuntu 22.04"

# # --- HARDCODED DATA (Kept exactly as provided) ---
# msg_sizes = [1024, 4096, 16384, 65536]
# thread_counts = [1, 2, 3, 4]

# # Data provided (40 values)
# throughput_gbps = [2.2908 , 2.1500 , 2.1592 , 1.9577 , 2.1400 , 1.9838 , 1.7824 , 1.9957 , 1.8635 , 1.9080 , 1.9778 , 2.0068 , 2.0146 ,  1.7761 ,  1.7632 , 1.7586 , 1.6070 , 1.5948, 1.6066, 1.5982 , 1.9144 , 1.8981, 1.9298, 1.7396, 1.7167 , 1.7448 ,  1.6335 , 1.6176 , 1.6069 , 1.5902 , 1.8504 , 1.9335, 1.9584 , 1.7567 , 1.7269 , 1.7801 , 1.6206 , 1.6085 , 1.6138 , 1.6312]     
# latency_us = [3.58, 3.81,  3.79, 4.18 , 3.83 , 4.13 , 4.60 , 4.10 ,  4.40 , 4.29 , 16.57 , 16.33 ,  16.26 , 18.45 , 18.58 , 18.63 , 20.39 , 20.55  ,  20.40 , 20.50 , 68.47 , 69.06 , 67.92  , 75.34 ,  76.35 , 75.12 , 80.24 ,  81.03, 81.57 , 82.42 ,  283.33 , 271.16 , 267.73 , 298.46 , 303.61 , 294.53 , 323.51 ,  325.96 , 324.89 , 321.42 ]  

# # Data provided (16 values)
# cache_misses = [737068 ,   694599 , 688163 , 744233 , 684437 , 717500 , 725480 ,  696533 ,  695418  , 775444 , 692358 , 725757 , 729660, 713052 , 721353  ,  765523 ] 
# cpu_cycles = [ 45764588 , 42173686,  44456803,  53494208 ,  43431137 ,   44049079  , 43747135 ,  42473481 ,  43199409 ,  54916924 ,  43101071 , 40945312 , 46594167 ,  41174770 , 50171139 , 42085129 ] 

# # --- DATA PROCESSING (Averaging to match dimensions) ---

# # Plot 1: Average Throughput per Message Size (4 points)
# # Groups of 10 from the 40 values
# avg_throughput = [np.mean(throughput_gbps[i:i+10]) for i in range(0, 40, 10)]

# # Plot 2: Average Latency per Thread Count (4 points)
# # Groups of 10 from the 40 values
# avg_latency = [np.mean(latency_us[i:i+10]) for i in range(0, 40, 10)]

# # Plot 3: Average Cache Misses per Message Size (4 points)
# # Groups of 4 from the 16 values
# avg_cache = [np.mean(cache_misses[i:i+4]) for i in range(0, 16, 4)]

# # Plot 4: Average CPU Cycles per Byte Transferred (4 points)
# avg_cycles = [np.mean(cpu_cycles[i:i+4]) for i in range(0, 16, 4)]
# cycles_per_byte = [c / s for c, s in zip(avg_cycles, msg_sizes)]

# # --- PLOTTING ---
# fig, axs = plt.subplots(2, 2, figsize=(14, 10))
# plt.subplots_adjust(hspace=0.4, wspace=0.3)
# fig.suptitle(f'Performance Analysis - Mode 3 (Zero-Copy)\n{SYSTEM_INFO}', fontsize=16)

# # Plot 1: Throughput vs Message Size
# axs[0, 0].plot(msg_sizes, avg_throughput, marker='o', color='b', label='Avg Throughput')
# axs[0, 0].set_title('Throughput vs Message Size')
# axs[0, 0].set_xlabel('Message Size (Bytes)')
# axs[0, 0].set_ylabel('Throughput (Gbps)')
# axs[0, 0].grid(True)
# axs[0, 0].legend()

# # Plot 2: Latency vs Thread Count
# axs[0, 1].plot(thread_counts, avg_latency, marker='s', color='r', label='Avg Latency')
# axs[0, 1].set_title('Latency vs Thread Count')
# axs[0, 1].set_xlabel('Thread Count')
# axs[0, 1].set_ylabel('Latency (us)')
# axs[0, 1].grid(True)
# axs[0, 1].legend()

# # Plot 3: Cache Misses vs Message Size
# axs[1, 0].bar([str(s) for s in msg_sizes], avg_cache, color='orange', label='Avg L1 Misses')
# axs[1, 0].set_title('Cache Misses vs Message Size')
# axs[1, 0].set_xlabel('Message Size (Bytes)')
# axs[1, 0].set_ylabel('Number of Misses')
# axs[1, 0].grid(axis='y')
# axs[1, 0].legend()

# # Plot 4: CPU Cycles per Byte Transferred
# axs[1, 1].plot(msg_sizes, cycles_per_byte, marker='^', color='g', label='Efficiency')
# axs[1, 1].set_title('CPU Cycles per Byte Transferred')
# axs[1, 1].set_xlabel('Message Size (Bytes)')
# axs[1, 1].set_ylabel('Cycles/Byte')
# axs[1, 1].grid(True)
# axs[1, 1].legend()

# plt.savefig('MT25005_Performance_Plots.png')
# print("Plots generated successfully using averaged values.")
# plt.show()
# ----------------------------------------------


import matplotlib.pyplot as plt
import numpy as np

# --- SYSTEM CONFIGURATION ---
SYSTEM_INFO = "AMD Ryzen-5 4000 Series @ 2.40GHz, Ubuntu 22.04"

# --- HARDCODED DATA FROM IMAGES ---
msg_sizes = [1024, 4096, 16384, 65536]
thread_counts = [1, 2, 3, 4]

# Throughput Data (Gbps)
throughput_mode1 = [0.9027, 1.6858, 2.2901, 2.9, 0.8593, 1.5697, 2.2764, 2.841, 0.86, 1.6107, 2.3431, 2.8303, 0.8407, 1.5136, 2.1179, 2.9405]
throughput_mode2 = [3.6182, 9.7949, 16.4021, 20.7863, 3.2327, 6.0285, 7.9503, 10.238, 3.0676, 5.5558, 7.6989, 10.1736, 3.1097, 5.6912, 8.1272, 10.0043]
throughput_mode3 = [6.3869, 7.4874, 18.5701, 21.629, 3.0127, 5.9696, 7.8635, 10.561, 3.2083, 5.4392, 7.9647, 10.1469, 3.0698, 5.8103, 8.3175, 10.1392]

# Latency Data (us)
latency_mode1 = [9.07, 9.725, 10.7367, 11.3, 38.13, 41.745, 43.1867, 46.16, 152.41, 162.745, 167.86, 185.322, 623.64, 692.77, 744.84, 713.377]
latency_mode2 = [2.26, 1.81, 1.59333, 1.59, 10.14, 10.87, 12.3733, 12.8025, 42.73, 47.185, 51.09, 51.5575, 168.6, 184.25, 193.543, 209.857]
latency_mode3 = [1.28, 2.2, 1.32667, 1.515, 10.88, 10.98, 12.5033, 12.4125, 40.85, 48.225, 49.37, 51.6825, 170.79, 180.47, 189.107, 206.845]

# CPU Cycles
cycles_mode1 = [36443427007, 67615949647, 91261086339, 130248895080, 38639872339, 69406222153, 100143440906, 129383628116, 36774024702, 67419317456, 96127347914, 132176371579, 37319953397, 67846843678, 96145372791, 121352802065]
cycles_mode2 = [34849734568, 55278702909, 72217633223, 99144851950, 38535685379, 72103018851, 100022225928, 127517805002, 36172187635, 66797492831, 93359227081, 133941750368, 38848821739, 70398455285, 99439431482, 122982336731]
cycles_mode3 = [24907595558, 66097048281, 63615389522, 84105464148, 37286679754, 71449092472, 98120570237, 127966579328, 36269080202, 64623206887, 103702720388, 130713957142, 36893210128, 69960224460, 100303051934, 123914673402]

# Cache Misses (Estimated based on Image 2, capturing a sample for visualization)
# As LLC Misses were "not supported" in most runs, we use representative L1 misses from valid runs
l1_misses_sample = [400770352, 100496419, 396912719, 905299834] 

# --- DATA PROCESSING ---

def get_avg_by_msg_size(data):
    # Data is ordered as (Size1,T1), (Size1,T2)...
    # Reshape and mean across thread counts to get average per message size
    return np.mean(np.array(data).reshape(4, 4), axis=1)

def get_avg_by_threads(data):
    # Reshape and mean across message sizes to get average per thread count
    return np.mean(np.array(data).reshape(4, 4), axis=0)

# 1. Throughput averages (per Msg Size)
avg_thr_m1 = get_avg_by_msg_size(throughput_mode1)
avg_thr_m2 = get_avg_by_msg_size(throughput_mode2)
avg_thr_m3 = get_avg_by_msg_size(throughput_mode3)

# 2. Latency averages (per Thread Count)
avg_lat_m1 = get_avg_by_threads(latency_mode1)
avg_lat_m2 = get_avg_by_threads(latency_mode2)
avg_lat_m3 = get_avg_by_threads(latency_mode3)

# 3. CPU Efficiency (Cycles per Byte)
def get_cpb(cycles, sizes):
    avg_cyc = get_avg_by_msg_size(cycles)
    return [c / s for c, s in zip(avg_cyc, sizes)]

cpb_m1 = get_cpb(cycles_mode1, msg_sizes)
cpb_m2 = get_cpb(cycles_mode2, msg_sizes)
cpb_m3 = get_cpb(cycles_mode3, msg_sizes)

# --- PLOTTING ---
fig, axs = plt.subplots(2, 2, figsize=(15, 11))
plt.subplots_adjust(hspace=0.4, wspace=0.3)
fig.suptitle(f'Comparative Multi-Mode Performance Analysis\n{SYSTEM_INFO}', fontsize=16)

# Plot 1: Throughput vs Message Size
axs[0, 0].plot(msg_sizes, avg_thr_m1, marker='o', label='Mode 1 (2-Copy)')
axs[0, 0].plot(msg_sizes, avg_thr_m2, marker='s', label='Mode 2 (1-Copy)')
axs[0, 0].plot(msg_sizes, avg_thr_m3, marker='^', label='Mode 3 (Zero-Copy)')
axs[0, 0].set_title('Throughput vs Message Size')
axs[0, 0].set_xlabel('Message Size (Bytes)')
axs[0, 0].set_ylabel('Throughput (Gbps)')
axs[0, 0].grid(True)
axs[0, 0].legend()

# Plot 2: Latency vs Thread Count
axs[0, 1].plot(thread_counts, avg_lat_m1, marker='o', label='Mode 1')
axs[0, 1].plot(thread_counts, avg_lat_m2, marker='s', label='Mode 2')
axs[0, 1].plot(thread_counts, avg_lat_m3, marker='^', label='Mode 3')
axs[0, 1].set_title('Latency vs Thread Count')
axs[0, 1].set_xlabel('Thread Count')
axs[0, 1].set_ylabel('Latency (us)')
axs[0, 1].grid(True)
axs[0, 1].legend()

# Plot 3: Cache Misses (Sample L1 Misses across Message Sizes)
axs[1, 0].bar([str(s) for s in msg_sizes], l1_misses_sample, color='teal', alpha=0.7)
axs[1, 0].set_title('Representative L1 Cache Misses vs Message Size')
axs[1, 0].set_xlabel('Message Size (Bytes)')
axs[1, 0].set_ylabel('L1 D-Cache Misses')
axs[1, 0].grid(axis='y', linestyle='--')

# Plot 4: CPU Cycles per Byte
axs[1, 1].plot(msg_sizes, cpb_m1, marker='o', label='Mode 1')
axs[1, 1].plot(msg_sizes, cpb_m2, marker='s', label='Mode 2')
axs[1, 1].plot(msg_sizes, cpb_m3, marker='^', label='Mode 3')
axs[1, 1].set_title('CPU Cycles per Byte Transferred')
axs[1, 1].set_xlabel('Message Size (Bytes)')
axs[1, 1].set_ylabel('Cycles / Byte')
axs[1, 1].grid(True)
axs[1, 1].legend()

plt.show()