#!/usr/bin/env python3

import argparse
import time

from strassen import *


def main():
    parser = argparse.ArgumentParser(description='Matrix multiplication utility\n'
                                                 'Multiplies two matrices using Strassen algorithm\n'
                                                 'prints the matrix if only one file specified')
    group1 = parser.add_mutually_exclusive_group(required=True)
    group2 = parser.add_mutually_exclusive_group(required=False)
    group3 = parser.add_mutually_exclusive_group(required=False)

    group1.add_argument('-g', '--generate', dest='g', nargs=2, metavar='N M', type=int, default=list(), help='Generate matrix of size NxM')
    group1.add_argument(dest='file1', type=str, nargs='?', default='', help='File with dump of numpy matrix')
    parser.add_argument(dest='file2', type=str, nargs='?', default='', help='File with dump of numpy matrix')
    group2.add_argument('-m', '--multi', dest='multi', action='store_true', help='Use multithreading for Strassen')
    group2.add_argument('-n', '--naive', dest='naive', action='store_true', help='Naive multiplication')
    group3.add_argument('-o', '--output', dest='file3', metavar='FILE', type=str, default='', help='File to save the result to')
    group3.add_argument('-t', '--timing', dest='timing', action='store_true', help='Measure timing, do not store result')
    args = parser.parse_args()

    file1, file2, file3 = args.file1, args.file2, args.file3
    multi, naive, timing = args.multi, args.naive, args.timing
    generate = args.g

    if generate:
        if len(generate) != 2:
            parser.print_usage()
            return
        res = random_matrix(generate[0], generate[1])
        output(file3, res)
        return

    if not file1:
        parser.print_usage()
        return

    a = np.load(file1)
    if not file2:
        print(a)
        return

    b = np.load(file2)
    n, m = a.shape
    p, q = b.shape

    if m != p:
        print('Unable to multiply matrices: incorrect sizes.')
        return

    if not naive:
        k = max(pad_size(n, m), pad_size(p, q))
        a = pad_matrix(a, k)
        b = pad_matrix(b, k)

    if timing:
        t1 = time.time_ns()

    if naive:
        res = multiply_naive(a, b)
    else:
        res = multiply_strassen(a, b, multi)

    if timing:
        t = time.time_ns() - t1
        print('Time: %d.%09d s' % (t // 1e9, t % 1e9))
        return

    res = res[:n, :q]
    output(file3, res)


def output(file3, res):
    if file3:
        np.save(file3, res)
        print(f'Saved the result to "{file3}"')
    else:
        print(res)


if __name__ == '__main__':
    main()
