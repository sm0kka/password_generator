#!/usr/bin/env python
# New version of pg
import argparse
import re
from random import choices, shuffle
from string import ascii_lowercase, ascii_uppercase, digits


VERSION = '1.0.7'

LENGTH = 14
NUMBER = 1
KEYS = 'dul'

CHARSETS = {
    'd': digits,
    'l': ascii_lowercase,
    'u': ascii_uppercase,
    'p': '!$&(*.,+)-@^_?',
    'v': 'aeiou',
    't': '!/-?',
}


def get_charset(keys=KEYS):
    keys = [key for key in keys if key in CHARSETS]
    charset = []
    for key in keys:
        chars = CHARSETS.get(key)
        charset.extend(iter(chars))
    return charset


def get_password(charset=None, length=LENGTH):
    if not charset:
        charset = get_charset()
    return ''.join(choices(charset, k=length))
    # return ''.join([choice(charset) for _ in range(length)])


def get_multy_password(n=2, func=get_password, **kwargs):
    for _ in range(n):
        yield func(**kwargs)


def fixate(query):
    return tuple(re.findall(r"[^\W\d_]+|\d+", query)[:2])

def template_password(template=None):
    """
    Template password
    :param template:
    :return:
    """
    password = []
    if not template:
        template = ['1u', '1v', '1l', '5d']

    for i in template:
        amount, keys = fixate(i)
        charset = get_charset(keys=keys)
        password.append(get_password(charset=charset, length=int(amount)))

    return ''.join(password)


def secure_password(template=None):
    """
    Secure password generator
    :param template:
    :return:
    """
    if not template:
        template = ['12ul', '2d', '1p'] # old version template (12, 'ul'), (2, 'd'), (1, 'p')
    password = list(template_password(template=template))
    shuffle(password)
    return ''.join(password)

def show_version():
    print(''' 
     ____                ____                    _   ___  _____ 
    |  _ \ __ _ ___ ___ / ___| ___ _ __   __   _/ | / _ \|___  |
    | |_) / _` / __/ __| |  _ / _ \ '_ \  \ \ / / || | | |  / / 
    |  __/ (_| \__ \__ \ |_| |  __/ | | |  \ V /| || |_| | / /  
    |_|   \__,_|___/___/\____|\___|_| |_|   \_/ |_(_)___(_)_/   
    ''')
    print(f'Password generator version {VERSION}')
    return

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
        '--template',
        metavar='1u 1v 1l 5d',
        nargs='*',
        type=str,
        default='',
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
        '-t',
        '--temporary',
        action='store_true',
        help='Generate temporary password. Ignore all other settings except of -n. Example: Gik01103'
    )
    parser.add_argument(
        '-s',
        '--shuffle',
        action='store_true',
        help='Generate shuffle template password.'
    )
    return parser.parse_args()


def _show_passwords(func, number_of_passwords, **kwargs):
    # print(f'{number_of_passwords} {func.__name__} passwords: ')
    print('\n'.join(get_multy_password(n=number_of_passwords, func=func, **kwargs)))


def main():
    options = cli_parser() # Namespace(length=14, number=1, template='', charset='dlu', version=False, temporary=False, shuffle=False)
    # print(options)
    length = options.length
    number_of_passwords = options.number
    version = options.version
    temporary = options.temporary
    shuffle = options.shuffle
    template = options.template

    if version:
        show_version()
    elif temporary:
        _show_passwords(template_password, number_of_passwords)
    elif template:
        if shuffle:
            _show_passwords(secure_password, number_of_passwords, template=template)
        else:
            _show_passwords(template_password, number_of_passwords, template=template)
    elif shuffle:
        _show_passwords(secure_password, number_of_passwords)
    else:
        charset = get_charset(keys=options.charset)
        # print(f'{number_of_passwords}  {length}char passwords: ')
        _show_passwords(get_password, number_of_passwords, charset=charset, length=length)
        # print('\n'.join(get_multy_password(n=number_of_passwords, charset=charset, length=length)))

    return


if __name__ == "__main__":
    main()
