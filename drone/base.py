from util.ecc import ECCPoint
from random import randint

class BaseDrone:
    d_i: str
    x_i: int
    P_i: ECCPoint
    s_i: int
    R_i: ECCPoint


    def __init__(self):
        self.d_i = str(randint(0, 9999))


    def gen_secret_value(self, q, G):
        self.x_i = randint(0, q)
        self.P_i = self.x_i * G


    def full_key_gen(self, s_i, R_i):
        sk_i = [s_i, self.x_i]
        pk_i = [R_i, self.P_i]

        return (pk_i, sk_i)
