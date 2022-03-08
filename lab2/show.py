#!/usr/bin/env python3

import argparse
import sys

from graphs import Graph


def main():
    parser = argparse.ArgumentParser(description='Show graph stored in a file')
    parser.add_argument(dest='filename', type=str, help='File with pickle dump of graph')
    args = parser.parse_args()
    try:
        g = Graph.load(args.filename)
    except IOError as e:
        print(f"Could not load graph from {args.filename}: {e}")
        sys.exit(1)
    g.show()


if __name__ == '__main__':
    main()
