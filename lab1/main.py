#!/usr/bin/env python3
import os
import sys
import time
import argparse

from multiprocessing import Process
from sorting import quick_sort, merge_sort
from hashgen import generate_hashes

sys.setrecursionlimit(100000)


def key(sha_hash):
    return int(sha_hash[:16], 16)


def run(func, hashes, file_dst, file_dst_rev):
    init_time = time.thread_time()

    hashes_1 = hashes[:]
    hashes_2 = hashes[:]

    func(hashes_1, key)
    try:
        with open(file_dst, 'w') as f:
            f.writelines(hashes_1)
    except IOError as e:
        print(f"Thread {func.__name__}: error writing to {file_dst}: {e.strerror}")

    func(hashes_2, key, reverse=True)
    try:
        with open(file_dst_rev, 'w') as f:
            f.writelines(hashes_2)
    except IOError as e:
        print(f"Thread {func.__name__}: error writing to {file_dst_rev}: {e.strerror}")

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
        try:
            with open(args.input) as f:
                hashes = f.readlines()
        except IOError as e:
            print(f"File {args.input} not found: {e.strerror}")
            sys.exit(1)

    if not os.path.exists(args.out_path + "/"):
        os.mkdir(args.out_path)

    print(f'Read {len(hashes)} hashes from {args.input}.')
    print('Running...')
    proc_qsort = Process(target=run, args=(quick_sort, hashes,
                                           args.out_path + '/quicksort.txt', args.out_path + '/quicksort_rev.txt'))
    proc_msort = Process(target=run, args=(merge_sort, hashes,
                                           args.out_path + '/mergesort.txt', args.out_path + '/mergesort_rev.txt'))
    proc_qsort.start()
    proc_msort.start()

    proc_qsort.join()
    proc_msort.join()


if __name__ == '__main__':
    main()
