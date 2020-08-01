"""
Solution to Cryptopals challenge 2 in set 1.

Fixed XOR.

Challenge website: https://cryptopals.com/sets/1/challenges/2
"""

def fixedXOR(hexStr1, hexStr2):
    """
    This function takes two strings represented as hex, 
    and returns the XOR or them.

    Inputs:
    hexStr1 [str]: First input
    hexStr2 [str]: Second input

    Output:
    str1xorStr2 [str]: The exclusive OR (XOR) or hexStr1 and hexStr2
    """

    str1xorStr2 = int(hexStr1, 16) ^ int(hexStr2, 16) # Use builtin XOR function

    str1xorStr2 = hex(str1xorStr2)[2:] # Remove '0x' part

    if len(str1xorStr2) < len(hexStr1): # Since Python removes leading zeros
        str1xorStr2 = ("0" * (len(hexStr1) - len(str1xorStr2))) + str1xorStr2

    return str1xorStr2

if __name__ == "__main__":
    """
    Testing the fixedXOR function.
    """

    hexStr1 = "1c0111001f010100061a024b53535009181c"
    hexStr2 = "686974207468652062756c6c277320657965"

    correctResult = "746865206b696420646f6e277420706c6179"

    functionResult = fixedXOR(hexStr1, hexStr2)

    if correctResult == functionResult:
        print("The results match.")
    else:
        print("The results do not match.")