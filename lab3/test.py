from merkle_hellman import generate_private_key, create_public_key, encrypt_mh, decrypt_mh
from utils import is_superincreasing, coprime

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

    msgs = [
        b'egy kis message'
        b'szia hogy vagy'
        b'asd'
        b'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Amet deleniti vel id esse culpa laboriosam est dolorum soluta aut laudantium. Sapiente repudiandae doloremque enim earum incidunt quaerat expedita minus autem!'
    ]

    for msg in msgs:
        assert msg == decrypt_mh(encrypt_mh(msg, beta), (w, q, r))

if __name__ == '__main__':
    test_merkle_hellman()