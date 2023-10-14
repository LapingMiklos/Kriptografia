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
from utils import vigenere_add, vigenere_subtract, InvalidKeyException
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

# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if len(keyword) == 0:
        raise InvalidKeyException
    return ''.join([vigenere_add(char, keyword[index % len(keyword)]) for index, char in enumerate(plaintext)])

print(encrypt_vigenere('ATTACKATDAWN', 'LEMON'))

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if len(keyword) == 0:
        raise InvalidKeyException
    return ''.join([vigenere_subtract(char, keyword[index % len(keyword)]) for index, char in enumerate(ciphertext)])

print(decrypt_vigenere('LXFOPVEFRNHR', 'LEMON'))

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

asd = encrypt_scytale('0123456789012', 5)
print(asd)
print(decrypt_scytale(asd, 5))

"""
0    5    0
 1    6
  2    7
   3    8
    4    9
"""