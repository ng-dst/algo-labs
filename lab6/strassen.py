from multiprocessing import Pool

from matrix import *

NAIVE_MUL_BOUND = 64


def multiply_strassen(a, b, multi=False):
    if a.shape[0] <= NAIVE_MUL_BOUND:
        return multiply_naive(a, b)

    n, m = a.shape
    # assuming n == m == p == q == pad_size

    res = np.zeros((n, n))
    k = n//2

    a11 = a[:k, :k]
    a12 = a[:k, k:]
    a21 = a[k:, :k]
    a22 = a[k:, k:]
    b11 = b[:k, :k]
    b12 = b[:k, k:]
    b21 = b[k:, :k]
    b22 = b[k:, k:]

    """a11 = np.zeros((k, k))
    a12 = np.zeros((k, k))
    a21 = np.zeros((k, k))
    a22 = np.zeros((k, k))
    b11 = np.zeros((k, k))
    b12 = np.zeros((k, k))
    b21 = np.zeros((k, k))
    b22 = np.zeros((k, k))

    for i in range(k):
        for j in range(k):
            a11[i][j] = a[i][j]
            a12[i][j] = a[i][k+j]
            a21[i][j] = a[k+i][j]
            a22[i][j] = a[k+i][k+j]
            b11[i][j] = b[i][j]
            b12[i][j] = b[i][k+j]
            b21[i][j] = b[k+i][j]
            b22[i][j] = b[k+i][k+j]
    """
    if not multi:
        p1 = multiply_strassen(a11, b12 - b22)
        p2 = multiply_strassen(a11 + a12, b22)
        p3 = multiply_strassen(a21 + a22, b11)
        p4 = multiply_strassen(a22, b21 - b11)
        p5 = multiply_strassen(a11 + a22, b11 + b22)
        p6 = multiply_strassen(a12 - a22, b21 + b22)
        p7 = multiply_strassen(a11 - a21, b11 + b12)
    else:
        tasks = ( (a11, b12 - b22),
                  (a11 + a12, b22),
                  (a21 + a22, b11),
                  (a22, b21 - b11),
                  (a11 + a22, b11 + b22),
                  (a12 - a22, b21 + b22),
                  (a11 - a21, b11 + b12) )
        pool = Pool(processes=7)
        p = pool.starmap(multiply_strassen, tasks)
        pool.close()
        p1, p2, p3, p4, p5, p6, p7 = p

    res[:k, :k] = p4 + p5 + p6 - p2
    res[:k, k:] = p1 + p2
    res[k:, :k] = p3 + p4
    res[k:, k:] = p1 - p3 + p5 - p7
    """
    for i in range(k):
        for j in range(k):
            res[i][j] = c11[i][j]
            res[i][k+j] = c12[i][j]
            res[k+i][j] = c21[i][j]
            res[k+i][k+j] = c22[i][j]
    """
    return res
