#!/usr/bin/env python3

import argparse
import sys

from graphs import Graph


def main():
    parser = argparse.ArgumentParser(description='Find Eulerian / Hamiltonian cycle in graph')
    parser.add_argument(dest='mode', type=str, help='Cycle type (e - Eulerian, h - Hamiltonian)')
    parser.add_argument(dest='filename', type=str, help='File with pickle dump of graph')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help="Do not visualise the path, only print it")
    args = parser.parse_args()

    try:
        g = Graph.load(args.filename)
    except IOError as e:
        print(f"Could not load graph from {args.filename}: {e}")
        sys.exit(1)

    if args.mode == 'e':
        path = g.get_eulerian_cycle()
        if path is None:
            print("Graph is not Eulerian")
            sys.exit(1)
    elif args.mode == 'h':
        path = g.get_hamiltonian_cycle()
        if path is None:
            print("Graph is not Hamiltonian")
            sys.exit(1)
    else:
        parser.print_usage()
        sys.exit(1)

    print(path)
    if not args.quiet:
        g.show(path)


if __name__ == '__main__':
    main()
