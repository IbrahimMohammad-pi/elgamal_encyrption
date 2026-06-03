import secrets
import random
import math

def extended_euclid(a,b):
    if a<b: 
        a, b = b, a 
    if b == 0:
        return (a,1,0)
    q = a // b
    r = a % b
    hcf, i, j = extended_euclid(b, r)
    return hcf, j, i - j * q


def elgamal(p,):
    pass 

def fast_modular(base: int, exp: int, p: int):
    base %= p

    if exp == 0:
        return 1

    odd = exp & 1
    extra = 1 + (base - 1) * odd

    exp -= odd

    t = fast_modular(base, exp // 2, p)

    return (extra * (t * t % p)) % p

def string_to_int(message: str) -> int:
    return int.from_bytes(message.encode("utf-8"), byteorder="big")


def int_to_string(value: int) -> str:
    if value == 0:
        return ""
    
    length = (value.bit_length() + 7) // 8
    return value.to_bytes(length, byteorder="big").decode("utf-8")

def not_prime(x,p):
    exp = p-1 
    if fast_modular(x, exp, p) != 1: return True
    exp = exp // 2
    while exp % 2 != 0:
        c = fast_modular(x, exp, p)
        if c != 1 or c != -1: return True 
        elif c == 1:
            exp = exp // 2
            continue
        else:
            return False
    return False 


def gen_prime(bits = 8, k:int = 5, q:float = 0.25): #so k is a paramter of how sure we are
    if bits< 3:
        raise ValueError("too little bits")
    t = math.ceil(-k / math.log2(q))

    while True:
        p = 0
        while p % 2 == 0:# the number we are trying to test for prime
            p = random.getrandbits(bits)
        
        i = 0
        while i < t:
            i += 1
            x = random.randint(2,p-2)
            if not_prime(x,p): break 
        else:
            return p 

        


        
    



class key:
    def __init__(self, x, g, p):
        self._x = x 
        self.g = g
        self.p = p 
        self.A = fast_modular(g, x, p) 

    @classmethod
    def generate_key(cls):
        
        pass #need to generate prime numbers

    def decrypt(self, a, b):
        shared = fast_modular(a, self._x, self.p)
        hcf, i, j = extended_euclid(self.p, shared)
        if hcf != 1:
            raise Exception("shared is not coprime with p, which is bad")
        message = (b * j) % self.p
        return int_to_string(message)

    @staticmethod
    def encrypt(public_key, message_string):
        message = string_to_int(message_string)
        if message >= public_key.p:
            raise ValueError("message is too big for p")
        k = 17  # for now use this. we just need a random k.
        a = fast_modular(public_key.g, k, public_key.p)
        b = (message * fast_modular(public_key.A, k, public_key.p)) % public_key.p
        return a, b




    
