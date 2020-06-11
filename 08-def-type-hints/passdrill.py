#!/usr/bin/env python3

"""passdrill: typing drills for practicing passphrases
"""

import sys
import os
from getpass import getpass
from hashlib import scrypt
from base64 import b64encode, b64decode

from typing import Sequence, Tuple

HASH_FILENAME = 'passdrill.hash'
HELP = 'Use -s to save passphrase hash for practice.'


def prompt() -> str:
    print('WARNING: the passphrase WILL BE SHOWN so that you can check it!')
    confirmed = ''
    while confirmed != 'y':
        passphrase = input('Type passphrase to hash (it will be echoed): ')
        if passphrase == '' or passphrase == 'q':
            print('ERROR: the passphrase cannot be empty or "q".')
            continue
        print(f'Passphrase to be hashed -> {passphrase}')
        confirmed = input('Confirm (y/n): ').lower()
    return passphrase


def crypto_hash(salt: bytes, passphrase: str) -> bytes:
    octets = passphrase.encode('utf-8')
    # Recommended parameters for interactive logins as of 2017:
    # N=32768, r=8 and p=1 (https://godoc.org/golang.org/x/crypto/scrypt)
    return scrypt(octets, salt=salt, n=32768, r=8, p=1, maxmem=2 ** 26)


def build_hash(passphrase: str) -> bytes:
    salt = os.urandom(32)
    payload = crypto_hash(salt, passphrase)
    return b64encode(salt) + b':' + b64encode(payload)


def save_hash() -> None:
    salted_hash = build_hash(prompt())
    with open(HASH_FILENAME, 'wb') as fp:
        fp.write(salted_hash)
    print(f'Passphrase hash saved to', HASH_FILENAME)


def load_hash() -> Tuple[bytes, bytes]:
    try:
        with open(HASH_FILENAME, 'rb') as fp:
            salted_hash = fp.read()
    except FileNotFoundError:
        print('ERROR: passphrase hash file not found.', HELP)
        sys.exit(2)

    salt, stored_hash = salted_hash.split(b':')
    return (b64decode(salt), b64decode(stored_hash))


def practice() -> None:
    salt, stored_hash = load_hash()
    print('Type q to end practice.')
    turn = 0
    correct = 0
    while True:
        turn += 1
        response = getpass(f'{turn}:')
        if response == '':
            print('Type q to quit.')
            turn -= 1  # don't count this response
            continue
        elif response == 'q':
            turn -= 1  # don't count this response
            break
        if crypto_hash(salt, response) == stored_hash:
            correct += 1
            answer = 'OK'
        else:
            answer = 'wrong'
        print(f'  {answer}\thits={correct}\tmisses={turn-correct}')

    if turn:
        pct = correct / turn * 100
        print(f'\n{turn} turns. {pct:0.1f}% correct.')


def main(argv: Sequence[str]) -> None:
    if len(argv) < 2:
        practice()
    elif len(argv) == 2 and argv[1] == '-s':
        save_hash()
    else:
        print('ERROR: invalid argument.', HELP)
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
