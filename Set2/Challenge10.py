"""

Cryptopals challenge 10 in set 2.

Implementing CBC mode.

Challenge website: https://cryptopals.com/sets/2/challenges/10

"""

# Standard library imports
import base64
import os
from math import floor

# Third party imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Custom imports
from Challenge9 import PKCS7padding

# Functions
def bitwiseXOR(bytearray1, bytearray2):
    """
    Computes the bitwise XOR between bytearray1 and bytearray2
    """
    result = int.from_bytes(bytearray1, 'little') ^ int.from_bytes(bytearray2, 'little')
    result = result.to_bytes(len(bytearray1), 'little')
    return result

def AESEncrypt(plaintext, key):
    """
    Encrypts a plaintext using the key 
    key in AES-ECB mode. Only intended 
    for 16 byte blocks.
    """

    cipher = Cipher(algorithm=algorithms.AES(key), mode=modes.ECB(), backend=default_backend())

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext

def AESDecrypt(ciphertext, key):
    """
    Decrypts a ciphertext using the key 
    key in AES-ECB mode. Only intended 
    for 16 byte blocks.
    """

    cipher = Cipher(algorithm=algorithms.AES(key), mode=modes.ECB(), backend=default_backend())

    decryptor = cipher.decryptor()

    decryptedPlaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return decryptedPlaintext

def CBCencrypt(plaintext, key, iv):
    """
    Encrypts a plaintext in Cipher Block Chaining (CBC)
    mode using the key key and 
    initialization vector iv
    Calls the AESencrypt() function for each 
    16 byte block in the plaintext
    """

    blocksize = len(key)

    # This will hold all blocks in the ciphertext
    ciphertext = bytearray()

    # Loop over the 16 byte blocks in the plaintext
    for i in range(0, len(plaintext), blocksize):

        plaintextBlock = plaintext[i:i+blocksize]

        # For the last block, pad it using PKCS7
        if len(plaintextBlock) < blocksize:
            plaintextBlock = PKCS7padding(plaintextBlock, blocksize)

        # For the first plaintext block, the previous block is just the iv
        if i == 0:
            previousBlock = iv

        # XOR the iv and plaintext
        plaintextBlockXORpreviousBlock = bitwiseXOR(previousBlock, plaintextBlock)

        # Encrypt the block using AES and append to ciphertext
        ciphertextBlock = AESEncrypt(plaintextBlockXORpreviousBlock, key)
        ciphertext += ciphertextBlock

        # Update the previous block
        previousBlock = ciphertextBlock

    return bytes(ciphertext)        

def CBCdecrypt(ciphertext, key, iv):
    """
    Decrypts a ciphertext in Cipher Block Chaining (CBC)
    mode using the key key and 
    initialization vector iv
    Calls the AESdecrypt() function for each 
    16 byte block in the ciphertext
    """
    
    blocksize = len(key)

    # This will hold all blocks in the plaintext
    plaintext = bytearray()

    for i in range(0, len(ciphertext), blocksize):

        ciphertextBlock = ciphertext[i:i+blocksize]

        # For the first ciphertext block, the previous block is just the iv
        if i == 0:
            previousBlock = iv
        
        # Decrypt the ciphertext
        plaintextBlock = AESDecrypt(ciphertextBlock, key)

        # XOR the plaintext block and previous ciphertext (or iv in case it's the first one)
        plaintextBlockXORpreviousBlock = bitwiseXOR(plaintextBlock, previousBlock)

        # Remove PKCS7 padding in case it is the last block
        # This means that we need to find the number of 
        # trailing bytes in the plaintext that are equal
        for paddingLength in range(1,blocksize+1): # Loop over valid padding lengths
            padding = paddingLength.to_bytes(1,'little')*paddingLength
            if padding == plaintextBlockXORpreviousBlock[blocksize-paddingLength:]:
                # Remove the padding from the plaintext
                plaintextBlockXORpreviousBlock = plaintextBlockXORpreviousBlock[0:blocksize-paddingLength]

        plaintext += plaintextBlockXORpreviousBlock

        # Update the previous block
        previousBlock = ciphertextBlock

    return bytes(plaintext)

if __name__ == "__main__":
    # Ensure correct directory and open file
    filename = "10.txt"
    filepath = os.path.dirname(__file__) + "/" + filename

    with open(filepath) as f:
        ciphertextBase64 = f.read()

    ciphertext = base64.b64decode(ciphertextBase64)

    # Encryption parameters
    key = b'YELLOW SUBMARINE'
    iv = b'\x00' * len(key) # iv is the same length as the key, since they are XOR'ed together

    # Test with encrypting a file
    decryptedCiphertext = CBCdecrypt(ciphertext, key, iv)

    print("Decrypted ciphertext: ", decryptedCiphertext.decode())

    # Encrypt the decrypted text, compare to original
    encryptedPlaintext = CBCencrypt(decryptedCiphertext, key, iv)

    if encryptedPlaintext == ciphertext:
        print("The encrypted plaintext and the original ciphertext match.")