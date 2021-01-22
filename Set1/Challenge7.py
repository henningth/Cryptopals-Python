"""

Cryptopals challenge 7 in set 1.

Decrypting AES in ECB mode with key given.

Challenge website: https://cryptopals.com/sets/1/challenges/7

"""

# Standard library imports
import base64
import os

# Third party imports
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Functions
def aesDecrypt(ciphertext, key):

    cipher = Cipher(algorithm=algorithms.AES(key), mode=modes.ECB(), backend=default_backend())

    decryptor = cipher.decryptor()

    decryptedPlaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return decryptedPlaintext

# Ensure correct directory and open file
filename = "7.txt"
filepath = os.path.dirname(__file__) + "/" + filename

with open(filepath) as f:
    ciphertextBase64 = f.read()

# Convery Base64 file input to binary string
ciphertext = base64.b64decode(ciphertextBase64)

key = b'YELLOW SUBMARINE'

# Decrypt the ciphertext with the given key
decryptedPlaintext = aesDecrypt(ciphertext, key)

# Prints results
print(decryptedPlaintext.decode())