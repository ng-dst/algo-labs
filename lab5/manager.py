from multiprocessing import Pool

import count
from md4 import *


def md4_invert_part(a, b, c, d, k):
    s = b'\0'*4 + struct.pack('<I', k)
    s = pad(s)
    w = list(map(Int32, struct.unpack('<16I', s)))
    a = Int32(a) - A
    b = Int32(b) - B
    c = Int32(c) - C
    d = Int32(d) - D
    return _md4_invert_round3(a, b, c, d, w)


def _md4_invert_round3(a, b, c, d, w):
    w = [w[i] + Int32(0x6ED9EBA1) for i in range(16)]
    for i in (3, 1, 2, 0):
        b = md4_invert_step(H, b, c, d, a, w[i + 12], 15)
        c = md4_invert_step(H, c, d, a, b, w[i + 4], 11)
        d = md4_invert_step(H, d, a, b, c, w[i + 8], 9)
        if i:
            a = md4_invert_step(H, a, b, c, d, w[i], 3)
    return a, b, c, d


def _work(argv):
    return count.enum(*argv)


def md4_search_preimage(h, threads=4):
    h = struct.unpack('<4I', h)
    argv = [None] * threads
    i = 0
    while i < (1 << 32):
        with Pool(processes=threads) as p:
            for j in range(threads):
                ph = md4_invert_part(*h, i)
                argv[j] = (i, ph, h)
                i += 1
            for t in p.imap_unordered(_work, argv):
                if t:
                    p.terminate()
                    return 0
    print('[-] Could not find preimage in the given keyspace')
    return -1

