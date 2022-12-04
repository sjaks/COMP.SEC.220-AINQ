from drone.base import BaseDrone
from random import randint

class LeaderDrone(BaseDrone):
    K_g: int
    l_k: int
    GL_i: list


    def gen_group_key(self, GL, t_g, q, G, H_0, H_1, P_pub):
        # Compute a random group key and broadcast ciphertexts for each drone
        self.GL_i = GL
        C_i = []
        self.K_g = randint(0, q)    # random group key
        self.l_k = randint(0, q)

        print("------> generated group key", self.K_g)

        V = self.l_k * G

        cipher_texts = []
        for drone in GL:
            # Generate for each drone
            Y_i = drone.R_i + H_0(drone.d_i, drone.R_i, drone.P_i) * P_pub + drone.P_i
            T_i = self.l_k * Y_i
            C_i = self.K_g ^ H_1(V, T_i, self.d_i, self.R_i, self.P_i, drone.d_i, drone.R_i, drone.P_i, t_g)
            cipher_texts.append(C_i)

        # Broadcast values for group key generation in each drone
        return (V, cipher_texts, t_g)


    def rekey(self, GL, q, G, H_0, H_1, P_pub, t_g):
        # Recalculate a group key for updated edge drone list
        K_g_n = randint(0, q)   # new group key
        V = self.l_k * G
    
        print("------> re-keyed group key ", K_g_n)

        cipher_texts = []
        for drone in GL:
            # Recalculate ciphertexts
            Y_i = drone.R_i + H_0(drone.d_i, drone.R_i, drone.P_i) * P_pub + drone.P_i
            T_i = self.l_k * Y_i
            C_i = K_g_n ^ H_1(V, T_i, self.d_i, self.R_i, self.P_i, drone.d_i, drone.R_i, drone.P_i, t_g)
            cipher_texts.append(C_i)

        self.GL_i = GL
        self.K_g = K_g_n

        # Broadcast updated values for key retrieval
        return (V, cipher_texts, t_g)
