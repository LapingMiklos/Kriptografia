#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
from utils import vigenere_add, vigenere_subtract, vigenere_add_bytes, vigenere_subtract_bytes, InvalidKeyException
from math import ceil

# Caesar Cipher

CAESAR_KEY: int = 3
ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt_caesar(plaintext: str) -> str:
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    cipher: dict[str, str] = {letter: ALPHABET[(index + CAESAR_KEY) % len(ALPHABET)] for index, letter in enumerate(ALPHABET)}
    return ''.join([cipher.get(char, char) for char in plaintext])

def decrypt_caesar(ciphertext: str) -> str:
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    decipher: dict[str, str] = {letter: ALPHABET[(index - CAESAR_KEY) % len(ALPHABET)] for index, letter in enumerate(ALPHABET)}
    return ''.join([decipher.get(char, char) for char in ciphertext])

def encrypt_bytes_caesar(plainbytes: bytes) -> bytes:
    return bytes([(byte + CAESAR_KEY) % 256 for byte in plainbytes])

def decrypt_bytes_caesar(cipherbytes: bytes) -> bytes:
    return bytes([(byte - CAESAR_KEY) % 256 for byte in cipherbytes])

# Vigenere Cipher

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if len(keyword) == 0:
        raise InvalidKeyException
    
    return ''.join([vigenere_add(char, keyword[index % len(keyword)]) for index, char in enumerate(plaintext)])

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if len(keyword) == 0:
        raise InvalidKeyException
    
    return ''.join([vigenere_subtract(char, keyword[index % len(keyword)]) for index, char in enumerate(ciphertext)])

def encrypt_bytes_vigenere(plainbytes: bytes, keyword: bytes) -> bytes:
    if len(keyword) == 0:
        raise InvalidKeyException
    
    return bytes([vigenere_add_bytes(byte, keyword[index % len(keyword)]) for index, byte in enumerate(plainbytes)])

def decrypt_bytes_vigenere(cipherbytes: bytes, keyword: bytes) -> bytes:
    if len(keyword) == 0:
        raise InvalidKeyException
    
    return bytes([vigenere_subtract_bytes(byte, keyword[index % len(keyword)]) for index, byte in enumerate(cipherbytes)])

# Scytale cipher

def encrypt_scytale(plaintext: str, circumference: int) -> str:
    if circumference < 1:
        raise InvalidKeyException
    
    return ''.join([plaintext[start_i::circumference] for start_i in range(circumference)])

def decrypt_scytale(ciphertext: str, circumference: int) -> str:
    if circumference < 1:
        raise InvalidKeyException
    
    step = ceil(len(ciphertext) / circumference)
    extra_char_count = len(ciphertext) % circumference
    if extra_char_count == 0:
        return ''.join([ciphertext[start_i::step] for start_i in range(step)])
    
    step_len_separation = step * extra_char_count
    left, right = ciphertext[:step_len_separation], ciphertext[step_len_separation:]

    return ''.join([left[start_i::step] + right[start_i::(step - 1)] for start_i in range(step - 1)]) + left[step - 1::step]

# Railfence cipher

def encrypt_railfence(plaintext: str, num_rails: int) -> str:
    if num_rails < 1:
        raise InvalidKeyException
    
    rails = ['' for _ in range(num_rails)]
    current_rail = 0
    inc = 1
    for char in plaintext:
        rails[current_rail] += char
        current_rail += inc
        if current_rail == 0:
            inc = 1
        elif current_rail == num_rails - 1:
            inc = -1
    return ''.join(rails)

def decrypt_railfence(ciphertext: str, num_rails: int) -> str:
    if num_rails < 1:
        raise InvalidKeyException
    
    char_counts = [0 for _ in range(num_rails)]
    current_rail = 0
    inc = 1
    for _ in ciphertext:
        char_counts[current_rail] += 1
        current_rail += inc
        if current_rail == 0:
            inc = 1
        elif current_rail == num_rails - 1:
            inc = -1
    
    rails: list[list[int]] = []
    sum = 0
    for char_count in char_counts:
        prev_sum = sum
        sum += char_count
        rails.append(list(range(prev_sum, sum)))

    plaintext = ''
    current_rail = 0
    inc = 1
    for _ in ciphertext:
        plaintext += ciphertext[rails[current_rail].pop(0)]
        current_rail += inc
        if current_rail == 0:
            inc = 1
        elif current_rail == num_rails - 1:
            inc = -1
    
    return plaintext