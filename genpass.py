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
import json
from typing import Optional, NamedTuple

SPECIAL = r'@#*(){}+=/?~;,.-_'
DIGIT = r'0123456789'
LOWER = r'abcdefghijklmnopqrstuvwxyz'
UPPER = LOWER.upper()
PREFS_FILE = ".genpass"
DEFAULT_LENGTH = 12


class Requires(NamedTuple):
    length: float = DEFAULT_LENGTH
    digit: bool = False
    special: bool = False
    upper: bool = False
    lower: bool = False

    @classmethod
    def from_args(cls, args):
        return Requires(length=args.length, digit=args.digit, special=args.special, upper=args.upper, lower=args.lower)

    def is_default(self):
        return self == Requires()

    def trim(self, word):
        if 0 < self.length < len(word):
            word = word[0:self.length]
        return word

    def charsets(self):
        charsets = list()  # Use list because order must be deterministic
        if self.special:
            charsets.append(SPECIAL)
        if self.digit:
            charsets.append(DIGIT)
        if self.upper:
            charsets.append(UPPER)
        if self.lower:
            charsets.append(LOWER)
        return charsets

    def meets_all(self, word):
        return all(has(charset, word) for charset in self.charsets())


def main():
    parser = argparse.ArgumentParser(description='Generate a password')
    parser.add_argument('domain', metavar='domain', type=str,
                        help='The domain for which to generate a password')
    parser.add_argument('-s', dest='special', action='store_const',
                        const=True, default=False,
                        help='Require a special character in the output')
    parser.add_argument('-d', dest='digit', action='store_const',
                        const=True, default=False,
                        help='Require a digit in the output')
    parser.add_argument('-u', dest='upper', action='store_const',
                        const=True, default=False,
                        help='Require an upper case in the output')
    parser.add_argument('-l', dest='lower', action='store_const',
                        const=True, default=False,
                        help='Require an upper case in the output')
    parser.add_argument('-L', dest='length', type=int, default=DEFAULT_LENGTH)

    args = parser.parse_args()
    passphrase = getpass.getpass("Passphrase: ")

    requires = Requires.from_args(args)
    if requires.is_default():
        if saved := load(args.domain):
            requires = saved
    else:
        save(args.domain, requires)
    password = genpass(passphrase, args.domain, requires)
    print(password)


def load(domain) -> Optional[Requires]:
    try:
        with open(PREFS_FILE, 'r') as file:
            all_domains = json.load(file)
    except FileNotFoundError:
        all_domains = {}

    if domain in all_domains:
        requires = Requires._make(all_domains[domain])
        print(f'Loaded prefs for {domain} from {PREFS_FILE}: {requires}')
        return requires

    return None


def save(domain, requires):
    print(f'Saving prefs for {domain} to {PREFS_FILE}')
    try:
        with open(PREFS_FILE, 'r') as file:
            all_domains = json.load(file)
    except FileNotFoundError:
        all_domains = {}

    all_domains[domain] = requires

    try:
        with open(PREFS_FILE, 'w') as file:
            json.dump(all_domains, file)
    except IOError as err:
        print(f'Unable to save prefs for {domain} in {PREFS_FILE}: {err}')


def genpass(passphrase, domain, requires):
    password = base64.b64encode(sha256(f'{passphrase} {domain}\n')).decode()
    password = requires.trim(password)
    # Loop because if length is to be maintained, then overwriting can clobber a required character
    charsets = requires.charsets()
    while not requires.meets_all(password):
        for charset in requires.charsets():
            password = ensure(charset, password)
    return password


def sha256(s):
    h = hashlib.new('sha256')
    h.update(s.encode())
    return h.digest()


def has(charset, password):
    return any(elem in password for elem in charset)


def ensure(charset, password):
    """Deterministically replace a character in S with a special character"""
    prand = int.from_bytes(sha256(f'salt for {charset} {password}'), 'big')  # pseudo-random based on hash of password
    chars = list(password)
    chars[prand % len(chars)] = charset[prand % len(charset)]
    return ''.join(chars)


if __name__ == "__main__":
    main()
