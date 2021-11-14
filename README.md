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

Finally, we are going to use the Berlekamp Massey algorithm to recover a LFSR inner state and seed with a time complexity of `O(n^2)`. The Berlekamp Massey algorithm is an algorithm that findss the hortest linear feedback shift register for a given binary sequence. the algorithm also find the minimal polynomiaal of linearly recurrent sequence in an arbitrary field. The algorithm was first described by James L. Massey in the paper "Shift-Register Synthesis and BCH Decoding" and than described in a simpler way in "The Berlekamp-Massey Algorithm revisited" by Nadia. B. Atti and Gema M. Díaz-Toca.

The algorithm works in the following way:

![image](https://user-images.githubusercontent.com/60748408/141658295-8b37a448-5451-4d1d-ac08-85a67d27e0ff.png)

An intuitive explanation of the algorithm can be given in the following way:

1. Lets assume we want to estimate the paramters of the following recursion sequence, where the next bit of the LFSR output is decribed also by it. Where the coefficents lie in any finite field or infinte field (such as the real number field).

![image](https://user-images.githubusercontent.com/60748408/141685829-f3dc77d8-36a9-4a9b-bab4-6e05b6b9ef29.png)

2. One can prove that inorder to estimate the LFSR exactly we need to see `2*L` bits of output (ofcourse in `GF(2)`), and there exist a unique minimal polynomial such that it reconstruct the output sequence prefectly under those conditions which can be synthesised by the algorithm.

3. After looking at the recurnce relation one can define the following polynomial with respect to the recurrnce relation, if we estimate the derived polynomial coefficents we recovered the LFSR coefficents.

![image](https://user-images.githubusercontent.com/60748408/141685976-150228f7-4ce4-4cac-8dc4-ecc02a77ef06.png)

4. The algorithm starts iteratevly computing the correct polynomial using the following method: we start with an estimated polynomial of degree 0, therefore the estimted polynomial is `C(D)=1`. After intializing the polynomial we solve the equation recusresively each time looking at the polynomial error with respect to the current sequence length, which is called the discrepancy, if we have an error we need to find a coefficent of the this exact degree to add inorder to zero out the discrepancy. The equation describing this recursive process can be seen below.

![image](https://user-images.githubusercontent.com/60748408/141686103-5b9be420-118b-4b14-8b9c-11d24c3e2f90.png)

5. After estimating the discrepancy we do the following update step to get the connection polynomial, which describes the output sequence more accurately:

![image](https://user-images.githubusercontent.com/60748408/141686144-6a5bf13f-7400-473d-8303-690d5b0b24fa.png)

Unlike the algorithm we described earlier the original Berlekamp Massey algorithm, can be written in the following way (which is a little bit more complicated to understand but gives more intution for preforming the algorithm on any finite field):

![image](https://user-images.githubusercontent.com/60748408/141686210-2e90ad0f-2ac3-4263-83b8-e1b3e86cb64d.png)








