"""
Solution to Cryptopals challenge 4 in set 1.

Detect single-character XOR.

The file 4.txt contains one 60-character string 
that has been encrypted with single-character XOR.

Challenge website: https://cryptopals.com/sets/1/challenges/4
"""

# Standard library imports
import os

# Custom imports
from Challenge3 import computeCharacterFrequency, compareCharacterFrequencyToEnglish, decodeHexStringToASCII, getEnglishCharacterFrequency

# Ensure correct directory
filename = "4.txt"
filepath = os.path.dirname(__file__) + "/" + filename

savefilepath = os.path.dirname(__file__) + "/" + "4sorted.txt"

fileContents = [] # One string in each position in the list
asciiStrings = [] # Each entry contains a dictionary, with the 256 possible bytes (keys) used for decryption

# Read file
with open(filepath, "r") as f:
    fileContents = f.readlines()

for string in fileContents:
    asciiStrings.append(decodeHexStringToASCII(string))

asciiCharacterFrequencyList = []
asciiCharacterSquaredDistanceList = []
asciiCharacterAbsDistanceList = []

asciiStringsCharacterFrequencies = {}

# Compute character frequency of decrypted strings
num = 0
for asciiString in asciiStrings:

    asciiCharacterFrequency = {}
    asciiCharacterSquaredDistance = {}
    asciiCharacterAbsDistance = {}

    for key in asciiString.keys():
        asciiCharacterFrequency[key] = computeCharacterFrequency(asciiString[key])
        asciiCharacterSquaredDistance[key], asciiCharacterAbsDistance[key] = compareCharacterFrequencyToEnglish(asciiCharacterFrequency[key])

    asciiCharacterFrequencyList.append(asciiCharacterFrequency)
    asciiCharacterSquaredDistanceList.append(asciiCharacterSquaredDistance)
    asciiCharacterAbsDistanceList.append(asciiCharacterAbsDistance)

    num += 1

# For each of the 60 strings, sort character frequency of the tables in ascending order
# (from: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)

asciiCharacterSquaredDistanceSortedList = []
asciiCharacterAbsDistanceSortedList = []

for asciiCharacterSquaredDistance in asciiCharacterSquaredDistanceList:
    asciiCharacterSquaredDistanceSortedList.append({k: v for k, v in sorted(asciiCharacterSquaredDistance.items(), key=lambda item: item[1])})
    
for asciiCharacterAbsDistance in asciiCharacterAbsDistanceList:
    asciiCharacterAbsDistanceSortedList.append({k: v for k, v in sorted(asciiCharacterAbsDistance.items(), key=lambda item: item[1])})

# Save results (top-10 for each string) in a text file
strnum = 1
with open(savefilepath, mode="w") as f:
    for asciiCharacterSquaredDistanceSorted in asciiCharacterSquaredDistanceSortedList:
        num = 0
        f.write("String: " + str(strnum))
        for key, value in asciiCharacterSquaredDistanceSorted.items():
            #print(asciiStrings[key], "with distance: ", value)
            f.write( str(asciiCharacterSquaredDistanceSorted[key]) + "with distance: " + str(value) )
            num += 1
            if num == 5:
                break
        strnum += 1

pass