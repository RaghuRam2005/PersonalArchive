from sympy import is_prime
from math import gcd

def generate_key(p, q):
    if not is_prime(p) and not is_prime(q):
        return None
    n = p*q
    phi = (p-1)*(q-1)
    e = next(s for s in range(2, phi) if gcd(s, phi) == 1)
    d = pow(e, -1, n)
    return ((e, n), (d, n))

def encrypt(msg, public_key):
    key, n = public_key
    encrypted_text = [pow(ord(c), key, n) for c in msg]
    return encrypted_text

def decrypt(msg, private_key):
    key, n = private_key
    decrypted_text = [chr(pow(c, key, n)) for c in msg]
    return decrypted_text
