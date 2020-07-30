"""
Solution to Cryptopals challenge 1 in set 1.

Converting hex to Base64.

Challenge website: https://cryptopals.com/sets/1/challenges/1
"""

def hex2base64(number):
    """
    Function which converts an integer in hexadecimal 
    to its Base64 representation.
    
    Arguments:
    number [str]: Hexadecimal number to convert

    Output:
    base64number [str]: Base64 representation of "number"
    """

    # Convert hexadecimal string to binary
    
    hexNumber = int(number, 16)
    
    binaryNumber = bin(hexNumber)

    binaryNumber = binaryNumber[2:] # Remove the 0b part

    leadingZeros = ""

    # Add leading zeros, since Python automatically removes them
    if len(binaryNumber) % 4:
        for i in range(4 - len(binaryNumber) % 4):
            leadingZeros = "0" + leadingZeros

    binaryNumber = leadingZeros + binaryNumber

    # Make the binary to Base64 lookup table (see Wikipedia: https://en.wikipedia.org/wiki/Base64)
    binary2Base64Dict = {}
    base64Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    base64Number = ""

    for i in range(len(base64Alphabet)):
        binary2Base64Dict[i] = base64Alphabet[i]

    # Check if length of input binary string is a multiple of 6
    paddingLength = 0
    if len(binaryNumber) % 6 == 4: # Four bits in last sextet
        binaryNumber = binaryNumber + "00"
        paddingLength = 1 # Add one "=" as padding the output

    if len(binaryNumber) % 6 == 2: # Two bits in last sextet
        binaryNumber = binaryNumber + "0000"
        paddingLength = 2 # Add two "=" as padding the output


    # Convert binary to Base64 according to the definition

    # Loop through the binary number, discarding last part if
    # the length of the binary number is not a multiple of 6.
    for i in range(0,len(binaryNumber), 6):
        currentBinaryNumber = binaryNumber[i:i+6]
        base64Number = base64Number + binary2Base64Dict[int(currentBinaryNumber, 2)]

    # Add the padding to the output, either one or two equals signs.

    if paddingLength == 1:
        base64Number = base64Number + "="
    
    if paddingLength == 2:
        base64Number = base64Number + "=="

    return base64Number

"""
Here we test the function with the provided input, 
and see if the output from it is as desired.
"""

knownHexInput = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

knownBase64Output = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

print("Correct output: ", knownBase64Output)
print("Base64 output:  ", hex2base64(knownHexInput))

"""
Test cases, generate some random hexadecimal numbers, convert them to Base64, 
and compare with b64 module.
"""

if( hex2base64(knownHexInput) == knownBase64Output ):
    print("Success")
else:
    print("Failure")