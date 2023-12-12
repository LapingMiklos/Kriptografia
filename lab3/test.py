import sys
from random import shuffle

sys.path.append('../lab2')

from merkle_hellman import generate_private_key, create_public_key, encrypt_mh, decrypt_mh
from crypto_classes import PrivateKeyDecrypter, PublicKeyEncrypter
from utils import is_superincreasing, coprime
from generators import solitaire
from crypto_stream import StreamEncrypter, test_generator

msgs = [
    b'egy kis message',
    b'szia hogy vagy?',
    "non asscii áááasdüú".encode(),
    b'asd',
    b'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet deleniti vel id esse culpa laboriosam est dolorum soluta aut laudantium. Sapiente repudiandae doloremque enim earum incidunt quaerat expedita minus autem!'
]

def test_merkle_hellman():
    print('Testing Merkle Hellman')
    w, q, r = generate_private_key()
    print('w =', w)
    print('q =', q)
    print('r =', r)
    assert is_superincreasing(w)
    assert coprime(q, r)
    assert q > sum(w)
    beta = create_public_key((w, q, r))
    print('beta =', beta)

    encrypt = PublicKeyEncrypter(beta, encrypt_mh)
    decrypt = PrivateKeyDecrypter((w, q, r), decrypt_mh)
    for msg in msgs:
        assert msg == decrypt(encrypt(msg))
    print('Testing successful\n')

def test_solitaire():
    print('Testing solitaire')
    DECK = [i + 1 for i in range(54)]
    shuffle(DECK)
    print('Seed =', DECK)

    test_generator([card for card in DECK], solitaire, 'solitaire')

    encrypt = StreamEncrypter([card for card in DECK], solitaire)
    decrypt = StreamEncrypter([card for card in DECK], solitaire)
    
    for msg in msgs:
        assert msg == decrypt(encrypt(msg))
    print('Testing successful\n')
    

if __name__ == '__main__':
    test_merkle_hellman()
    test_solitaire()