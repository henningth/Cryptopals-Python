"""
Solution to Cryptopals challenge 5

Implementing repeating-key XOR

The plaintext is (note the newline!):

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal

It should be encrypted using repeated key XOR, where the key is "ICE".

Expected output:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Challenge website: https://cryptopals.com/sets/1/challenges/5
"""

import binascii

plaintext = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

expectedCiphertext = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

key = "ICE"

def repeatedKeyXOR(plaintext, key):

    k = 0

    ciphertext = bytearray()
    
    # Compute the XOR character-wise
    for char in plaintext:
        hexPlainCharacter = ord(char)
        hexKeyCharacter = ord(key[k])
        hexCipherCharacter = hexPlainCharacter ^ hexKeyCharacter
        ciphertext.append(hexCipherCharacter)
        k = k + 1
        if k % len(key) == 0:
            k = 0

    return ciphertext

ciphertext = repeatedKeyXOR(plaintext, key)

ciphertextHex = ciphertext.hex()

if ciphertextHex == expectedCiphertext:
    print("Expected hex-string and XOR-ed hex-string match.")
else:
    print("Expected hex-string and XOR-ed hex-string DO NOT match.")