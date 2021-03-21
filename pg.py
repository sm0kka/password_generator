#!/usr/bin/python3
import random
import string as st
import argparse


class PasswordGenerator(object):
    def __init__(self):
        self.passwords = []

    def generate(self, chars=14, amount=1):
        if amount == 0:
            return self.passwords

        self.passwords.append(
            ''.join(
                random.choice(st.ascii_letters + st.digits) for _ in range(chars)
            )
        )

        return self.generate(chars, amount - 1)

    def __repr__(self):
        result = [
            f'\t{index if len(self.passwords) > 1 else ""}\t{password}\n'
            for index, password in enumerate(self.passwords, 1)
        ]

        return ''.join(result)


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
