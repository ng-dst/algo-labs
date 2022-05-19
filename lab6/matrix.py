import math
import numpy as np


def random_matrix(n, m):
    return np.random.random(size=(n, m))


def save_matrix(M, file):
    np.save(file, M)


def load_matrix(file):
    return np.load(file)


def multiply_naive(a, b):
    n, m = a.shape
    p, q = b.shape
    if m != p:
        print("Unable to multiply: incorrect matrices sizes")
        return -1
    c = np.zeros((n, q))
    for i in range(n):
        for j in range(q):
            for k in range(p):
                c[i][j] += a[i][k] * b[k][j]
    return c


def pad_matrix(a, k):
    b = np.zeros((k, k))
    n, m = a.shape
    for i in range(n):
        for j in range(m):
            b[i][j] = a[i][j]
    return b


def pad_size(n, m=None):
    if m is None:
        m = n
    return 2 ** math.ceil(np.log2(max(n, m)))