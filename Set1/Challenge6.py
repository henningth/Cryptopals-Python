"""

Cryptopals challenge 6 in set 1.

Breaking repeated-key XOR.

Challenge website: https://cryptopals.com/sets/1/challenges/6

"""

# Standard library imports
import base64
import os

# Function for computing edit distance (Hamming distance):
# how many bits are different in the two input strings.
def editDistance(bitstring1, bitstring2):
    """
    This function computes the edit distance between two bitstrings.
    It is defined as the number of bit positions where the two 
    bitstrings differ. This is equal to the number of bit positions 
    where the XOR of the two bitstrings is 1.

    Inputs:
    bitstring1 [bytes]
    bitstring2 [bytes]

    Returns:
    distance [int]
    """
    distance = 0
    for b in range(len(bitstring1)):
        distance = distance + bin(bitstring1[b] ^ bitstring2[b])[2:].count('1')

    return distance

def repeatedKeyXOR(ciphertext, key):
    """
    This function computes the repeated-key XOR between ciphertext 
    and key. The ciphertext is split into blocks of length equal to 
    the length of key, and each block is XOR'ed with key.
    It returns the XOR between them, which is the variable plaintext.

    Inputs:
    ciphertext [bytes]
    key [bytes]

    Returns:
    plaintext [bytes]
    """

    k = 0

    plaintext = bytearray()

    # Compute the XOR byte-wise
    
    k = 0
    for i in range(len(ciphertext)):
        plainCharacter = ciphertext[i] ^ key[k]
        plaintext.append(plainCharacter)
        k += 1
        if k % len(key) == 0:
            k = 0
    
    return plaintext

def compareToEnglish(decodedStrings):
    """
    This function computes the score of the input string.
    For each character in the input string, we do a lookup 
    in a dictionary to see if the character is in the English alphabet.
    If it is, the score of the character is added to the total score.
    Each character has a score, based on the relative frequency 
    of that character in English text.

    Input:
    decodedStrings [byte]

    Returns:
    score [int]
    """
    englishCharacterFrequency = {"a": 8.497,
                             "b": 1.492,
                             "c": 2.202,
                             "d": 4.253,
                             "e": 11.162,
                             "f": 2.228,
                             "g": 2.015,
                             "h": 6.094,
                             "i": 7.546,
                             "j": 0.153,
                             "k": 1.292,
                             "l": 4.025,
                             "m": 2.406,
                             "n": 6.749,
                             "o": 7.507,
                             "p": 1.929,
                             "q": 0.095,
                             "r": 7.587,
                             "s": 6.327,
                             "t": 9.356,
                             "u": 2.758,
                             "v": 0.978,
                             "w": 2.560,
                             "x": 0.150,
                             "y": 1.994,
                             "z": 0.077,
                             " ": 17.100} # From: http://www.fitaly.com/board/domper3/posts/136.html and Wikipedia

    # Compute score of the input text
    score = 0
    for decodedString in decodedStrings.lower():
        score += englishCharacterFrequency.get(chr(decodedString), 0)

    return score

# Keysize possibilities
keysizes = list(range(2,41))

# Ensure correct directory and open file
filename = "6.txt"
filepath = os.path.dirname(__file__) + "/" + filename

with open(filepath) as f:
    base64string = f.read()

# Convery Base64 file input to binary string
byteString = base64.b64decode(base64string)

"""
Iterate over the possible keysizes given, where in each 
iteration, the ciphertext is split into blocks of length
equal to the current keysize. 

For each pair of blocks, compute the edit distance between them.
Do this for all consecutive blocks and average it.
This is done to find the most likely keysize, because that 
keysize will (statistically) give the smallest distance
between blocks.
"""

avgDistances = {}

for keysize in keysizes:

    distances = []

    # Break the ciphertext into blocks of size keysize
    blocks = []
    for i in range(0,len(byteString), keysize):
        blocks.append(byteString[i:i+keysize])

    for i in range(len(blocks)-1):
        try:
            distances.append(editDistance(blocks[i], blocks[i+1])/keysize)
        except:
            pass

    avgDistances[keysize] = sum(distances)/len(distances)

# Find minimum distance
avgDistancesSorted = sorted(avgDistances.items(), key=lambda item: item[1])
minIndex = avgDistancesSorted[0][0]

"""
Make a list with the 256 possible single byte XOR keys
These are used as building blocks for the repeating-key XOR
"""
possibleKeys = []
for currentByte in range(256):
    currentByteHex = hex(currentByte)[2:]

    if len(currentByteHex) == 1:
        currentByteHex = '0' + currentByteHex

    possibleKeys.append(int(currentByteHex,16))

"""
For each possible key of length keysize, compute the repeated-key 
XOR with the ciphertext, and compute the score of the decoded plaintext.
The plaintext with highest score most resembles English.
The corresponding key will be the decoding key.
"""

substrings = {} # Dict, where key is the block-index (1st, 2nd, 3rd etc.) 
                # of original ciphertext, and value is the actual substring

for i in range(0,minIndex):

    substrings[i] = bytearray()

for i in range(0,len(byteString)):

    substrings[i % minIndex].append(byteString[i])

decodedStrings = dict()
characterScore = dict()

for i in range(0, minIndex):

    decodedStrings[i] = dict()
    characterScore[i] = dict()

    for key in possibleKeys:
        decodedStrings[i][key] = bytearray()
        characterScore[i][key] = bytearray()
        
        # XOR the transposed blocks with each of the possible 256 byte keys
        for j in range(len(substrings[i])):
            decodedStrings[i][key].append(substrings[i][j] ^ key)

        characterScore[i][key] = compareToEnglish(decodedStrings[i][key])

characterScoreSorted = list()

# Sort character frequency of the tables in ascending order
# (from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
for i in range(minIndex):
    characterScoreSorted.append({k: v for k, v in sorted(characterScore[i].items(), key=lambda item: item[1], reverse=True)})

"""
Construct the possible decoding keys, based on the smallest distances.
If there are two or more bytes which have the same distance, make two (or more) decoding keys 
based on those bytes.
"""

decodingKey = bytearray()

for charScore in characterScoreSorted:
    # Assume only printable ASCII characters
    # (Since we are asked to compare character 
    # score to English.)
    for character in list(charScore.items()):
        if character[0] >= 32 and character[0] <= 126:
            decodingKey.append(character[0])
            break

# Decode the ciphertext
plaintext = repeatedKeyXOR(byteString, decodingKey)

# And print key and decoded plaintext
print("Key:", decodingKey.decode('latin-1'))
print("Decoded text:", plaintext.decode('latin-1'))