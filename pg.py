#!/usr/bin/python3
import argparse
import random


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []

    def generate(self, chars=14, amount=1, set_chars='dlu'):

        option = {
            'd': '0123456789',
            'l': 'abcdefghijklmnopqrstuvwxyz',
            'u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'p': '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        }

        if all(False for i in set_chars if i in option):
            print(f'ValueError: -s {set_chars}\nRun with default charset: "dlu"')
            # Default set of chars letters and digits
            set_chars = 'dlu'

        set_chars = ''.join(option.get(i, '') for i in set_chars if i in option)

        chars_dict = {k: v for k, v in enumerate(set_chars)}
        for _ in range(amount):
            self.passwords.append(
                ''.join(
                    chars_dict[random.randrange(len(chars_dict))] for _ in range(chars)
                )
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

        return "ValueError: [-a / --amount] less 1"


def main():
    parser = argparse.ArgumentParser(prog='pg.py', description='Password generator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--chars", metavar='', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument("-a", "--amount", metavar='', type=int, default=1,
                        help='Amount of passwords')
    parser.add_argument("-s", "--set", type=str, default='dlu',
                        help=f'Charset for password generation '
                             f'(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)')

    args = parser.parse_args()

    password = PasswordGenerator()
    password.generate(args.chars, args.amount, args.set)

    return password.__repr__()


if __name__ == '__main__':
    print(main())
