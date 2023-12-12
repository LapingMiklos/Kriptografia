from typing import Callable

type EncryptionMethod[T] = Callable[[bytes, T], list[int]]

type DecryptionMethod[T] = Callable[[list[int], T], bytes]

class PublicKeyEncrypter[T]:
    def __init__(self, public_key: T, encryption_method: EncryptionMethod[T]):
        self.public_key = public_key
        self.encryption_method = encryption_method 

    def __call__(self, data: bytes) -> list[int]:
        return self.encryption_method(data, self.public_key)
    
class PrivateKeyDecrypter[T]:
    def __init__(self, private_key: T, decryption_method: DecryptionMethod[T]):
        self.private_key = private_key
        self.decryption_method = decryption_method 

    def __call__(self, data: list[int]) -> bytes:
        return self.decryption_method(data, self.private_key)
        