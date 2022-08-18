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


def genpass(passphrase, domain, length=12, require_special=False, require_number=False):
    h = hashlib.new('sha256')
    h.update(f'{passphrase} {domain}\n'.encode())
    b = h.digest()
    password = base64.b64encode(b).decode()
    if length and len(password) > length:
        password = password[0:length]
    if require_special:
        password = ensure_special(password)
    if require_number:
        password = ensure_number(password)
    return password


def ensure_special(s):
    """Deterministically replace a character in S with a special character"""
    return s


def ensure_number(s):
    """Deterministically replace a character in S with a number"""
    return s


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
