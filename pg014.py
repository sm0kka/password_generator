#!/usr/bin/python3
import argparse
from secrets import choice
import string
from functools import lru_cache
import logging


VERSION = '0.1.4'  # Last edit 10.04.2021
logging.basicConfig(level=logging.INFO, format='%(message)s')
OPTION = {
    'd': string.digits,
    'l': string.ascii_lowercase,
    'u': string.ascii_uppercase,
    'p': string.punctuation,
    'v': 'aeiou'  # vowels
}


class PasswordGenerator:
    def __init__(self, **kwargs):
        """kwargs: chars, amount, manual, set_chars, verbose, temporary, version"""
        self.passwords = set()
        self._kwargs = kwargs

    @property
    def kwargs(self):
        return self._kwargs

    def temp_pass(self):
        # password_collector: tuple of tuples (int: amount, str: set_chars)
        password_collector = (
            (1, OPTION['u']),
            (1, OPTION['v']),
            (1, OPTION['l']),
            (5, OPTION['d'])
        )

        for _ in range(self.kwargs['amount']):
            generate = ''.join(
                ''.join(
                    choice(set_chars) for _ in range(number_of_chars)
                )
                for number_of_chars, set_chars in password_collector
            )
            self.passwords.add(''.join(generate))
        if self.kwargs['verbose']:
            logging.info('Generate temporary password like: Gik01103')

        return self.passwords

    @lru_cache()
    def get_password(self):
        if self.kwargs['version']:
            logging.info(f'Password Generator {VERSION}')
            return

        if self.kwargs['temporary']:
            return PasswordGenerator.temp_pass(self)

        if all(False for i in self.kwargs['set_chars'] if i in OPTION):
            set_chars = self.kwargs['set_chars']
            logging.error(f'ValueError: unknown parameters "{set_chars}" in option -s'
                          f'\nRun with default charset: "dlu"')
            # Default set of chars letters and digits
            self.kwargs['set_chars'] = 'dlu'

        # Generate chars string
        chars_str = ''.join(OPTION.get(i, '')
                            for i in self.kwargs['set_chars'] if i in OPTION)

        if self.kwargs['manual'] in range(1, len(chars_str)):
            chars_str = chars_str[:self.kwargs['manual']]  # Slice set

        if self.kwargs['verbose']:
            logging.info(f'Current set({len(chars_str)}): {chars_str}')

        for _ in range(self.kwargs['amount']):
            self.passwords.add(
                ''.join(
                    choice(chars_str) for _ in range(self.kwargs['chars'])
                )
            )
        return self.passwords

    def generated_passwords(self):
        if self.kwargs['amount'] > 1:
            result = [
                f'\t{index}\t{password}\n'
                for index, password in enumerate(self.passwords, 1)
            ]
            return ''.join(result)

        return '\t\t' + ''.join(self.passwords)


def cli_parser():
    parser = argparse.ArgumentParser(
        prog='pg.py', description='Password generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-c',
        '--chars',
        metavar='',
        type=int,
        default=14,
        help='Length of password in characters'
    )
    parser.add_argument(
        '-a',
        '--amount',
        metavar='',
        type=int,
        default=1,
        help='Amount of passwords'
    )
    parser.add_argument(
        '-m',
        '--manual',
        metavar='',
        type=int,
        default=0,
        help='Manual slice set of chars'
    )
    parser.add_argument(
        '-s',
        '--set_chars',
        type=str,
        default='dlu',
        help='Charset for password generation(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Show set of chars before generation'
    )
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='Show version'
    )
    parser.add_argument(
        '-t', '--temporary', action='store_true',
        help='Generate temporary password. Ignore all other settings except of -a. Example: Gik01103'
    )

    return parser.parse_args()


@lru_cache()
def main():
    password = PasswordGenerator(**vars(cli_parser()))
    # logging.info(f'kwargs: {password.kwargs}')
    password.get_password()
    return password.generated_passwords()


if __name__ == '__main__':
    print(main())
