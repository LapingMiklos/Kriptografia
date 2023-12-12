from random import randint, seed
from time import time
from utils import coprime, byte_to_bits, bits_to_byte, modinv

type PrivateKey = tuple[tuple, int, int]

def generate_private_key(n: int=8) -> PrivateKey:
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    seed(time())
    w = []
    total = 0
    lower = 2
    upper = 10
    for _ in range(n):
        w_i = randint(lower, upper)
        w.append(w_i)
        total += w_i
        lower, upper = total + 1, total * 2
    q = randint(lower, upper)
    r = randint(2, q-1)
    while not coprime(q, r):
        r = randint(2, q-1)

    return tuple(w), q, r

def create_public_key(private_key: PrivateKey) -> tuple:
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r x w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    w, q, r = private_key
    return tuple(r * w_i % q for w_i in w)


def encrypt_mh(message: bytes, public_key: tuple) -> list[int]:
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    return [
        sum(a_i * b_i for a_i, b_i in zip(byte_to_bits(byte), public_key))
        for byte
        in message
    ]


def decrypt_mh(message: list[int], private_key) -> bytes:
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    w, q, r = private_key
    s = modinv(r, q)
    c = [(byte * s) % q for byte in message]

    def decrypt(c_i: int) -> int:
        bits = []
        for w_i in reversed(w):
            if w_i <= c_i:
                bits.append(1)
                c_i -= w_i
            else:
                bits.append(0)
        
        bits.reverse()
        return bits_to_byte(bits)

    return bytes(decrypt(c_i) for c_i in c)