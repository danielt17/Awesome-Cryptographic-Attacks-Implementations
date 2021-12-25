# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 13:54:37 2021

@author: danie
"""

# %% Imports

import numpy as np
from AttackOnLFSR import Berlekamp_Massey_algorithm,LFSR,create_valid_seed_and_polynomial,bits_str_to_ls_bits,bin_list_to_int,print_poly
import matplotlib.pyplot as plt
from time import time

# %% Functions

def BSC_channel(sequence,p=0.1):
    output_sequence = [];
    position_changes = []
    for cur_bit in sequence:
        if np.random.rand() < p:
            new_cur_bit = int(not cur_bit)
            position_changes.append(1)
        else:
            new_cur_bit = cur_bit
            position_changes.append(0)
        output_sequence.append(new_cur_bit)    
    return output_sequence,position_changes

def plot_sequence_difference_after_bsc_channel(lfsr_sequence,lfsr_bsc_sequence,lfsr_position_changes,p):
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(lfsr_sequence,label='Original LFSR sequence')
    plt.plot(lfsr_bsc_sequence, label = 'LFSR sequence after BSC with probality of: ' + str(p))
    plt.ylabel('Bit value [#]')
    plt.legend(loc = 'upper right')
    plt.title('Comparison between original LFSR sequence and LFSR sequence after binary symmetric channel')
    plt.subplot(2,1,2)
    plt.plot(lfsr_position_changes, label = 'Error locations')
    plt.title('Position of errors in the LFSR sequence after the binary symmetric channel')
    plt.xlabel('Bit number [#]')
    
def Berlekamp_Massey_algorithm_fails(lfsr_bsc_sequence,k):
    BM = Berlekamp_Massey_algorithm(lfsr_bsc_sequence[:k//2])
    end = time()
    print('Time taken to recover LFSR seed and polynomial coefficents: ' + str(end - start) + ' [sec]\n')
    recovered_seed = BM.get_seed(); recovered_taps = BM.get_taps()
    print('Recovered seed: ' + str(bin_list_to_int(recovered_seed)) + '\n')
    print('Recovered polynomial: ' + str(print_poly(''.join(map(str,recovered_taps)))) + '\n')
    estimated_degree = BM.get_degree()
    print('Recovered polynomial order: ' + str(estimated_degree) + '\n')

# %% Main

if __name__ == '__main__':
    start = time()
    print('\n\n\n\n\n')
    print('POC of recovering an LFSR over a binary symmetric channel (BSC) \n')
    print('Using a HMM to model the LFSR undergoing the BSC \n')
    print('The LFSR polynomial is learned using a sigmoid model for the markov states \n')
    print('The optimization is done using the Expectation-Maximization (EM) algorithm \n')
    n = 32 # poly order 
    k = n*20 # LFSR sequence size
    enable_brute_force_attack = False
    seed, feedback_poly = create_valid_seed_and_polynomial(n)
    print('Initial seed: ' + str(bin_list_to_int(bits_str_to_ls_bits(seed))) + '\n')
    print('Generated polynomial: ' + str(print_poly(feedback_poly)) + '\n')
    lfsr = LFSR(bits_str_to_ls_bits(seed), bits_str_to_ls_bits(feedback_poly[::-1]))
    lfsr_sequence = lfsr.get_lfsr(k)
    print('LFSR sequence of size: ' + str(k) + '\n')
    print('LFSR original sequence: ' + str(lfsr_sequence))
    p = 0.1
    lfsr_bsc_sequence,lfsr_position_changes = BSC_channel(lfsr_sequence,p)
    print('BSC with probabilty of: p = ' + str(p) + '\n')
    print('LFSR sequence after BSC: ' + str(lfsr_bsc_sequence) + ' \n')
    print('Positions of errors with respect to original sequence: ' + str(lfsr_position_changes) + ' \n')
    plot_sequence_difference_after_bsc_channel(lfsr_sequence,lfsr_bsc_sequence,lfsr_position_changes,p)
    Berlekamp_Massey_algorithm_fails(lfsr_bsc_sequence,k)
    print('We can see the Berlekamp Massey algorithm fails therefore, we are going to use a more advanced method \n')
    print('The method is based upon a probablstic approach modeling the LFSR as a markov model\n')
    print('And the sequence after the output of the binary symmetric channel as Hidden Markov Model training problem \n')
    print('Our goal is going to be to estaimte the polynomial coefficents of the LFSR \n')
    # Should implement the paper: Maximum likelihood binary shift-register synthesis from noisy obsetvations
    
    
    
    