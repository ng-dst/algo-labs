import struct

from int32 import Int32

# constants
A = Int32(0x67452301)
B = Int32(0xefcdab89)
C = Int32(0x98badcfe)
D = Int32(0x10325476)

BLOCK_SIZE = 64


# boolean functions
def F(x, y, z):
    return (x & y) | (~x & z)


def G(x, y, z):
    return (x & y) | (x & z) | (y & z)


def H(x, y, z):
    return x ^ y ^ z


# block operations
def pad(s):
    size = len(s)
    s += b'\x80'
    s += b'\0' * ((56 - (len(s) % 64)) % 64)
    s += struct.pack('<L', 8 * size)
    s += b'\0' * 4
    return s


# round functions
def md4_step(f, a, b, c, d, xk, s):
    return (a + f(b, c, d) + xk) << s


def md4_invert_step(f, y, b, c, d, xk, s):
    return (y >> s) - f(b, c, d) - xk


def md4_round(r, f, x, s, k):
    for j in range(16):
        r[(3*j)%4] = md4_step(f, r[(3 * j) % 4], r[(1 + 3 * j) % 4], r[(2 + 3 * j) % 4], r[(3 + 3 * j) % 4], x[k(j)], s[j % 4])
    return r


# algorithm implementation
def md4_hash_block(s, r_prev=None):
    assert len(s) == 64
    x = list(map(Int32, (struct.unpack('<16I', s))))

    if not r_prev: r_prev = [A, B, C, D]
    x1 = [Int32(0x5A827999) + Int32(x[i]) for i in range(16)]
    x2 = [Int32(0x6ED9EBA1) + Int32(x[i]) for i in range(16)]

    r = r_prev[:]
    r = md4_round(r, F, x, [3, 7, 11, 19], lambda j: j)
    r = md4_round(r, G, x1, [3, 5, 9, 13], lambda j: j // 4 + 4 * (j % 4))
    r = md4_round(r, H, x2, [3, 9, 11, 15], lambda j: [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15][j])
    r = [r[i] + r_prev[i] for i in range(4)]
    return r


def md4(s):
    s = pad(s)
    arr = [s[i:i+BLOCK_SIZE] for i in range(0, len(s), BLOCK_SIZE)]
    r = [A, B, C, D]
    for j in arr:
        r = md4_hash_block(j, r)
    return struct.pack('<I', r[0]) + struct.pack('<I', r[1]) + struct.pack('<I', r[2]) + struct.pack('<I', r[3])
