import os
import mmh3

from bloomfilter import BloomFilter
from multiprocessing import Process

PROCESSES = 16


def find_offset(pattern, filename, generator=False):
    size = len(pattern)
    pattern_hash = mmh3.hash(pattern)
    offset = 0
    with open(filename) as f:
        while True:
            s = f.read(size)
            if not s:
                return
            if mmh3.hash(s) == pattern_hash:
                yield offset
                if not generator:
                    return
            offset += 1
            f.seek(offset, 0)


def search(bf, filename, pattern, do_all=False):
    if pattern in bf:
        for offset in find_offset(pattern, filename, do_all):
            print(offset, pattern)


def work(text_file, patterns, do_all=False):
    bf = BloomFilter(os.path.getsize(text_file) - len(patterns[0]) + 1, 0.01)
    init_bf(bf, text_file, len(patterns[0]))
    processes = []
    for pattern in patterns:
        p = Process(target=search, args=(bf, text_file, pattern, do_all))
        processes.append(p)
        p.start()
        if len(processes) == PROCESSES:
            for p in processes:
                p.join()
            processes = []
    for p in processes:
        p.join()


def init_bf(bf, filename, pattern_len):
    with open(filename) as f:
        for j in range(bf.items_count):
            f.seek(j, 0)
            string = f.read(pattern_len)
            if not string:
                break
            bf.add(string)
