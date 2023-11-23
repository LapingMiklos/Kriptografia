from typing import Iterator, Callable
from math import gcd

class InvalidSeedException(Exception):
    pass

type Deck = list[int]

JOKER_A = 53
JOKER_B = 54
DECK_LEN = 54

def joker_push(deck: Deck) -> Deck:
    a_i = deck.index(JOKER_A)

    if a_i == DECK_LEN - 1:
        deck = deck[0:1] + [JOKER_A] + deck[1:-1]
    else:
        deck[a_i], deck[a_i + 1] = deck[a_i + 1], JOKER_A
    
    b_i = deck.index(JOKER_B)
    if b_i == DECK_LEN - 1:
        deck = deck[0:2] + [JOKER_B] + deck[2:-1]
    elif b_i == DECK_LEN - 2:
        deck = deck[0:1] + [JOKER_B] + deck[1:-2] + deck[-1:]
    else:
        deck[b_i], deck[b_i + 1], deck[b_i + 2] = deck[b_i + 1], deck[b_i + 2], JOKER_B

    return deck

def triple_cut(deck: Deck) -> Deck:
    a_i = deck.index(JOKER_A)
    b_i = deck.index(JOKER_B)
    first, second = a_i, b_i
    if a_i > b_i:
        first, second = b_i, a_i
    deck = deck[second + 1:] + deck[first:second + 1] + deck[:first]
    return deck

def count_cut(deck: Deck) -> Deck:
    bottom_val = min(53, deck[-1])
    deck = deck[bottom_val:-1] + deck[:bottom_val] + deck[-1:]
    return deck

def pipeline[T](arg: T, functions: Callable[[T], T]) -> T:
    for func in functions:
        arg = func(arg)
    return arg

def solitaire(deck: Deck) -> Iterator[int]:
    if len(deck) != DECK_LEN:
        raise InvalidSeedException
    
    cards = [x + 1 for x in range(54)]
    if any([card not in deck for card in cards]):
        raise InvalidSeedException

    while True:
        byte = 0
        i = 0
        while i < 8:
            deck = pipeline(deck, [joker_push, triple_cut, count_cut])

            top_val = min(53, deck[0])
            if deck[top_val] == JOKER_A or deck[top_val] == JOKER_B:
                continue
            output = deck[top_val] % 4
            
            byte = byte | (output << i)
            i += 2
        yield byte


M = 1204334797 * 9022686991

def blum_blum_shub(seed: int) -> Iterator[int]:
    if gcd(seed, M) != 1:
        raise InvalidSeedException
    
    x = seed
    while True:
        byte = 0
        for i in range(8):
            x = x ** 2 % M
            byte = byte | ((x % 2) << i)
        
        yield byte

