#!/usr/bin/env python3

import sys
import argparse
import numtools


def main():
    parser = argparse.ArgumentParser(description='Number factorization utility. '
                                                 'Prints prime factors in the following format: '
                                                 '2 2 2 3 23')
    parser.add_argument(dest='n', type=str, help='Number to factorize')
    parser.add_argument('-x', '--hex', dest='hex', action='store_true', help='input in hexadecimal')
    parser.add_argument('-b', '--bin', dest='bin', action='store_true', help='input in binary')
    parser.add_argument('-o', '--oct', dest='oct', action='store_true', help='input in octal')
    parser.add_argument('-t', '--test', dest='test', action='store_true', help='test for primality without factorizing')
    args = parser.parse_args()

    n, x, b, o, t = args.n, args.hex, args.bin, args.oct, args.test
    if int(x) + int(b) + int(o) > 1:
        parser.print_usage()
        sys.exit(1)

    if x or n.startswith('0x'):  base = 16
    elif b or n.startswith('0b'): base = 2
    elif o or n.startswith('0o'): base = 8
    else:
        base = 10

    try:
        n = int(n, base)
    except ValueError as e:
        print(e)
        parser.print_usage()
        sys.exit(1)

    if not t:
        factors = numtools.factorize(n)
        for k, v in factors.items():
            for _ in range(v):
                print(k, end=' ')
        print()
    else:
        is_prime = numtools.miller_rabin(n)
        print(('composite', 'prime')[is_prime])


if __name__ == '__main__':
    main()
