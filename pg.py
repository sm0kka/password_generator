#!/usr/bin/python3
import argparse
import random, sys
from functools import lru_cache


VERSION = '0.1.1'  # Last edit 01.04.2021

GLOBAL_VERBOSE = False


class PasswordGenerator(object):
    OPTION = {'d': '0123456789', # все инстансы класса видят это и могут менять, globals - зло!
        'l': 'abcdefghijklmnopqrstuvwxyz',
        'u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'p': '!#$%&()*+,-.:;<=>?@[]^_{}~',
        'v': 'aeiou'  # vowels
        }
    def __init__(self):
        self.passwords = []

    def temp_pass(self):
        # helper: tuple of tuples (amount, set_chars)
        helper = (
            (1, self.OPTION.get('u', '')), # get() чуть дороже, чем OPTION[key]
            (1, self.OPTION.get('v', '')), # зачем был str.join я не понял, он нужен
            (1, self.OPTION.get('l', '')), # для объединения iterable, а у тебя в 
            (5, self.OPTION.get('d', ''))  # tuple уже лежит строка
        )

        generated = ''.join(((random.choice(set_chars) for _ in range(number_of_chars)) for number_of_chars, set_chars in helper))
        self.passwords.append(generated) # тут тоже был лишний join

        if GLOBAL_VERBOSE:
            print('Generate temporary password like: Abc12345\n')

        return self.passwords

    # @lru_cache() # если оставить, то генерится только один пароль (типа вызов уже сделан)
    def generate(self, chars=14, manual=0, set_chars='dlu'):
        if all(False for i in set_chars if i in self.OPTION):
            print(f'ValueError: -s {set_chars}\nRun with default charset: "dlu"')
            # Default set of chars letters and digits
            set_chars = 'dlu'

        # Generate chars string
        chars_str = ''.join(self.OPTION.get(i, '') for i in set_chars if i in self.OPTION)

        if manual in range(1, len(chars_str)):
            chars_str = chars_str[:manual]  # Slice set

        if GLOBAL_VERBOSE:
            print(f'Current set({len(chars_str)}): {chars_str}\n')

        self.passwords.append(
            ''.join(random.choice(chars_str) for _ in range(chars))
            )
        return self.passwords

    def __repr__(self):
        len_of_passwords = len(self.passwords)
        if len_of_passwords > 1:
            result = [
                f'\t{index}\t{password}\n'
                for index, password in enumerate(self.passwords, 1)
            ]
            return ''.join(result)

        if len_of_passwords == 1:
            return '\t\t' + ''.join(self.passwords)

        return ""

    def __str__(self):
        return self.__repr__() ## Your repr was good.

def version():
    print(f'Password Generator {VERSION}')

@lru_cache()
def main():
    parser = argparse.ArgumentParser(prog='pg.py', description='Password generator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--chars", metavar='', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument("-a", "--amount", metavar='', type=int, default=1,
                        help='Amount of passwords')
    parser.add_argument("-m", "--manual", metavar='', type=int, default=0,
                        help='Manual slice set of chars')
    parser.add_argument("-s", "--set", type=str, default='dlu',
                        help=f'Charset for password generation'
                             f'(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help='Show set of chars before generation')
    parser.add_argument("-V", "--version", action='store_true',
                        help='Show version')
    parser.add_argument("-t", "--temporary", action='store_true',
                        help='Generate temporary password. Ignore all other settings except of -a. Example: Zyx51534', default=False)

    args = parser.parse_args()

    if args.version:
        version()
        sys.exit(0)

    global GLOBAL_VERBOSE 
    GLOBAL_VERBOSE = args.verbose
    
    password = PasswordGenerator()

    if args.temporary:
        password.temp_pass()

    for _ in range(args.amount):
        password.generate(args.chars, args.manual, args.set)

    return str(password) # раз уж у тебя есть __repr__


if __name__ == '__main__':
    print(main())

