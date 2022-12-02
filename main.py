# Simulates the communication between the different components of the AinQ scheme

import time    
from kgc import Kgc
from drone.leader import LeaderDrone
from drone.edge import EdgeDrone

print("---> starting")

# Init the KGC and the leader drone
kgc = Kgc()
omega = kgc.setup()
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
leader_drone.gen_secret_value(kgc.q, omega[0])
print("---> computed secret value for drone id =", leader_drone.d_i)
for drone in edge_drones:
    drone.gen_secret_value(kgc.q, omega[0])
    print("---> computed secret value for drone id =", drone.d_i)

# Compute partial public and private keys at the KGC
R_i, s_i = kgc.gen_partial_key(leader_drone.d_i, leader_drone.P_i, omega[5])
leader_drone.R_i = R_i
leader_drone.s_i = s_i
print("---> generating partial keypairs for all drones")
leader_drone.full_key_gen(s_i, R_i)
for drone in edge_drones:
    R_i, s_i = kgc.gen_partial_key(drone.d_i, drone.P_i, omega[5])
    drone.R_i = R_i
    drone.s_i = s_i
    (pk_i, sk_i) = drone.full_key_gen(s_i, R_i)

# Compute a group key at the leader drone
print("---> generating and retrieving group keys")
t_g = 600
group_key = leader_drone.gen_group_key(edge_drones, t_g, kgc.q, omega[0], omega[3], omega[4], omega[1])

# Key retrieval for edge drones
index = 0
for drone in edge_drones:
    drone.key_retrieval(group_key[0], group_key[1][index], omega[4], leader_drone.d_i, leader_drone.R_i, leader_drone.P_i, t_g)
    index += 1

print("---> retrieved the group key at all edge drones")
