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
                             "z": 0.077}

# Normalize character frequencies
englishCharacterFrequencyNormalized = {}
for key in englishCharacterFrequency.keys():
    englishCharacterFrequencyNormalized[key] = englishCharacterFrequency[key] / 100

def computeCharacterFrequency(asciiString):
    """
    Compute character frequency of string 
    in asciiString, return histogram

    Taken from: https://en.wikipedia.org/wiki/Letter_frequency
    """

    englishCharacters = list(englishCharacterFrequency.keys())

    asciiStringCharacterFrequency = englishCharacterFrequency
    for key in asciiStringCharacterFrequency.keys():
        asciiStringCharacterFrequency[key] = 0

    for englishCharacter in englishCharacters:

        for character in asciiString:

            if character.lower() == englishCharacter:

                asciiStringCharacterFrequency[englishCharacter] += 1

    asciiStringRelativeCharacterFrequency = asciiStringCharacterFrequency
    for key in asciiStringRelativeCharacterFrequency.keys():
        asciiStringRelativeCharacterFrequency[key] = asciiStringRelativeCharacterFrequency[key] / len(asciiString)

    return asciiStringRelativeCharacterFrequency

def compareCharacterFrequencyToEnglish(asciiCharacterFrequency):
    """
    Compares character frequenct in function 
    argument with that of English text, 
    returns distance by computing squared 
    distance between letters
    """

    squaredDistance = 0
    absDistance = 0

    for key in englishCharacterFrequencyNormalized.keys():
        squaredDistance += (asciiCharacterFrequency[key] - englishCharacterFrequencyNormalized[key])**2
        absDistance += abs(asciiCharacterFrequency[key] - englishCharacterFrequencyNormalized[key])

    return squaredDistance, absDistance


def decodeHexStringToASCII(hexString):
    """
    Iterate through the 256 possible byte values, 
    generating the candidate input string using 
    the fixedXOR function
    """

    # Make a dictionary with the 256 possible byte values as keys, 
    # while the repeated byte values as values.
    repeatedBytes = {} # Containing e.g. efefefef...
    decodedStrings = {} # RepeatedBytes XORed with hexEncodedString
    base64Strings = {} # Base64 encoded strings from decodedStrings dict
    asciiStrings = {} # ASCII encoded strings from decodedStrings dict

    numBytesInHexEncodedString = int(len(hexString)/2)

    for currentByte in range(256):
        currentByteHex = hex(currentByte)[2:]

        if len(currentByteHex) == 1:
            currentByteHex = '0' + currentByteHex

        repeatedBytes[currentByte] = currentByteHex * numBytesInHexEncodedString

        decodedStrings[currentByte] = fixedXOR( repeatedBytes[currentByte], hexEncodedString)

        base64Strings[currentByte] = hex2base64(decodedStrings[currentByte])

        asciiStrings[currentByte] = bytearray.fromhex(decodedStrings[currentByte]).decode('latin1')

    return asciiStrings

asciiStrings = decodeHexStringToASCII(hexEncodedString)

asciiCharacterFrequency = {}
asciiCharacterSquaredDistance = {}
asciiCharacterAbsDistance = {}

for key in asciiStrings.keys():
    asciiCharacterFrequency[key] = computeCharacterFrequency(asciiStrings[key])
    asciiCharacterSquaredDistance[key], asciiCharacterAbsDistance[key] = compareCharacterFrequencyToEnglish(asciiCharacterFrequency[key])

# Sort character frequency of the tables in ascending order
# (from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
asciiCharacterSquaredDistanceSorted = {k: v for k, v in sorted(asciiCharacterSquaredDistance.items(), key=lambda item: item[1])}
asciiCharacterAbsDistanceSorted = {k: v for k, v in sorted(asciiCharacterAbsDistance.items(), key=lambda item: item[1])}

# Print results:
print("For squared distance, the ten strings with character distribution closest to English are:")
num = 0
for key, value in asciiCharacterSquaredDistanceSorted.items():
    print(asciiStrings[key], "with distance: ", value)
    num += 1
    if num == 10:
        break

print("\n===================================================================================================\n")
print("For absolute value distance, the ten strings with character distribution closest to English are:")
num = 0
for key, value in asciiCharacterAbsDistanceSorted.items():
    print(asciiStrings[key], "with distance: ", value)
    num += 1
    if num == 10:
        break