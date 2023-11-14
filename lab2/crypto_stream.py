from typing import Callable, Iterator
from generators import solitaire, blum_blum_shub

type StreamGenerator[T] = Callable[[T], Iterator[int]]

def test_generator[T](seed: T, generator: StreamGenerator[T], method_name: str, iterations: int = 100000):
    print(f"Testing rng {method_name}: ")
    stream = generator(seed)
    bytes_list = []
    hist = [0 for _ in range(256)]

    for _ in range(iterations):
        byte = next(stream)
        hist[byte] += 1
        bytes_list.append(byte)

    E = sum(bytes_list) / len(bytes_list)
    print("Mean: ", E)
    VAR = sum([byte ** 2 for byte in bytes_list]) / len(bytes_list) - E ** 2
    print("Std dev: ",  VAR ** 0.5)
    print("Min: ", min(hist))
    print("Max: ", max(hist))
    # print("Hist: ", hist)
    

class StreamEncrypter[T]:
    def __init__(self, seed: T, generator: StreamGenerator[T]):
        self.stream = generator(seed)

    def __call__(self, data: bytes) -> bytes:
        e = bytearray()
        for p, k in zip(data, self.stream):
            e.append(p ^ k)
        return bytes(e)

test_generator(2, blum_blum_shub, "Blum Blum Shub")
test_generator([x + 1 for x in range(54)], solitaire, "Solitaire")