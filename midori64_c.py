'''
This is more of an experience for using C with python.
It speeds up encryption a tiny bit.
'''
from ctypes import *

midori64 = CDLL('./midori64c.so')

block_t = c_uint8 * 16

subCell_c = midori64.subCell
shuffleCell_c = midori64.shuffleCell
invShuffleCell_c = midori64.invShuffleCell
mixColumns_c = midori64.mixColumns

def encrypt_differential(msg, keys: list[list[int]]):
    m = block_t(*msg)

    arr = c_uint8 * (len(keys) * 16)
    ks = arr(*[x for key in keys for x in key])
    midori64.encrypt_differential(m, ks)

    return [x for x in m]

def encrypt(msg, r, keys: list[list[int]]):
    m = block_t(*msg)

    arr = c_uint8 * (len(keys) * 16)
    ks = arr(*[x for key in keys for x in key])
    midori64.encrypt(m, r, ks)

    return [x for x in m]

def decrypt(ct, r, keys):
    m = block_t(*ct)

    arr = c_uint8 * (len(keys) * 16)
    ks = arr(*[x for key in keys for x in key])
    midori64.decrypt(m, r, ks)

    return [x for x in m]