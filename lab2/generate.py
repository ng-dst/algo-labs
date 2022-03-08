#!/usr/bin/env python3

import argparse
import pickle
import sys

from graphs import Graph


def main():
    parser = argparse.ArgumentParser(description='Generates graph of size N and density characteristic D (0 <= D <= 1) '
                                                 'and outputs with Pickle. Use > operator to write the output to file.')
    parser.add_argument(metavar='N', dest='n', type=int, help='number of nodes')
    parser.add_argument('-d', '--density', metavar='D', dest='d', type=float, default=0.25, help='graph density '
                                                                                       '(0 - no edges, 1 - full graph)')
    args = parser.parse_args()

    if not args.n:
        parser.print_usage()
        sys.exit(1)

    g = Graph.generate(args.n, args.d)
    sys.stdout.buffer.write(pickle.dumps(g))


if __name__ == '__main__':
    main()
