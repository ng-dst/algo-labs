#!/usr/bin/env python3

def merge_sort_p(arr, key=lambda x: x, reverse=False):
    arr_srt = merge_sort(arr, key, reverse)
    while arr:
        arr.pop()
    arr += arr_srt


def merge_sort(arr, key=lambda x: x, reverse=False):
    if len(arr) <= 1:
        return arr
    half_size = len(arr) // 2
    left = merge_sort(arr[:half_size], key, reverse)
    right = merge_sort(arr[half_size:], key, reverse)
    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    res = list()
    while left and right:
        if (key(left[0]) <= key(right[0])) ^ reverse:
            res.append(left.pop(0))
        else:
            res.append(right.pop(0))
    res += left
    res += right
    return res


def quick_sort(arr, key=lambda x: x, reverse=False, start=0, end=None):
    if end is None:
        end = len(arr) - 1
    if start < end:
        p = partition(arr, key, reverse, start, end)
        quick_sort(arr, key, reverse, start, p-1)
        quick_sort(arr, key, reverse, p+1, end)


def partition(arr, key, reverse, start, end):
    pivot = key(arr[end])
    i = start - 1
    for j in range(start, end):
        if (key(arr[j]) <= pivot) ^ reverse:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    i += 1
    arr[i], arr[end] = arr[end], arr[i]
    return i
