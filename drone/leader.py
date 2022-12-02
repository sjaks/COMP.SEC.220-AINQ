from drone.base import BaseDrone
from random import randint

class LeaderDrone(BaseDrone):
    K_g: int
    l_k: int

    def gen_group_key(self, GL, t_g, q):
        C_i = []
        self.K_g = randint(0, q)
        self.l_k = randint(0, q)

        P = 0
        V = self.l_k * P # TODO: what is P?

        cipher_texts = []
        for drone in GL:
            pk_i = (drone.R_i, drone.P_i) # TODO: add R_i to base.py

            Y_i = "" # TODO: calculate Y_i, T_i and C_i
            T_i = ""
            C_i = ""
            cipher_texts.append(C_i)

        return (V, cipher_texts, t_g)
