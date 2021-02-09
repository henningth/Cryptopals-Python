"""

Cryptopals challenge 9 in set 2.

Implementing PKCS#7 padding.

Challenge website: https://cryptopals.com/sets/2/challenges/9

"""

def PKCS7padder(plaintext, blocksize):
    """
    Implements PKCS#7 padding on input plaintext, 
    returns padded plaintext, taking blocksize
    into account.
    Assumes plaintext to be shorter than blocksize.

    Input:
    plaintext [byte]
    blocksize [int]

    Output:
    paddedPlaintext [byte]
    """
    plaintextLength = len(plaintext)

    # Take care of invalid input cases
    if plaintextLength > blocksize:
        return b''

    paddedPlaintext = b''

    # Special case is when length of the input plaintext
    # is equal to the blocksize. Then an extra block 
    # of length blocklength is added
    if plaintextLength == blocksize:
        # Pad the plaintext to be a multiple of blocksize bytes
        padding = blocksize.to_bytes(1,'little')*blocksize

        paddedPlaintext = plaintext + padding

    # Otherwise, we are in the standard case
    else:
        # Pad the plaintext to be a multiple of blocksize bytes
        paddingLength = blocksize - plaintextLength

        padding = paddingLength.to_bytes(1,'little')*paddingLength

        paddedPlaintext = plaintext + padding

    return paddedPlaintext

def PKCS7unpadder(paddedPlaintext, blocksize):
    """
    Removes padding from padded plaintext
    Assumes plaintext to be shorter than blocksize.

    Input:
    paddedPlaintext [byte]
    blocksize [int]

    Output:
    plaintext [byte]
    """

    plaintext = b''

    for paddingLength in range(1,blocksize+1): # Loop over valid padding lengths
        padding = paddingLength.to_bytes(1,'little')*paddingLength
        if padding == paddedPlaintext[blocksize-paddingLength:]:
            # Remove the padding from the plaintext
            plaintext = paddedPlaintext[0:blocksize-paddingLength]
            break
        if paddingLength == blocksize:
            # Remove entire last block
            plaintext = paddedPlaintext[0:blocksize]
            break

    return plaintext

def testPadding(plaintext, blocksize):
    """
    Test function for the PKCS7 padder and unpadder
    """
    paddedPlaintext = PKCS7padder(plaintext, blocksize)
    unpaddedPlaintext = PKCS7unpadder(paddedPlaintext, blocksize)
    print(plaintext)
    print(paddedPlaintext)
    print(unpaddedPlaintext, "\n")
    assert len(paddedPlaintext) % blocksize == 0
    assert len(plaintext) == len(unpaddedPlaintext)

if __name__ == "__main__":

    # Test 1: From the website
    plaintext = b'YELLOW SUBMARINE'
    blocksize = 20
    testPadding(plaintext, blocksize)

    # Test 2: Standard padding
    plaintext = b'SEGA GENESIS'
    blocksize = 16
    testPadding(plaintext, blocksize)

    # Test 3: Standard padding
    plaintext = b'NINTENDO'
    blocksize = 16
    testPadding(plaintext, blocksize)

    # Test 4: Plaintext length equal to blocksize
    plaintext = b'YELLOW SUBMARINE'
    blocksize = 16
    testPadding(plaintext, blocksize)