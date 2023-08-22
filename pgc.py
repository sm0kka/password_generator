#!/usr/bin/env python
# New version of pg
import argparse
import random
from dataclasses import dataclass
import re
from random import choices, shuffle
from string import ascii_lowercase, ascii_uppercase, digits

# Default values
VERSION = '1.0.8'
LENGTH = 14
NUMBER = 1
KEYS = 'dul'
TEMPLATE = ['1u', '1v', '1l', '5d']

CHARSETS = {
    'd': digits,
    'l': ascii_lowercase,
    'u': ascii_uppercase,
    'p': '!$&(*.,+)-@^_?',
    'v': 'aeiou',
    't': '!/-?',
}

@dataclass
class Options:
        length: int
        number: int
        template: list
        charset: str
        version: bool
        # temporary: bool
        shuffle: bool

@dataclass
class Password:
    value: str = ''

    def __str__(self):
        return self.value


def shuffle_password(password: Password):
    if password and isinstance(password, Password):
        list_pass = list(password.value)
        random.shuffle(list_pass)
        return Password(''.join(list_pass))
    else:
        raise ValueError


def get_charset(keys=KEYS):
    keys = [key for key in keys if key in CHARSETS]
    charset = []
    for key in keys:
        chars = CHARSETS.get(key)
        charset.extend(iter(chars))
    return charset

def template_parser(template):
    return tuple(re.findall(r"[^\W\d_]+|\d+", template)[:2])

def cli_parser():
    parser = argparse.ArgumentParser(
        prog='pgc.py', description='Password generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-l',
        '--length',
        metavar='',
        type=int,
        default=LENGTH,
        help='Length of password in characters'
    )
    parser.add_argument(
        '-n',
        '--number',
        metavar='',
        type=int,
        default=NUMBER,
        help='Number of passwords'
    )
    parser.add_argument(
        '-t',
        '--template',
        metavar='1u 1v 1l 5d',
        nargs='*',
        type=str,
        # default=TEMPLATE,
        action='store',
        help='Template for generation, with -s arg shuffle final password',
    )
    parser.add_argument(
        '-c',
        '--charset',
        type=str,
        default=KEYS,
        help='Charset for password generation(d: digits, l: lowercase letters,u: uppercase letters, p: punctuation, v: vowels)',
    )
    parser.add_argument(
        '-V',
        '--version',
        action='store_true',
        help='Show version'
    )
    parser.add_argument(
        '-s',
        '--shuffle',
        action='store_true',
        help='Finally shuffle template password.'
    )
    return Options(**vars(parser.parse_args()))

def get_password(options: Options) -> Password:
    return Password("".join(random.choices(get_charset(keys=options.charset), k=options.length)))

def get_char(amount=1, keys=None):
    if keys:
        return "".join(random.choices(get_charset(keys=keys), k=amount))

def version():
    return f'Password generator version {VERSION}'

def template_password(options):
    password = []
    if not options.template or options.template == []:
        options.template = TEMPLATE

    for i in options.template:
        amount, keys = template_parser(i)
        password.append(str(get_char(int(amount), keys)))
    # print(password)
    return Password(''.join(password))

def main():
        options = cli_parser()
        # options.shuffle = True
        # options.version = True
        # options.temporary = True
        # print(options)
        result = Password()

        if options.version:
            print(version())
            exit()

        for _ in range(options.number):

            if options.template == []:
                options.template = TEMPLATE

                result = template_password(options)
            elif options.template:
                result = template_password(options)
            else:

                result = get_password(options)


            if options.shuffle and isinstance(result, Password):
                result = shuffle_password(result)


            print(result)


if __name__ == '__main__':
    main()