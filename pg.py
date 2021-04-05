#!/usr/bin/python3
import argparse
import random
from functools import lru_cache


VERSION = '0.1.3'  # Last edit 05.04.2021
OPTION = {
    'd': '0123456789',
    'l': 'abcdefghijklmnopqrstuvwxyz',
    'u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'p': '!#$%&()*+,-.:;<=>?@[]^_{}~',
    'v': 'aeiou'  # vowels
}


class PasswordGenerator(object):
    def __init__(self, **kwargs):
        """kwargs: chars, amount, manual, set_chars, verbose, temporary, version"""
        self.passwords = set()
        self.kwargs = kwargs

    def get_kwarg_value(self, name):
        return self.kwargs.get(name, '')

    def set_kwarg_value(self, name, value):
        self.kwargs[name] = value

    def temp_pass(self):
        # password_collector: tuple of tuples (int: amount, str: set_chars)
        password_collector = (
            (1, OPTION.get('u', '')),
            (1, OPTION.get('v', '')),
            (1, OPTION.get('l', '')),
            (5, OPTION.get('d', ''))
        )

        for _ in range(self.get_kwarg_value('amount')):
            generate = ''.join(
                ''.join(
                    random.choice(set_chars) for _ in range(number_of_chars)
                )
                for number_of_chars, set_chars in password_collector
            )
            self.passwords.add(''.join(generate))

        if self.get_kwarg_value('verbose'):
            self.set_kwarg_value('verbose_info', 'Generate temporary password like: Abc12345\n')

        return self.get_kwarg_value('passwords')

    @lru_cache()
    def get_password(self):
        if self.get_kwarg_value('version'):
            print(f'Password Generator {VERSION}')
            return

        if self.get_kwarg_value('temporary'):
            return PasswordGenerator.temp_pass(self)

        if all(False for i in self.get_kwarg_value('set_chars') if i in OPTION):
            set_chars = self.get_kwarg_value('set_chars')
            print(f'ValueError: unknown parameters "{set_chars}" in option -s \nRun with default charset: "dlu"')
            # Default set of chars letters and digits
            self.set_kwarg_value('set_chars', 'dlu')

        # Generate chars string
        chars_str = ''.join(OPTION.get(i, '') for i in self.get_kwarg_value('set_chars') if i in OPTION)

        if self.get_kwarg_value('manual') in range(1, len(chars_str)):
            chars_str = chars_str[:self.get_kwarg_value('manual')]  # Slice set

        if self.get_kwarg_value('verbose'):
            self.set_kwarg_value('verbose_info', f'Current set({len(chars_str)}): {chars_str}\n')

        for _ in range(self.get_kwarg_value('amount')):
            self.passwords.add(
                ''.join(
                    random.choice(chars_str) for _ in range(self.get_kwarg_value('chars'))
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
            return self.get_kwarg_value('verbose_info') + ''.join(result)

        if len_of_passwords == 1:
            return self.get_kwarg_value('verbose_info') + '\t\t' + ''.join(self.passwords)

        return ''


def cli_parser():
    parser = argparse.ArgumentParser(prog='pg.py', description='Password generator',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--chars', metavar='', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument('-a', '--amount', metavar='', type=int, default=1,
                        help='Amount of passwords')
    parser.add_argument('-m', '--manual', metavar='', type=int, default=0,
                        help='Manual slice set of chars')
    parser.add_argument('-s', '--set_chars', type=str, default='dlu',
                        help=f'Charset for password generation'
                             f'(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show set of chars before generation')
    parser.add_argument('-V', '--version', action='store_true',
                        help='Show version')
    parser.add_argument('-t', '--temporary', action='store_true',
                        help='Generate temporary password. Ignore all other settings except of -a. Example: Zyx51534')

    return parser.parse_args()


@lru_cache()
def main():
    password = PasswordGenerator(**vars(cli_parser()))
    password.get_password()
    return password


if __name__ == '__main__':
    print(main())
