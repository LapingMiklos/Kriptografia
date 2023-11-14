from typing import Iterator

class InvalidSeedException(Exception):
    pass

JOKER_A = 53
JOKER_B = 54
DECK_LEN = 54

def solitaire(deck: list[int]) -> Iterator[int]:
    if len(deck) != DECK_LEN:
        raise InvalidSeedException
    
    if any([card < 1 or card > DECK_LEN for card in deck]):
        raise InvalidSeedException

    while True:
        byte = []
        while len(byte) < 8:
            # joker find and push
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

            # triple cut
            a_i = deck.index(JOKER_A)
            b_i = deck.index(JOKER_B)
            first, second = a_i, b_i # if a_i < b_i else b_i, a_i
            if a_i > b_i:
                first, second = b_i, a_i
            deck = deck[second + 1:] + deck[first:second + 1] + deck[:first]
            # count cut
            bottom_val = min(53, deck[-1])
            deck = deck[bottom_val:-1] + deck[:bottom_val] + deck[-1:]


            top_val = min(53, deck[0])
            if deck[top_val] == JOKER_A or deck[top_val] == JOKER_B:
                continue
            output = deck[top_val] % 4
            

            byte += [output % 2, output // 2 % 2]
        
        yield sum([bit * (2 ** i) for i, bit in enumerate(byte)])








        
        
