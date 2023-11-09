from typing import Callable, TypeVar, Iterator

type Method[T] = Callable[[T], Iterator[int]]
T = TypeVar('T')

def stream_encryption(data: Iterator[int], seed: T, stream_generator: Method[T]) -> Iterator[int]:
    for p, k in zip(data, stream_generator(seed)):
        yield p ^ k

    