#!/usr/bin/env python3 -tt
"""
File: crypto-console.py
-----------------------
Implements a console menu to interact with the cryptography functions exported
by the crypto module.

If you are a student, you shouldn't need to change anything in this file.
"""
import random

from crypto import (encrypt_caesar, decrypt_caesar,
                    encrypt_bytes_caesar, decrypt_bytes_caesar,
                    encrypt_vigenere, decrypt_vigenere,
                    encrypt_bytes_vigenere, decrypt_bytes_vigenere,
                    encrypt_scytale, decrypt_scytale,
                    encrypt_bytes_scytale, decrypt_bytes_scytale,
                    encrypt_railfence, decrypt_railfence,
                    encrypt_bytes_railfence, decrypt_bytes_railfence)

from utils import InvalidCharException


#############################
# GENERAL CONSOLE UTILITIES #
#############################

def get_tool():
    print("* Tool *")
    return _get_selection("(C)aesar, (V)igenere, (S)cytale or (R)ailfence? ", "CVSR")


def get_action():
    """Return true iff encrypt"""
    print("* Action *")
    return _get_selection("(E)ncrypt or (D)ecrypt? ", "ED")


def get_filename():
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename


def get_input(binary=False):
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_yes_or_no(prompt, reprompt=None):
    """
    Asks the user whether they would like to continue.
    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def get_int_bigger_than_one(prompt: str) -> int:
    while True:
        try:
            value = int(input(f"{prompt}? "))
            if value > 1:
                return value
        except ValueError:
            pass
        print("Value must be bigger than 1")


def clean_caesar(text):
    """Convert text to a form compatible with the preconditions imposed by Caesar cipher"""
    return text.upper()


def clean_vigenere(text):
    return ''.join(ch for ch in text.upper() if ch.isupper())

def is_valid(data: str):
    return all([ch.isupper() for ch in data])


def run_caesar():
    action = get_action()
    encrypting = action == 'E'
    binary = get_yes_or_no('Binary?')
    while True:
        data = get_input(binary)
        if binary or is_valid(data):
            break
        print("Input was invalid")

    print("* Transform *")
    print("{}crypting {} using Caesar cipher...".format('En' if encrypting else 'De', data))

    if binary:
        output = (encrypt_bytes_caesar if encrypting else decrypt_bytes_caesar)(data)
    else:
        output = (encrypt_caesar if encrypting else decrypt_caesar)(data)

    set_output(output, binary)


def run_vigenere():
    action = get_action()
    encrypting = action == 'E'

    while True:
        data = get_input(binary=False)
        if is_valid(data):
            break
        print("Input was invalid")

    print("* Keyword *")
    while True:
        keyword = get_input(binary=False)
        if is_valid(keyword):
            break
        print("Input was invalid")

    print("{}crypting {} using Vigenere cipher and keyword {}...".format('En' if encrypting else 'De', data, keyword))

    output = (encrypt_vigenere if encrypting else decrypt_vigenere)(data, keyword)

    set_output(output)


def run_scytale():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=False)

    print("* Transform *")
    circumference = get_int_bigger_than_one("Circumference")

    print("{}crypting {} using Scytale cipher and circumference {}...".format('En' if encrypting else 'De', data, circumference))

    output = (encrypt_scytale if encrypting else decrypt_scytale)(data, circumference)

    set_output(output)

def run_railfence():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=False)

    print("* Transform *")
    rails = get_int_bigger_than_one("Rails")

    print("{}crypting {} using Railfence cipher and circumference {}...".format('En' if encrypting else 'De', data, rails))

    output = (encrypt_railfence if encrypting else decrypt_railfence)(data, rails)

    set_output(output)

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print('-' * 34)
    tool = get_tool()
    # This isn't the cleanest way to implement functional control flow,
    # but I thought it was too cool to not sneak in here!
    commands = {
        'C': run_caesar,         # Caesar Cipher
        'V': run_vigenere,       # Vigenere Cipher
        'S': run_scytale,        # Scytale
        'R': run_railfence,      # Railfence
    }
    commands[tool]()


def main():
    """Harness for CS41 Assignment 1"""
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while get_yes_or_no("Again?"):
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    main()
