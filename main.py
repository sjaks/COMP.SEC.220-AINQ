# Simulates the communication between the different components of the AinQ scheme

import time    
from kgc import Kgc
from drone.leader import LeaderDrone
from drone.edge import EdgeDrone

print("---> starting")

# Init the KGC and the leader drone
kgc = Kgc()
o = kgc.setup()
leader_drone = LeaderDrone()
edge_drones = []
EDGE_DRONE_NRO = 10

print("---> added 1 team leader drone")

# Add new edge drones
for i in range(EDGE_DRONE_NRO):
    new_edge = EdgeDrone()
    edge_drones.append(new_edge)

print("---> added", str(len(edge_drones)), "edge drones")

# Compute secret values for each drone
leader_drone.gen_secret_value(kgc.q, o["G"])
print("---> computed secret value for drone id =", leader_drone.d_i)
for drone in edge_drones:
    drone.gen_secret_value(kgc.q, o["G"])
    print("---> computed secret value for drone id =", drone.d_i)

# Compute partial public and private keys at the KGC
R_i, s_i = kgc.gen_partial_key(leader_drone.d_i, leader_drone.P_i, o["x"])
leader_drone.R_i = R_i
leader_drone.s_i = s_i
print("---> generating partial keypairs for all drones")
leader_drone.full_key_gen(s_i, R_i) # upon receiption, generate full keys for leader
for drone in edge_drones:
    R_i, s_i = kgc.gen_partial_key(drone.d_i, drone.P_i, o["x"])
    drone.R_i = R_i
    drone.s_i = s_i
    drone.full_key_gen(s_i, R_i) # generate full keys for edge drones

# Compute a group key at the leader drone
print("---> generating and retrieving group keys")
t_g = 600 # some time validity
group_key = leader_drone.gen_group_key(edge_drones, t_g, kgc.q, o["G"], o["H_0"], o["H_1"], o["P_pub"])

# Key retrieval for edge drones
index = 0
for drone in edge_drones:
    drone.key_retrieval(group_key[0], group_key[1][index], o["H_1"], leader_drone.d_i, leader_drone.R_i, leader_drone.P_i, t_g)
    index += 1

print("---> retrieved the group key at all edge drones")

# Add a new edge drone and rekey
print("---> adding a new edge drone")
additional_edge_drone = EdgeDrone()
additional_edge_drone.gen_secret_value(kgc.q, o["G"])
R_i, s_i = kgc.gen_partial_key(additional_edge_drone.d_i, additional_edge_drone.P_i, o["x"])
additional_edge_drone.R_i = R_i
additional_edge_drone.s_i = s_i
edge_drones.append(additional_edge_drone)
print("---> added a new edge drone")

# Regenerate group key for the updated drone list
group_key = leader_drone.rekey(edge_drones, kgc.q, o["G"], o["H_0"], o["H_1"], o["P_pub"], t_g)

# Re-key retrieval for edge drones
index = 0
for drone in edge_drones:
    drone.key_retrieval(group_key[0], group_key[1][index], o["H_1"], leader_drone.d_i, leader_drone.R_i, leader_drone.P_i, t_g)
    index += 1

print("---> all done")
