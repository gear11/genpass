#!/usr/bin/env python3
"""
Command line tool for generating passwords
"""
__author__ = "Andy Jenkins"
__license__ = "Apache 2.0"

import argparse
import getpass
import hashlib
import base64


SPECIAL = r'@#*(){}+=/?~;,.-_'
DIGITS = r'0123456789'


def genpass(passphrase, domain, length=12, require_special=False, require_number=False):
    h = hash(f'{passphrase} {domain}\n')
    password = base64.b64encode(h).decode()
    if length and len(password) > length:
        password = password[0:length]
    # Loop because if length is to be maintained, then overwriting can clobber a required character
    while (require_special and not has_special(password)) or (require_number and not has_digit(password)):
        print(f'Password is now {password}')
        if require_special and not has_special(password):
            password = ensure_special(password)
        if require_number and not has_digit(password):
            password = ensure_digit(password)
    return password


def hash(s):
    h = hashlib.new('sha256')
    h.update(s.encode())
    return h.digest()


def has_digit(password):
    return any(elem in password for elem in DIGITS)


def has_special(password):
    return any(elem in password for elem in SPECIAL)


def ensure_special(password):
    """Deterministically replace a character in S with a special character"""
    print("Ensure special")
    prand = int.from_bytes(hash(f'salt for special {password}'), 'big')  # pseudo-random based on hash of password
    chars = list(password)
    chars[prand % len(chars)] = SPECIAL[prand % len(SPECIAL)]
    return ''.join(chars)


def ensure_digit(password):
    """Deterministically replace a character in S with a digit"""
    print("Ensure digit")
    prand = int.from_bytes(hash(f'salt for digit {password}'), 'big')  # pseudo-random based on hash of password
    chars = list(password)
    chars[prand % len(chars)] = DIGITS[prand % len(DIGITS)]
    return ''.join(chars)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a password')
    parser.add_argument('domain', metavar='domain', type=str,
                        help='The domain for which to generate a password')
    parser.add_argument('-s', dest='require_special', action='store_const',
                        const=True, default=False,
                        help='Require a special character in the output')
    parser.add_argument('-n', dest='require_number', action='store_const',
                        const=True, default=False,
                        help='Require a number in the output')
    parser.add_argument('-l', dest='length', type=int, default=12)

    args = parser.parse_args()
    the_passphrase = getpass.getpass("Passphrase: ")
    the_password = genpass(the_passphrase, args.domain, args.length, args.require_special, args.require_number)
    print(the_password)
