"""

Cryptopals challenge 8 in set 1.

Detecting which ciphertext has been encrypted with AES-ECB,
among a collection of ciphertexts.

Challenge website: https://cryptopals.com/sets/1/challenges/8

"""

# Standard library imports
import os

# Ensure correct directory and open file
filename = "8.txt"
filepath = os.path.dirname(__file__) + "/" + filename

"""
The file 8.txt consists of a collection of hex-encoded ciphertexts. 
We first need to split them into separate ciphertexts.
So we need to find the newline character.
This is done using the readlines() function.
"""

with open(filepath, mode="r") as f:
    ciphertextsHexencodedList = f.readlines()

"""
Convert the ciphertexts to bytearrays.
"""

ciphertextsBytesList = []

for ciphertextHexencoded in ciphertextsHexencodedList:
    ciphertextsBytesList.append(ciphertextHexencoded.strip('\n').encode())

"""
We now need to find which of the ciphertexts has been encrypted with AES-ECB.
The ciphertext will have 16-byte blocks that are identical because 
AES-ECB is stateless and deterministic.

This is done by iterating over the ciphertexts, 
and comparing them pairwise.
(This algorithm has a bad time complexity, but good enough for this purpose.)
"""

# List of tuples (i,j,k) which have identical 16-byte blocks,
# where i = ciphertext index
#       j = first member of identical block
#       k = second member of identical block
ECBtextblockList = []

for i in range(len(ciphertextsBytesList)): # Iterate over the ciphertexts
    for j in range(int(len(ciphertextsBytesList[i])/16)-1): # Iterate over the 16-byte blocks in a ciphertext
        for k in range(j): # Compare to the subsequent blocks
            if ciphertextsBytesList[i][j*16:j*16+16] == ciphertextsBytesList[i][k*16:k*16+16]:
                ECBtextblockList.append((i,j,k))
                break

for ECBblock in ECBtextblockList:
    print("\nCiphertext %i is encoded with ECB." % (ECBblock[0]))
    print("Blocks %i and %i are identical." % (ECBblock[1], ECBblock[2]))
    print("They consists of the following:")
    print("%s and %s" % (ciphertextsBytesList[ECBblock[0]][ECBblock[1]*16:ECBblock[1]*16+16].decode(), ciphertextsBytesList[ECBblock[0]][ECBblock[2]*16:ECBblock[2]*16+16].decode()))