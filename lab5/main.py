#!/usr/bin/env python3

import argparse
import binascii

from manager import *


def main():
    parser = argparse.ArgumentParser(description='MD4 preimage search utility'
                                                 'Finds preimage in 2^64 keyspace for a given MD4 hash.')
    parser.add_argument(dest='hash', type=str, help='MD4 hash (hex)')
    parser.add_argument('-t', '--threads', dest='threads', type=int, default=4, help='Number of threads')
    args = parser.parse_args()

    h, t = args.hash, args.threads
    if t < 1:
        parser.print_usage()
        exit(1)
    print('[*] Working...')
    md4_search_preimage(binascii.unhexlify(h), t)


if __name__ == '__main__':
    main()
