# Simulates the communication between the different components of the AinQ scheme

from kgc import Kgc
from drone.leader import LeaderDrone
from drone.edge import EdgeDrone

kgc = Kgc()

# Init the KGC and the leader drone
omega = kgc.setup()
leader_drone = LeaderDrone()
edge_drones = []

# Add new edge drones
for i in range(3):
    new_edge = EdgeDrone()
    edge_drones.append(new_edge)

# Compute secret values for each drone
leader_drone.gen_secret_value(kgc.q, omega[0])
for drone in edge_drones:
    drone.gen_secret_value(kgc.q, omega[0])

# Compute partial public keys at the KGC
R_i, s_i = kgc.gen_partial_key(leader_drone.d_i, leader_drone.P_i, omega[5])
leader_drone.full_key_gen(s_i, R_i)
for drone in edge_drones:
    R_i, s_i = kgc.gen_partial_key(drone.d_i, drone.P_i, omega[5])
    (pk_i, sk_i) = drone.full_key_gen(s_i, R_i) # compute the full keys after getting the partials

# Compute a group key at the leader drone
leader_drone.gen_group_key(edge_drones, "", kgc.q)
