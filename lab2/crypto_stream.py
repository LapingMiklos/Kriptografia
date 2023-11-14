from typing import Callable, Iterable, Iterator

type StreamGenerator[T] = Callable[[T], Iterator[int]]

def stream_encryption[T](data: Iterable[int], seed: T, stream_generator: StreamGenerator[T]) -> Iterator[int]:
    for p, k in zip(data, stream_generator(seed)):
        yield p ^ k

with open("asd.txt", "rb") as f:
    seed = 10
    encrypted = stream_encryption(f.read(), seed, lambda x: range(100))

    decrypted = stream_encryption(encrypted, seed, lambda x: range(100))
    print(bytes(decrypted))
