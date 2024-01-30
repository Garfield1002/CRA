#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
// gcc -shared -Wl,-soname,midori64c -o midori64c.so -fPIC midori64.c
#define BLOCK_SIZE 16

typedef uint8_t block_t[BLOCK_SIZE];

block_t S_BOX = {
    0xc, 0xa, 0xd, 0x3,
    0xe, 0xb, 0xf, 0x7,
    0x8, 0x9, 0x1, 0x5,
    0x0, 0x2, 0x4, 0x6
};

block_t SHUFFLE = {
    0x0, 0xa, 0x5, 0xf,
    0xe, 0x4, 0xb, 0x1,
    0x9, 0x3, 0xc, 0x6,
    0x7, 0xd, 0x2, 0x8
};

block_t INV_SHUFFLE = {
    0x0, 0x7, 0xe, 0x9,
    0x5, 0x2, 0xb, 0xc,
    0xf, 0x8, 0x1, 0x6,
    0xa, 0xd, 0x4, 0x3
};

block_t M = {
    0, 1, 1, 1,
    1, 0, 1, 1,
    1, 1, 0, 1,
    1, 1, 1, 0
};


void subCell(block_t block) {
    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] = S_BOX[block[i]];
    }
}

void shuffleCell(block_t block) {
    block_t output = {0};

    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        output[i] = block[SHUFFLE[i]];
    }

    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] = output[i];
    }
}

void invShuffleCell(block_t block) {
    block_t output = {0};

    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        output[i] = block[INV_SHUFFLE[i]];
    }

    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] = output[i];
    }
}

void addRoundKey(block_t block, uint8_t* roundKey) {
    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] ^= roundKey[i];
    }
}

void mixColumns(block_t block) {
    block_t output = {0};

    // col
    for (size_t i = 0; i < 4; i++)
    {
        // line
        for (size_t j = 0; j < 4; j++)
        {
            // mul
            for (size_t k = 0; k < 4; k++)
            {
                output[j + 4 * i] ^= block[k + 4 * i] * M[j + 4 * k];
            }
        }
    }

    for (size_t i = 0; i < BLOCK_SIZE; i++)
    {
        block[i] = output[i];
    }
}

void encrypt(block_t msg, size_t round_count, uint8_t* roundKeys) {
    for (size_t i = 0; i < round_count; i++)
    {
        subCell(msg);
        shuffleCell(msg);
        mixColumns(msg);
        addRoundKey(msg, &roundKeys[i * BLOCK_SIZE]);
    }
}

void decrypt(block_t ct, size_t round_count, uint8_t* roundKeys) {
    for (size_t i = 0; i < round_count; i++)
    {
        addRoundKey(ct, &roundKeys[(round_count -  1 - i) * BLOCK_SIZE]);
        mixColumns(ct);
        invShuffleCell(ct);
        subCell(ct);
    }
}