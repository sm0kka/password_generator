#!/usr/bin/env python
import argparse
from dataclasses import dataclass, asdict
from secrets import choice
from string import digits, ascii_uppercase, ascii_lowercase

VERSION = '0.1.5'

CHAR_SETS = {
    'd': digits,
    'l': ascii_lowercase,
    'u': ascii_uppercase,
    'p': '!$&(*.,+)-@^_?',
    'v': 'aeiou',  # vowels
    't': '!/-?'  # token punctuations
}


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@dataclass
class Password:
    value: str = ''

    def __repr__(self):
        return f"{self.value}"


@dataclass
class Options:
    char_set: str = 'dul'
    amount: int = 1
    lenght: int = 14
    temporary: bool = False
    version: bool = False

    def __repr__(self):
        return f'{self.char_set=} {self.amount=} ' \
               f'{self.lenght=} ' \
               f'{self.temporary=} {self.version=}'

    def __add__(self, other):
        res = {**self.__dict__, **other.__dict__}
        return Options(**res)


@singleton
class Generator:
    def __init__(self):
        self.options = Options()

    def set_opts(self, options: Options | dict) -> None:
        res = {**self.options.__dict__, **self.set_options(options).__dict__}
        self.options = Options(**res)

    def get_passwd(self) -> list[Password()]:
        gen_function = self.temporary_passwd if self.options.temporary else self._generate_passwd

        if self.options.amount >= 1:
            return [gen_function() for _ in range(self.options.amount)]
        else:
            print('Amount could be >= 1')

    def _generate_passwd(self) -> Password():
        char_set = ''.join([
            CHAR_SETS.get(option) for option in self.options.char_set
            if option in CHAR_SETS
        ])
        lenght = self.options.lenght
        password = [choice(char_set) for _ in range(lenght)]
        return Password(''.join(password))

    def set_options(self, options: Options | dict) -> Options:
        so = self.options
        if isinstance(options, Options):
            return so + options
        elif isinstance(options, dict):
            tmp = so.__dict__ | options
            return Options(**tmp)
        else:
            raise ValueError('Invalid options')

    @staticmethod
    def temporary_passwd() -> Password:
        password_collector = (1, 'u'), (1, 'v'), (1, 'l'), (5, 'd')
        res = []
        for amount, char_set in password_collector:
            for _ in range(amount):
                res.append(choice(CHAR_SETS[char_set]))
        password = ''.join(res)
        return Password(password)


def print_pass(passwords: list[Password]) -> None:
    if passwords:
        for i, password in enumerate(passwords, 1):
            print(f'{i}\t{password}')


def main() -> None:
    opts = Options(**vars(cli_parser()))

    if opts.version:
        return print(f'Password Generator ver.{VERSION}')

    passwd = Generator()
    # ss = Options(amount=13, char_set='dt', lenght=128)
    # s = passwd.options
    # z = s + ss
    # print(z)
    # passwd.set_opts(z)
    passwd.set_opts(opts)

    print_pass(passwd.get_passwd())
    return


def cli_parser():
    parser = argparse.ArgumentParser(
        prog='pg.py', description='Password generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-l',
        '--lenght',
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
    # parser.add_argument('-m', '--manual', metavar='', type=int, default=0,
    #                     help='Manual slice set of chars')
    parser.add_argument(
        '-c',
        '--char_set',
        type=str,
        default='dlu',
        help='Charset for password generation(d: digits, l: lowercase letters, u: uppercase letters, p: punctuation)',
    )
    # parser.add_argument('-v', '--verbose', action='store_true',
    #                     help='Show set of chars before generation')
    parser.add_argument(
        '-V',
        '--version',
        action='store_true',
        help='Show version'
    )
    parser.add_argument(
        '-t',
        '--temporary',
        action='store_true',
        help='Generate temporary password. Ignore all other settings except of -a. Example: Gik01103'
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
