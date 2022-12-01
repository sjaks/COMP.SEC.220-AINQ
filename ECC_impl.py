### ================================ Base implementation for Tutorial 7 ================= ###
### ====================== Implements Point addition and Scalar Multiplication ========== ###

from dataclasses import dataclass
from re import I
from random import randint

@dataclass
class PrimeGaloisField:
    prime: int

    def __contains__(self, field_value: "FieldElement") -> bool:
        return 0 <= field_value.value < self.prime


@dataclass
class FieldElement:
    value: int
    field: PrimeGaloisField

    def __repr__(self):
        return "0x" + f"{self.value:x}".zfill(64)
        
    @property
    def P(self) -> int:
        return self.field.prime
    
    def __add__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value + other.value) % self.P,
            field=self.field
        )
    
    def __sub__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value - other.value) % self.P,
            field=self.field
        )

    def __rmul__(self, scalar: int) -> "FieldValue":
        return FieldElement(
            value=(self.value * scalar) % self.P,
            field=self.field
        )

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value * other.value) % self.P,
            field=self.field
        )
        
    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(
            value=pow(self.value, exponent, self.P),
            field=self.field
        )

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        other_inv = other ** -1
        return self * other_inv


@dataclass
class EllipticCurve:
    a: int
    b: int

    field: PrimeGaloisField

    def __contains__(self, point: "ECCPoint") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate the int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)

        # Whether the members of the curve parameters are in the field
        if self.a not in self.field or self.b not in self.field:
            raise ValueError

inf = float("inf")

# Representing an ECC Point using the curve equation yˆ2 = xˆ3 + ax + b
@dataclass
class ECCPoint:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        if self.x is None and self.y is None:
            return
        
        # Encapsulate x and y in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Ensure the ECCPoint satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    ##  ======== Point addition P1 + P2 = P3 ============== ##
    def __add__(self, other):
        if self == I:                       # I + P2 = P2
            return other

        if other == I:
            return self                     # P1 + I = P1

        if self.x == other.x and self.y == (-1 * other.y):
            return I                        # P + (-P) = I

        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            out = (y2 - y1) / (x2 - x1)
            x3 = out ** 2 - x1 - x2
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

        if self == other and self.y == inf:
            return I

        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            out = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = out ** 2 - 2 * x1
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

    ##  ======== Scalar Multiplication x * P1 = P1 ============== ##
    def __rmul__(self, scalar: int) -> "ECCPoint":
        inPoint = self
        outPoint = I

        while scalar:
            if scalar & 1:
                outPoint = outPoint + inPoint
            inPoint = inPoint + inPoint
            scalar >>= 1
        return outPoint


# Using the secp256k1 elliptic curve equation: yˆ2 = xˆ3 + 7
# Prime of the finite field
# Necessary parameters for the cryptographic operations
P: int = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

field = PrimeGaloisField(prime=P)

A: int = 0
B: int = 7

curve256k1 = EllipticCurve(
    a=A,
    b=B,
    field=field
)   

I = ECCPoint(x = None, y = None, curve = curve256k1)    # where I is a point at Infinity

# Generator point of the chosen group
G = ECCPoint(
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve = curve256k1
)

# Order of the group generated by G, such that nG = I
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


## ================================= Key generation phase ====================================== ##
import aes
from hashlib import sha256

def gen_hash(*args):
    text = f'{args}'
    return int(sha256(text.encode('utf-8')).hexdigest(), base=16)

x_master = randint(0, q)   # ramdom KGC master key
P_pub = x_master * G       # scalar multiplication, public key

# List of all users
users = {
    'Alice': {},
    'Bob': {}
}

kgc = {}

# Compute secret values and partial public keys for each user
for user in users:
    users[user]['id'] = 'ID_' + user[0]
    users[user]['x_i'] = randint(0, q)
    users[user]['P_i'] = users[user]['x_i'] * G

# Compute partial private key and partial public key for each user at KGC
for user in users:
    kgc[user] = {}
    kgc[user]['r_i'] = randint(0, q)
    kgc[user]['R_i'] = kgc[user]['r_i'] * G
    kgc[user]['d_i'] = kgc[user]['r_i'] + x_master * gen_hash(
                                                                users[user]['id'],
                                                                kgc[user]['R_i'],
                                                                users[user]['P_i']
                                                             )
# Compute the full private and public keys for each user
for user in users:
    users[user]['sk_i'] = [kgc[user]['d_i'], users[user]['x_i']]
    users[user]['PK_i'] = [kgc[user]['R_i'], users[user]['P_i']]

## ============================= Encryption and encapsulation ================================== ##
l_A = randint(0, q)
h_A = randint(0, q)
U = l_A * G
V = h_A * G

Y = kgc['Bob']['R_i'] + gen_hash(users['Bob']['id'], users[user]['PK_i'][0], users[user]['PK_i'][1]) * P_pub + users['Bob']['P_i']
T = h_A * Y


K_ab = gen_hash(Y, V, T, users['Bob']['id'], users['Bob']['P_i'])
print("K_ab1: " + str(K_ab))

d_a = 'Hello'
c_ab = aes.encrypt(d_a, str(K_ab))
print("To be encrypted: " + d_a)

H = gen_hash(U, c_ab, T, users['Alice']['id'], users['Bob']['id'], users['Alice']['P_i'], users['Bob']['P_i'])
W = kgc['Alice']['d_i'] + l_A * H + users['Alice']['x_i'] * H
phi = (U, V, W)

## ============================= Decryption and decapsulation ================================== ##
Y2 = (kgc['Bob']['d_i'] + users['Bob']['x_i']) * G
T2 = (kgc['Bob']['d_i'] + users['Bob']['x_i']) * V

H2 = gen_hash(U, c_ab, T2, users['Alice']['id'], users['Bob']['id'], users['Alice']['P_i'], users['Bob']['P_i'])
K_ab2 = gen_hash(Y2, V, T2, users['Bob']['id'], users['Bob']['P_i'])
print("K_ab2: " + str(K_ab2))

pt_a = aes.decrypt(c_ab, str(K_ab2))
print("Decypted: " + pt_a)
