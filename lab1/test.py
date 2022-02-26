# tests
import sys

from sorting import quick_sort, merge_sort
from hashgen import generate_hashes


def key(x):
    return int(x[:16], 16)


def test(N=100):
    hashes = generate_hashes(N)

    #  1. random
    hashes_qs = hashes[:]
    hashes_ms = hashes[:]
    quick_sort(hashes_qs, key=key)
    merge_sort(hashes_ms, key=key)

    i_prev = None
    for i, j in zip(hashes_qs, hashes_ms):
        if i_prev:
            if i != j or key(i_prev) > key(i):
                print(f"Random test ({N}): not passed!")
                return 1
        i_prev = i

    print(f"Random test ({N}): OK")

    #  2. random reversed
    hashes_qsr = hashes[:]
    hashes_msr = hashes[:]
    quick_sort(hashes_qsr, key=key, reverse=True)
    merge_sort(hashes_msr, key=key, reverse=True)

    if not hashes_qsr == hashes_msr == hashes_qs[::-1]:
        print(f"Random-Reversed test ({N}): not passed!")
        return 1

    print(f"Random-Reversed test ({N}): OK")
    del hashes_qsr

    #  3. already sorted
    merge_sort(hashes_ms)
    quick_sort(hashes_qs)

    if not hashes_qs == hashes_ms:
        print(f"Pre-sorted array test ({N}): not passed!")
        return 1

    print(f"Pre-sorted array test ({N}): OK")

    #  4. reversed array
    merge_sort(hashes_ms, key=key, reverse=True)
    quick_sort(hashes_qs, key=key, reverse=True)
    if not hashes_qs == hashes_ms == hashes_msr:
        print(f"Reversed array test ({N}): not passed!")

    print(f"Reversed array test ({N}): OK")
    print("...\nAll tests passed successfully.")


if len(sys.argv) > 1:
    test(int(sys.argv[1]))
else:
    test()
