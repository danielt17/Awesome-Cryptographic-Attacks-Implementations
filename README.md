# Awesome implementations of cryptographic attacks
This repository details implementations of different cryptographic attacks

# What is this ?

This is a list of implementations of cryptographic attacks, all implementations are in python 3.7.

# Table of contents

1. LFSR cracking using Berlekamp Massey algorithm, recovering both the degree of the polynomial recurrnce, seed and polynomial coefficents.

## LFSR cracking

In this subsection we are going to go over a state recovery attack against a LFSR pseudo random number generator (prng). First, we will introduce the LFSR and its inner workings, afterwards we will go over coefficent recovery using matrix inversion over `GF(2)`. Finally, we will go over the Berlekamp Massey algorithm which solves the problem in a very efficent manner with respect to both time and space complexity.
