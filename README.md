# Awesome implementations of cryptographic attacks
This repository details implementations of different cryptographic attacks

# What is this ?

This is a list of implementations of cryptographic attacks, all implementations are in python 3.7.

# Table of contents

1. LFSR cracking using Berlekamp Massey algorithm, recovering both the degree of the polynomial recurrnce, seed and polynomial coefficents.

## LFSR cracking

In this subsection we are going to go over a state recovery attack against a LFSR pseudo random number generator (prng). First, we will introduce the LFSR and its inner workings, afterwards we will go over coefficent recovery using matrix inversion over `GF(2)`. Finally, we will go over the Berlekamp Massey algorithm which solves the problem in a very efficent manner with respect to both time and space complexity.

### Linear-feedback shift register

Linear-feedback shift register AKA LFSR is a shift register whose input bit is a linear function of its previous state. There are many uses for LFSRs which include but are not limited to: pseudo random number generators, pseudo-noise sequences, whitening sequences and more. LFSRs are a very attractive choice for implementations of RNG as they are very easy implement in hardware requiring only xor and shift operations.
The LFSR works in the following way, one defines a list of taps which are bits which are feedback into the LFSR this bits will define the next state of the LFSR. After defining the taps one can define a coresponding polynomial over `GF(2)` which describes the LFSR. Finally, when one wants to run the LFSR he inputs a seed and asks the LFSR to do a given amount of step, which will correspond to a list of binary outputs.

<figure>
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/99/Lfsr.gif" />
</p>
</figure>

A gif describing the evolution of states in a LFSR of size 16 can be seen above, all standard LFSR work in the same, where the change is the amount of taps and there location.

### LFSR polynomial coefficent recovery using matrix inversion

We can describe the LFSR recuresion formula in the following way:

![image](https://user-images.githubusercontent.com/60748408/141657818-b3b6c39f-d211-4d69-a0ab-b68acf312f53.png)

One can describe the LFSR system as a matrix multiplication formula over `GF(2)`, where the equation is:

![image](https://user-images.githubusercontent.com/60748408/141657879-6842e7c0-86bf-4084-b694-3769ddba6ac2.png)

Where the matrix and the vector are defined in the following way:

![image](https://user-images.githubusercontent.com/60748408/141657915-6bc3018a-2de1-42f7-b2f6-9112218093ac.png)

If we assume the degree of the polynomial describing the LFSR is `n`, one needes to see `2*n` bits in order to recover the polynomial coefficents. Using matrix inversion over `GF(2)` can recover the coefficent vector in the following way:

![image](https://user-images.githubusercontent.com/60748408/141657993-c93ad4a2-a67e-4643-9b7e-8eae60bc082b.png)

The reason this approach isnt wildely used is because matrix inversion over a finite field has a time complexity of `O(n^3)`, and in addition an inverted matrix doesn't always exist. 

### LFSR full recovery using Berlekamp Massey algorithm


