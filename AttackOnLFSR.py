# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:14:20 2021

@author: danie
"""

# %% imports

from time import time
import random
from numpy import where,array
from functools import reduce

# %% Functions

# LFSR implemetation from https://en.wikipedia.org/wiki/Linear-feedback_shift_register

class LFSR:
    """ Normal LFSR impl with pythonic inputs. Everything is in `GF(2)`
    n-bit LFSR defined by given feedback polynomial
    seed = MSB to LSB list of bits
    feedback_polynomial = MSB to LSB list of bits
    """

    def __init__(self, seed, poly):
        if len(seed) != len(poly):
            raise Exception('Error: Seed and taps poly should be of same length')
        self._seed = seed.copy()        # Sn, Sn-1, ..., S0
        self._comb_poly = poly          # C0, C1, ..., Cn
    
    def next_bit(self):
        """ Generate next output bit """
        tapped = [self._seed[i] for i,j in enumerate(self._comb_poly) if j == 1] # taking elements in seed for which poly coefficent is 1
        xored = reduce(lambda x,y: x^y, tapped) # xoring all elements in tapped to get LFSR next step
        opt = self._seed.pop(0) # popping out of lfsr first element
        self._seed.append(xored) # appending xored value as last element
        return opt
    
    def get_lfsr(self, steps):
        """ Get next `steps` number of output bits """
        opt = [self.next_bit() for _ in range(steps)]
        return opt
    
    def set_seed(self, new_seed):
        """ Set the new seed to generate new LFSR using same polynomial """
        self._seed = new_seed.copy()

# https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm

class Berlekamp_Massey_algorithm:
    """ Berlekamp - Massey algo: PYTHON IMPLEMENTATION
    i/p:    S:  `list` of 0s and 1s, Sn, Sn-1, Sn-2, ... S1, S0.
    o/p:   min degree of C, Feedback Polynomial, anything else that we want 
    """

    def __init__(self, S):
        self.S = S
        C = [1]     # Connection polynomial. The one that generates next o/p bit. 1, C1, C2, ..., CL.
        L = 0       # Minimal size of LFSR at o/p
        m = -1      # num iterations since L and B were updated.
        B = [1]     # Previous value of C, before it was updated.
        n = 0       # counter. i.e. the iterator
        N = len(S)  # The length of i/p

        while(n < N):
            bit_calc = [i&j for i,j in zip(C,S[n-L:n+1][::-1])]
            d = reduce(lambda x, y: x^y, bit_calc,0)
            if d:
                c_temp = C.copy()
                lc = len(C)
                next_C = [0]*(n-m) + B + [0]*(lc - len(B) - n + m)
                C = [i^j for i,j in zip(C,next_C)] + next_C[lc:]
                if L <= n>>1:
                    L = n + 1 - L
                    m = n
                    B = c_temp.copy()
            n += 1
        self._L = L
        self._C = C[::-1]
        self._seed = S[:L]

    def get_seed(self):
        return self._seed

    def get_taps(self):
        return self._C[:-1][::-1]

    def get_degree(self):
        return self._L

def create_valid_seed_and_polynomial(n):
    # creating a valid random seed and polynomial coefficents
    rndm_seed = bin(random.getrandbits(n))[2:]
    seed = rndm_seed + '0'*(n-len(rndm_seed))
    rndm_poly = bin(random.getrandbits(n))[2:]
    feedback_poly = rndm_poly + '0'*(n - len(rndm_poly))
    return seed, feedback_poly

def bits_str_to_ls_bits(string):
    # transforming a string of bits to a list of bits
    return list(map(int,string))

def bin_list_to_int(ls):
    # transforming binary list to int
    out = 0
    for bit in ls:
        out = (out << 1) | bit
    return out

def print_poly(polynomial):
    # print polynomial
    poly_ls = bits_str_to_ls_bits(polynomial)
    poly_params = list(where(array(poly_ls)==1)[0]+1) + [0]
    result = ''
    lis = sorted(poly_params, reverse=True)
    for i in lis:
        if i == 0:
            result += '1'
        else:
            result += 'x^%s' % str(i)

        if i != lis[-1]:
            result += ' + '
    return result
    
# %% Main

if __name__ == '__main__':
    print('\n\n\n')
    print('Demo of reconstructing the inner state of a LFSR PRNG\n')
    n = 256 # poly order 
    k = n*2 # LFSR sequence size
    enable_brute_force_attack = False
    seed, feedback_poly = create_valid_seed_and_polynomial(n)
    print('Initial seed: ' + str(bin_list_to_int(bits_str_to_ls_bits(seed))) + '\n')
    print('Generated polynomial: ' + str(print_poly(feedback_poly)) + '\n')
    lfsr = LFSR(bits_str_to_ls_bits(seed), bits_str_to_ls_bits(feedback_poly[::-1]))
    lfsr_sequence = lfsr.get_lfsr(k)
    print('LFSR sequence of size: ' + str(k) + '\n')
    print('LFSR output sequence: ' + str(lfsr_sequence) + '\n')
    print('Running attack on LFSR to recover internal state and polynomial coefficents:\n')
    print('Running Berlekamp Massey algorithm: \n')
    start = time()
    BM = Berlekamp_Massey_algorithm(lfsr_sequence)
    end = time()
    print('Time taken to recover LFSR seed and polynomial coefficents: ' + str(end - start) + ' [sec]\n')
    recovered_seed = BM.get_seed(); recovered_taps = BM.get_taps()
    print('Recovered seed: ' + str(bin_list_to_int(recovered_seed)) + '\n')
    print('Recovered polynomial: ' + str(print_poly(''.join(map(str,recovered_taps)))) + '\n')
    estimated_degree = BM.get_degree()
    print('Recovered polynomial order: ' + str(estimated_degree) + '\n')
    lfsr_new = LFSR(recovered_seed, recovered_taps[::-1])
    recovered_sequence = lfsr_new.get_lfsr(k)
    print('Original LFSR output: ' + str(lfsr_sequence) + '\n')
    print('Recovered LFSR output: ' + str(recovered_sequence) + '\n')
    success_flag = False
    if recovered_sequence == lfsr_sequence:
        print('No mismatch for ' + str(n) + ' bit seed. Matched ' + str(k) + ' (random) output bits\n')
        print('Success!\n')
        success_flag = True
    else:
        for i, j in enumerate(zip(recovered_sequence, lfsr_sequence)):
            if j[0] != j[1]:
                print('For ' + str(k) + ' bits, 1st mismatch at index: ' + str(i) + '\n')
                print('Partial Success. Need more output bits\n')
                break
        raise Exception('Didnt crack LFSR! \n')
    print('Cracked LFSR! \n')
        
