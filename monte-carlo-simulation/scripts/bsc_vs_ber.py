import numpy as np
import matplotlib.pyplot as plt
import csv
from bsc_channel_mod import bsc_channel

# Simulation parameters
num_simulations = 1000  # Number of simulations per parameter set
input_data = [0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1]

def run_bsc_comparison(input_bits, ber_values):
    results = []
    for ber in ber_values:
        total_flips = 0
        for _ in range(num_simulations):
            output_bits, flipped_bits_count = bsc_channel(input_bits, ber)
            total_flips += flipped_bits_count
        avg_flips = total_flips / num_simulations
        results.append((ber, avg_flips))
    return results

def save_results_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["BER", "Average Bit Flips"])
        for row in data:
            writer.writerow(row)

def plot_bsc_comparison(results, plot_filename):
    ber_values, avg_flips = zip(*results)
    plt.plot(ber_values, avg_flips, marker='o')
    plt.title('BSC Comparison - Average Bit Flips vs BER')
    plt.xlabel('Bit Error Rate (BER)')
    plt.ylabel('Average Bit Flips')
    plt.grid(True)
    plt.savefig(plot_filename)
    plt.show()

# Run the BSC simulation
ber_values = np.logspace(-3, -6, 10)  # BER values in realistic range: 10^-3 to 10^-6
bsc_results = run_bsc_comparison(input_data, ber_values)

# Save results to CSV
save_results_to_csv('../CSV/bsc_vs_ber_results.csv', bsc_results)

# Generate the plot
plot_bsc_comparison(bsc_results, '../figures/bsc_vs_ber_plot.png')
