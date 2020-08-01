"""
Solution to Cryptopals challenge 3 in set 1.

Single-byte XOR cipher.

Here we find the single byte key which was 
used to XOR the provided string. Decision is 
done using character frequency of the 
English language.

Uses the fixedXOR function from challenge 2, 
where we for the second hex-string repeat each byte 
so that lengths of input strings to fixedXOR function 
match.

Challenge website: https://cryptopals.com/sets/1/challenges/3
"""

from Challenge1 import hex2base64
from Challenge2 import fixedXOR

hexEncodedString = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

numBytesInHexEncodedString = int(len(hexEncodedString)/2)

# Make a dictionary with the 256 possible byte values as keys, 
# while the repeated byte values as values.

repeatedBytes = {} # Containing e.g. efefefef...
decodedStrings = {} # RepeatedBytes XORed with hexEncodedString
base64Strings = {} # Base64 encoded strings from decodedStrings dict
asciiStrings = {} # ASCII encoded strings from decodedStrings dict

"""
Iterate through the 256 possible byte values, 
generating the candidate input string using 
the fixedXOR function
"""
for currentByte in range(256):
    currentByteHex = hex(currentByte)[2:]

    if len(currentByteHex) == 1:
        currentByteHex = '0' + currentByteHex

    repeatedBytes[currentByte] = currentByteHex * numBytesInHexEncodedString

    print(len(repeatedBytes[currentByte]))

    decodedStrings[currentByte] = fixedXOR( repeatedBytes[currentByte], hexEncodedString)

    base64Strings[currentByte] = hex2base64(decodedStrings[currentByte])

    print(len(decodedStrings[currentByte]))

    asciiStrings[currentByte] = bytearray.fromhex(decodedStrings[currentByte]).decode('latin1')

pass