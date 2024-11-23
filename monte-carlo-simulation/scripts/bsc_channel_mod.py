import numpy as np


def bsc_channel(input_bits, ber):
    """
    Simulates a Binary Symmetric Channel (BSC) with a given Bit Error Rate (BER).

    Parameters:
    input_bits (array-like): The input bit sequence to be transmitted.
    ber (float): The bit error rate, must be between 0 and 1.

    Returns:
    output_bits (ndarray): The output bit sequence after transmission through the BSC.
    flipped_bits_count (int): The number of bit flips that occurred.
    """
    # Convert input_bits to a NumPy array of integers if it isn't already
    input_bits = np.array(input_bits, dtype=int)

    # Generate random numbers for each bit to simulate errors based on BER
    random_values = np.random.rand(len(input_bits))

    # Flip bits where random values are less than the BER
    output_bits = np.where(random_values < ber, 1 - input_bits, input_bits)

    # Count the number of flipped bits
    flipped_bits_count = np.sum(output_bits != input_bits)

    return output_bits, flipped_bits_count


# Example usage for varying input data lengths

# Define different lengths of input_data to test
input_lengths = [1,3,7,15,31,63,127,255]

# Test for different BER values
ber_values = [0.01, 0.05, 0.1]

# Loop through different input lengths and BER values
for length in input_lengths:
    print(f"\nTesting with input length {length}...")

    # Generate random input data (0s and 1s)
    input_data = np.random.choice([0, 1], size=length)

    for ber in ber_values:
        output_bits, flipped_bits = bsc_channel(input_data, ber)
        print(f"BER: {ber}, Number of flipped bits: {flipped_bits}")
