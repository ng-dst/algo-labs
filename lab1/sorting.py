#!/usr/bin/env python3
from random import randint


def merge_sort(arr, key=lambda x: x, reverse=False, start=0, end=None):
    if len(arr) <= 1:
        return
    if end is None:
        end = len(arr)
    if start < end:
        half_size = (start + end) // 2
        merge_sort(arr, key, reverse, start, half_size)
        merge_sort(arr, key, reverse, half_size+1, end)
        merge(arr, key, reverse, start, half_size+1, end)


def merge(arr, key, reverse, start, mid, end):
    left = arr[start:mid]
    right = arr[mid:end+1]
    i = 0
    j = 0
    while i < len(left) or j < len(right):
        if i < len(left) and j < len(right):
            if (key(left[i]) <= key(right[j])) ^ reverse:
                arr[start + i+j] = left[i]
                i += 1
            else:
                arr[start + i+j] = right[j]
                j += 1
        elif i < len(left):
            arr[start + i+j] = left[i]
            i += 1
        else:
            arr[start + i+j] = right[j]
            j += 1


def quick_sort(arr, key=lambda x: x, reverse=False, start=0, end=None):
    if end is None:
        end = len(arr)
    if start < end:
        p1, p2 = partition(arr, key, reverse, start, end)
        quick_sort(arr, key, reverse, start, p1)
        quick_sort(arr, key, reverse, p2, end)


def partition(arr, key, reverse, start, end):
    rand = randint(start, end-1)
    pivot = key(arr[rand])
    left = list()
    eq = list()
    right = list()
    for i in range(start, end):
        if key(arr[i]) == pivot:
            eq.append(arr[i])
        elif (key(arr[i]) < pivot) ^ reverse:
            left.append(arr[i])
        else:
            right.append(arr[i])
    l1 = len(left)
    l2 = l1 + len(eq)
    for i in range(len(left)):
        arr[start + i] = left[i]
    for i in range(len(eq)):
        arr[start + l1 + i] = eq[i]
    for i in range(len(right)):
        arr[start + l2 + i] = right[i]
    return start + l1, start + l2
