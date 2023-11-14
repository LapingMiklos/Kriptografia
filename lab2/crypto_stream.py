from typing import Callable, Iterator
from solitaire import solitaire
type StreamGenerator[T] = Callable[[T], Iterator[int]]

class StreamEncrypter[T]:
    def __init__(self, seed: T, generator: StreamGenerator[T]):
        self.stream = generator(seed)

    def __call__(self, data: bytes) -> bytes:
        e = bytearray()
        for p, k in zip(data, self.stream):
            e.append(p ^ k)
        return bytes(e)

seed = [x + 1 for x in range(54)]
stream = solitaire(seed)


bytes_list = []
hist = [0 for _ in range(256)]
i = 0
for byte in stream:
    # print(byte)
    hist[byte] += 1
    bytes_list.append(byte)
    i += 1
    if i > 10000:
        break

print(sum(bytes_list) / len(bytes_list))
print(min(hist), max(hist))
print(hist)

message = bytes(input("What do you wanna encrytp? "), encoding='utf8')

encrypter = StreamEncrypter(seed, solitaire)
decrypter = StreamEncrypter(seed, solitaire)

e = bytes(encrypter(message))
# e = bytes(encrypter.transform(message))
print(e)
d = bytes(decrypter(e))
# d = bytes(decrypter.transform(e))
print(d)