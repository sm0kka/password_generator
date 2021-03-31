#!/usr/bin/python3
import argparse
import random

OPTION = {
    'd': '0123456789',
    'l': 'abcdefghijklmnopqrstuvwxyz',
    'u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'p': '!#$%&()*+,-.:;<=>?@[]^_{}~',
    'v': 'aeiou'
}


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []

    def temp_pass(self, amount=1, verbose=False):
        # helper: tuple of tuples (amount, set_chars)
        helper = (
            (1, ''.join(OPTION.get('u', ''))),
            (1, ''.join(OPTION.get('v', ''))),  # vowels
            (1, ''.join(OPTION.get('l', ''))),
            (5, ''.join(OPTION.get('d', '')))
        )

        for _ in range(amount):
            generate = ''.join(
                ''.join(
                    set_chars[random.randrange(len(set_chars))]
                    for _ in range(number_of_chars)
                )
                for number_of_chars, set_chars in helper
            )
            self.passwords.append(''.join(generate))

        if verbose:
            print('Generate temporary password like: Abc12345\n')

        return self.passwords

    def generate(self, chars=14, amount=1, set_chars='dlu', manual=0, verbose=False, temporary=False):
        if temporary:
            return PasswordGenerator.temp_pass(self, amount, verbose)

        if all(False for i in set_chars if i in OPTION):
            print(f'ValueError: -s {set_chars}\nRun with default charset: "dlu"')
            # Default set of chars letters and digits
            set_chars = 'dlu'

        # Generate chars string
        chars_str = ''.join(OPTION.get(i, '') for i in set_chars if i in OPTION)

        if manual in range(1, len(chars_str)):
            chars_str = chars_str[:manual]  # Slice set

        if verbose:
            print(f'Sliced set({len(chars_str)}): {chars_str}\n')

        for _ in range(amount):
            self.passwords.append(
                ''.join(
                    chars_str[random.randrange(len(chars_str))] for _ in range(chars)
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
                        help=f'Charset for password generation'
                             f'(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)')
    parser.add_argument("-m", "--manual", metavar='', type=int, default=0,
                        help='Manual slice set of chars')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help='Show set of chars before generation')
    parser.add_argument("-t", "--temporary", action='store_true',
                        help='Generate temporary password. Ignore all other settings except of -a. Example: Zyx51534')

    args = parser.parse_args()

    password = PasswordGenerator()
    password.generate(args.chars, args.amount, args.set, args.manual, args.verbose, args.temporary)

    return password.__repr__()


if __name__ == '__main__':
    print(main())
