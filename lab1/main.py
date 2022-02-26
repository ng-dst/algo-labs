#!/usr/bin/env python3

import sys
import time
import argparse

from multiprocessing import Process
from sorting import quick_sort, merge_sort_p
from hashgen import generate_hashes


def key(sha_hash):
    return int(sha_hash[:16], 16)


def run(func, hashes, file_dst, file_dst_rev):
    init_time = time.thread_time()

    hashes_1 = hashes[:]
    hashes_2 = hashes[:]

    func(hashes_1, key)
    with open(file_dst, 'w') as f:
        f.writelines(hashes_1)

    func(hashes_2, key, reverse=True)
    with open(file_dst_rev, 'w') as f:
        f.writelines(hashes_2)

    total_time = time.thread_time() - init_time
    print(f'Thread {func.__name__}: finished in {total_time} s')


def main():
    parser = argparse.ArgumentParser(description='Applies quicksort & mergesort to SHA-1 hashes in a file.')
    parser.add_argument('-i', '--input', metavar='FILE', type=str, default='', help='input file with hashes')
    parser.add_argument('-o', '--output', metavar='PATH', dest='out_path', default='.', help='path to write results')
    parser.add_argument('-g', '--generate', metavar='N', dest='generate', type=int, default=0, help='generate N hashes')
    args = parser.parse_args()

    if not args.input and args.generate <= 0:
        parser.print_usage()
        sys.exit(1)

    if args.generate > 0:
        hashes = generate_hashes(args.generate)
        args.input = "generator"
    else:
        with open(args.input) as f:
            hashes = f.readlines()

    print(f'Read {len(hashes)} hashes from {args.input}.')
    print('Running...')
    proc_qsort = Process(target=run, args=(quick_sort, hashes,
                                           args.out_path + '/quicksort.txt', args.out_path + '/quicksort_rev.txt'))
    proc_msort = Process(target=run, args=(merge_sort_p, hashes,
                                           args.out_path + '/mergesort.txt', args.out_path + '/mergesort_rev.txt'))
    proc_qsort.start()
    proc_msort.start()

    proc_qsort.join()
    proc_msort.join()

    print('Done!')


if __name__ == '__main__':
    main()
