#!/usr/bin/python3
import argparse
import random
import string as st


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []

    def generate(self, chars=14, amount=1, charset='l'):

        option = {'d': 10, 'l': 62, 'p': 94}

        # Default set of chars letters and digits
        # '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        set_of_chars = st.printable[:94]

        if charset not in option:
            set_of_chars = set_of_chars[:option['l']]

        else:
            set_of_chars = set_of_chars[:option[charset]]

        chars_dict = {k: v for k, v in enumerate(set_of_chars)}
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

        return "Error: [-a / --amount] equals 0 is too low value try -a 1 or more"


def main():
    parser = argparse.ArgumentParser(prog='pg.py', description='Generate ASCII passwords',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--chars", metavar='', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument("-a", "--amount", metavar='', type=int, default=1,
                        help='Amount of passwords')
    parser.add_argument("-cs", "--charset", type=str, default='l',
                        help=f'Charset for password generation (d(digits), l(letters), p(punctuation)')

    args = parser.parse_args()

    password = PasswordGenerator()
    password.generate(args.chars, args.amount, args.charset)

    return password.__repr__()


if __name__ == '__main__':
    print(main())
