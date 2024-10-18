import numpy as np

def string_to_bits(s):
    # Convert each character to its ASCII value, then to its binary representation as bits (0s and 1s).
    bit_list = [int(bit) for char in s for bit in format(ord(char), '08b')]
    
    # Convert the list of bits to a NumPy array of integers
    return np.array(bit_list, dtype=int)

def bits_to_string(bits):
    # Ensure the input is a NumPy array; if not, convert it to one
    if isinstance(bits, list):
        bits = np.array(bits, dtype=int)

    # Split the NumPy array of bits into chunks of 8 bits (since each character is 8 bits long)
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    
    # Convert each 8-bit chunk to a character
    return ''.join(chr(int(''.join(map(str, char)), 2)) for char in chars)