#!/usr/bin/python
import random
import string as st
import argparse


class Password(object):
    def __init__(self):
        self.result = []

    def generate(self, chars=14, amount=1):
        if amount == 0:
            return self.result

        self.result.append(''.join([random.choice(st.ascii_letters + st.digits) for _ in range(chars)]))

        return self.generate(chars, amount - 1)

    def __repr__(self):
        result = []
        for index, password in enumerate(self.result, 1):
            result.append(f'\t{index if len(self.result) > 1 else ""}\t{password}\n')
        return ''.join(result)


def main():
    parser = argparse.ArgumentParser(prog='pg.py', description='Generate ASCII passwords',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--chars", metavar='C', type=int, default=14,
                        help='Length of password in characters')
    parser.add_argument("-a", "--amount", metavar='A', type=int, default=1,
                        help='Amount of passwords')

    args = parser.parse_args()

    password = Password()
    password.generate(args.chars, args.amount)

    return password.__repr__()


if __name__ == '__main__':
    print(main())
