#!/usr/bin/env python3

import random
from math import gcd


def witness(a, n):
    if n == 2 or n == 3:
        return False
    if n % 2 == 0:
        return True
    u = n - 1
    t = 0
    while u & 1 == 0:
        t += 1
        u >>= 1
    x = pow(a, u, n)
    for i in range(t):
        y = pow(x, 2, n)
        if y == 1 and x != 1 and x != n-1:
            return True
        x = y
    return x != 1


def miller_rabin(n, s=20):
    for _ in range(s):
        a = random.randint(1, n-1)
        if witness(a, n):
            return False  # composite
    return True  # probably prime


def pollard_rho(n):
    if n <= 3:
        return n
    if n % 2 == 0:
        return 2
    x = random.randint(0, n-1)
    y = x
    k = 2
    cycle = set()
    count = 0
    i = 0
    while True:
        count += 1
        i += 1
        if x in cycle:
            return n
        elif count == 65537:
            cycle.add(x)
            count = 0
        x = (x**2 - 1) % n
        d = gcd(y - x, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = x
            k *= 2


def factorize(n):
    factors = dict()
    while n > 1:
        if not miller_rabin(n):
            d = pollard_rho(n)
            n //= d
            if not miller_rabin(d):
                fd = factorize(d)
                factors = sum_dicts(factors, fd)
            else:
                factors = sum_dicts(factors, {d: 1})
        else:
            factors = sum_dicts(factors, {n: 1})
            break
    return factors


def sum_dicts(d1, d2):
    for k, v in d2.items():
        if k not in d1.keys():
            d1[k] = v
        else:
            d1[k] += v
    return d1
