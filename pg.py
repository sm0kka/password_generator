#!/usr/bin/python3
import random
import string as st
import argparse


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []


    def generate(self, chars=14, amount=1):
        for _ in range(amount):
            self.passwords.append(
                ''.join(
                    random.choice(st.ascii_letters + st.digits) for _ in range(chars)
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
            return ''.join(self.passwords)

        return "Error: [-a / --amount] equals 0 is too low value try -a 1 or more"

def main():
    parser = argparse.ArgumentParser(prog='pg.py', description='Generate ASCII passwords',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--chars", metavar='C', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument("-a", "--amount", metavar='A', type=int, default=1,
                        help='Amount of passwords')

    args = parser.parse_args()

    password = PasswordGenerator()
    password.generate(args.chars, args.amount)

    return password.__repr__()


if __name__ == '__main__':
    print(main())