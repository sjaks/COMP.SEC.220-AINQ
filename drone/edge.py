from drone.base import BaseDrone

class EdgeDrone(BaseDrone):
    def key_retrieval(self, V, C_i, H_1, q_k, R_k, P_k, t_g):
        # Retrieve the group key from the common and drone parameters
        T_i = (self.s_i + self.x_i) * V
        K_g = C_i ^ H_1(V, T_i, q_k, R_k, P_k, self.d_i, self.R_i, self.P_i, t_g)
        print("------> retrieved group key", K_g)
        self.K_g = K_g
