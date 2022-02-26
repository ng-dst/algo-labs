#!/usr/bin/env python3

import os

from hashlib import sha1


def generate_hashes(n):
    return [sha1(os.urandom(8)).hexdigest() + '\n' for _ in range(n)]
