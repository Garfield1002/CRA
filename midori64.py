# Midori64:
#   - block size: 64
#   - key size: 128
#   - cell size: 4
#   - number of rounds: 16

# from ctypes import *

#load the shared object file
# adder = CDLL('./adder.so')

import random

S_BOX = [0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]

SHUFFLE = [0, 0xa, 5, 0xf, 0xe, 4, 0xb, 1, 9, 3, 0xc, 6, 7, 0xd, 2, 8]
INV_SHUFFLE = [SHUFFLE.index(i) for i in range(len(SHUFFLE))]

M = [0, 1, 1, 1,
     1, 0, 1, 1,
     1, 1, 0, 1,
     1, 1, 1, 0]

def subCell(xs: list[int]) -> list[int]:
    return [S_BOX[x] for x in xs]

def shuffleCell(xs: list[int]) -> list[int]:
    return [xs[p] for p in SHUFFLE]

def invShuffleCell(xs: list[int]) -> list[int]:
    return [xs[p] for p in INV_SHUFFLE]

def addRoundKey(xs: list[int], roundKey: list[int]) -> list[int]:
    return [xs[i] ^ roundKey[i] for i in range(16)]

def mixColumns(xs):
    output = [0 for _ in range(16)]
    # column
    for i in range(4):
        # line
        for j in range(4):
            # multiplication
            for k in range(4):
                output[j+4*i] ^= M[j+4*k] * xs[k+4*i]
    return output


def encrypt(m, r, roundKeys):
    work_vector = m
    for i in range(r):
        work_vector = subCell(work_vector)
        work_vector = shuffleCell(work_vector)
        work_vector = mixColumns(work_vector)
        work_vector = addRoundKey(work_vector, roundKeys[i])
    return work_vector

def decrypt(c, r, roundKeys):
    work_vector = c
    for i in range(r):
        work_vector = addRoundKey(work_vector, roundKeys[r-1-i])
        work_vector = mixColumns(work_vector)
        work_vector = invShuffleCell(work_vector)
        work_vector = subCell(work_vector)
    return work_vector
