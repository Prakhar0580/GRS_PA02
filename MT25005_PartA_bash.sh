#!/bin/bash

# 1. Create the namespaces
sudo ip netns add ns_server
sudo ip netns add ns_client

# 2. Create the virtual cable
sudo ip link add veth_s type veth peer name veth_c

# 3. Connect cable to namespaces
sudo ip link set veth_s netns ns_server
sudo ip link set veth_c netns ns_client

# 4. Assign IP addresses (This replaces the failed ifconfig lines)
sudo ip netns exec ns_server ip addr add 10.0.0.1/24 dev veth_s
sudo ip netns exec ns_client ip addr add 10.0.0.2/24 dev veth_c

# 5. Bring the interfaces UP
sudo ip netns exec ns_server ip link set veth_s up
sudo ip netns exec ns_client ip link set veth_c up
sudo ip netns exec ns_server ip link set lo up
sudo ip netns exec ns_client ip link set lo up