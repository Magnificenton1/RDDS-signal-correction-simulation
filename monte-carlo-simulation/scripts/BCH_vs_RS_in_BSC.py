import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os

def generate_plots():
    # BER range, with different steps
    ber_values = []

    # Adding values for the range from 0.0000001 to 0.01 with step 0.0001
    ber_values.extend(np.arange(0.0000001, 0.01, 0.0001))

    # Adding values for the range from 0.01 to 0.2 with step 0.01
    ber_values.extend(np.arange(0.01, 0.21, 0.01))

    # Lists to store simulation results
    num_errors_bch_list = []
    ber_bch_list = []
    received_text_matches_bch_list = []

    num_errors_rs_list = []
    ber_rs_list = []
    received_text_matches_rs_list = []

    # Prepare for simulation
    input_text = "Test input"  # Adjust the input data as needed
    channel = "BSC"  # You can change this to other channels if needed

    # Run simulations for different BER values
    for ber_value in ber_values:
        # BCH Simulation
        print(f"Running simulation for BCH code at BER = {ber_value}")
        num_errors_bch, ber_bch, received_text_matches_bch = run_simulation(input_text, channel, "BCH", ber_value)
        if num_errors_bch is not None:  # Check if the data is valid
            num_errors_bch_list.append(num_errors_bch)
        else:
            num_errors_bch_list.append(np.nan)  # Replace missing values with NaN

        if ber_bch is not None:
            ber_bch_list.append(ber_bch)
        else:
            ber_bch_list.append(np.nan)  # Replace missing values with NaN

        received_text_matches_bch_list.append(received_text_matches_bch)

        # RS Simulation
        print(f"Running simulation for RS code at BER = {ber_value}")
        num_errors_rs, ber_rs, received_text_matches_rs = run_simulation(input_text, channel, "RS", ber_value)
        if num_errors_rs is not None:  # Check if the data is valid
            num_errors_rs_list.append(num_errors_rs)
        else:
            num_errors_rs_list.append(np.nan)  # Replace missing values with NaN

        if ber_rs is not None:
            ber_rs_list.append(ber_rs)
        else:
            ber_rs_list.append(np.nan)  # Replace missing values with NaN

        received_text_matches_rs_list.append(received_text_matches_rs)

    # Generate the plots
    plt.figure(figsize=(10, 6))

    # Plot 1: Number of errors vs BER for BCH and RS
    plt.subplot(2, 1, 1)
    plt.plot(ber_values, num_errors_bch_list, label="BCH - Number of Errors", color='b', marker='o', linestyle='-')
    plt.plot(ber_values, num_errors_rs_list, label="RS - Number of Errors", color='r', marker='x', linestyle='-')
    plt.xlabel("BER")
    plt.ylabel("Number of Errors")
    plt.title("Number of Errors vs BER")
    plt.legend()
    plt.grid(True)

    # Plot 2: Text matches vs BER for BCH and RS
    plt.subplot(2, 1, 2)
    plt.plot(ber_values, received_text_matches_bch_list, label="BCH - Text Matches", color='b', marker='o', linestyle='-')
    plt.plot(ber_values, received_text_matches_rs_list, label="RS - Text Matches", color='r', marker='x', linestyle='-')
    plt.xlabel("BER")
    plt.ylabel("Text Matches (True/False)")
    plt.title("Text Matches vs BER")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    # Save the plot to a file
    figures_dir = "../figures"
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)

    plt.savefig(os.path.join(figures_dir, "BCH_vs_RS_in_BSC_plot.png"))
    plt.show()

    # Save results to CSV file
    csv_dir = "../CSV"
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    with open(os.path.join(csv_dir, "BCH_vs_RS_in_BSC_results.csv"), 'w') as f:
        f.write("BER,BCH_Num_Errors,RS_Num_Errors,BCH_Text_Matches,RS_Text_Matches\n")
        for i in range(len(ber_values)):
            f.write(f"{ber_values[i]},{num_errors_bch_list[i]},{num_errors_rs_list[i]},{received_text_matches_bch_list[i]},{received_text_matches_rs_list[i]}\n")


def run_simulation(input_text, channel, code_type, ber_value):
    try:
        process = subprocess.Popen(
            ['python', '../../App.py'],  # Use 'python' for Windows
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send the input data to the program
        process.stdin.write(f"{input_text}\n")
        process.stdin.write("88\n")  # Number of bits
        process.stdin.write(f"{channel}\n")
        process.stdin.write(f"{code_type}\n")

        if code_type == "RS":
            process.stdin.write("32\n")  # Parity symbols for RS (if applicable)

        process.stdin.write(f"{ber_value}\n")
        process.stdin.flush()

        # Collect the output
        output, _ = process.communicate()

        # Debug: Print full output from App.py
        print(f"Full output for BER = {ber_value}, Code = {code_type}:\n{output}\n{'-' * 50}")

        # Extract number of bit errors
        try:
            if "Number of bit errors:" in output:
                num_errors = int(output.split("Number of bit errors:")[1].split()[0])
            else:
                num_errors = None
        except (IndexError, ValueError) as e:
            num_errors = None
            print(f"Error extracting number of bit errors for BER = {ber_value}, Code = {code_type}: {e}")

        # Extract BER (Bit Error Rate)
        try:
            if "BER (Bit Error Rate):" in output:
                ber = float(output.split("BER (Bit Error Rate):")[1].split()[0])
            else:
                ber = None
        except (IndexError, ValueError) as e:
            ber = None
            print(f"Error extracting BER for BER = {ber_value}, Code = {code_type}: {e}")

        # Check if the received text matches the original text
        received_text_matches = "True" in output
        print(f"Received text matches: {received_text_matches}")

        return num_errors, ber, received_text_matches

    except Exception as e:
        print(f"Error occurred during simulation for BER = {ber_value}, Code = {code_type}: {e}")
        return None, None, None


# Run the function to generate plots
generate_plots()
