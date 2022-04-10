#!/usr/bin/env python3

import argparse

from manager import *


def main():
    parser = argparse.ArgumentParser(description='Search for a set of equal-length patterns in a text file')
    parser.add_argument('-p', '--patterns', dest='patterns', metavar='FILE', type=str, help='File with patterns, one in each line')
    parser.add_argument(dest='file', metavar='FILE', type=str, help='Text file')
    parser.add_argument('-a', '--all', dest='all', action='store_true',
                        help="Find all occurrences (by default: only the first one)")
    args = parser.parse_args()

    with open(args.patterns) as f:
        patterns = list(map(lambda x: x[:-1], f.readlines()))

    work(args.file, patterns, args.all)


if __name__ == '__main__':
    main()