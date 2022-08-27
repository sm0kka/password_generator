#!/usr/bin/env python
import argparse
from dataclasses import dataclass, asdict
from secrets import choice
from string import digits, ascii_uppercase, ascii_lowercase

VERSION = '0.1.5'


@dataclass(frozen=True, slots=True)
class CharSets:
    d: str = digits
    l: str = ascii_lowercase
    u: str = ascii_uppercase
    p: str = '!$&(*.,+)-@^_?'
    v: str = 'aeiou'  # vowels
    t: str = '!/-?'  # token punctuations

    def slots(self):
        return self.__slots__


@dataclass(slots=True, frozen=True)
class Password:
    value: str = ''

    def __repr__(self):
        return f"{self.value}"


@dataclass(slots=True, kw_only=True, match_args=True)
class Options:
    char_set: str = 'dul'
    amount: int = 1
    length: int = 14
    temporary: bool = False
    version: bool = False


class Generator:
    def __init__(self):
        self.options = Options()

    def set_opts(self, options: Options) -> None:
        if isinstance(options, Options):
            self.options = options
        else:
            raise ValueError('Invalid options')

    def get_passwd(self) -> list[Password()]:
        gen_function = self._temporary_passwd if self.options.temporary else self._generate_passwd

        if self.options.amount >= 1:
            return [gen_function() for _ in range(self.options.amount)]
        else:
            print('Amount could be >= 1')

    def _generate_passwd(self) -> Password():
        chrset = CharSets()
        kit_chrset = ''.join([
            getattr(chrset, option) for option in self.options.char_set
            if option in chrset.slots()
        ])
        lenght = self.options.length
        password = [choice(kit_chrset) for _ in range(lenght)]
        return Password(''.join(password))

    @staticmethod
    def _temporary_passwd() -> Password:
        password_collector = (1, 'u'), (1, 'v'), (1, 'l'), (5, 'd')
        res = []
        for amount, char_set in password_collector:
            for _ in range(amount):
                res.append(choice(getattr(CharSets(), char_set)))
        password = ''.join(res)
        return Password(password)


def print_passwd(passwords: list[Password]) -> None:
    if passwords:
        for i, password in enumerate(passwords, 1):
            print(f'{i}\t{password}')


def test():
    ps = Generator()
    print(ps.options)
    opt = Options(char_set='dut', amount=10, length=128)
    ps.set_opts(opt)
    print(ps.options)
    print_passwd(ps.get_passwd())


def main() -> None:
    opts = Options(**vars(cli_parser()))

    if opts.version:
        return print(f'Password Generator ver.{VERSION}')

    pg = Generator()

    pg.set_opts(opts)

    print_passwd(pg.get_passwd())
    return


def cli_parser():
    parser = argparse.ArgumentParser(
        prog='pg.py', description='Password generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-l',
        '--length',
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
