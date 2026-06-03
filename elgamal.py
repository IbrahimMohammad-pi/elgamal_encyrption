def hcf(a, b):
    if a<b: 
        a, b = b, a 
    if b == 0:
        return a 
    return hcf(b, a % b)

def elgamal(p,):
    pass 

def fast_modular(base:int,exp:int,p:int):
    if exp == 0:
        return 1
    odd = exp % 2
    extra = base * odd 
    exp = exp - odd
    t = fast_modular(base, exp // 2, p)
    return (extra * (t**2) % p) 



class key:
    def __init__(self, x, g, p):
        self.x = x 
        self.g = g
        self.p = p 
        self.A = fast_modular(g, x, p) 

    

class TEST