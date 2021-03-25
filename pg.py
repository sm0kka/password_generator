#!/usr/bin/python3
import argparse
import random
import string as st


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []

    def generate(self, chars=14, amount=1, punctuation=False):
        option = {'letters': st.ascii_letters, 'digits': st.digits, 'punctuation': st.punctuation}
        # Default set of chars letters and digits
        set_of_chars = option['letters'] + option['digits']

        if punctuation:
            set_of_chars += option['punctuation']

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
    parser.add_argument("-p", "--punctuation", action='store_true',
                        help=f'Add punctuation in letters and digits charset for password generation')

    args = parser.parse_args()

    password = PasswordGenerator()
    password.generate(args.chars, args.amount, args.punctuation)

    return password.__repr__()


if __name__ == '__main__':
    print(main())

