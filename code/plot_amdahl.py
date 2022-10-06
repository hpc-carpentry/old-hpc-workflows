"""
Plotting script for HPC Workflows scaling study
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import sys

from matplotlib.lines import Line2D


def actual_speedup(parallel_wall_time, serial_wall_time):
    return serial_wall_time / parallel_wall_time


def amdahl_speedup(serial_proportion, parallel_proportion, num_cores):
    normalized_run_time = serial_proportion + (parallel_proportion / num_cores)
    return 1.0 / normalized_run_time


def analyze_scaling_study(log_files, img_file):
    # Initialize empty variable to hold data(frame)
    data_frame = None

    # Append log files to the dataframe
    for log_file in log_files:
        with open(log_file, "r") as f:
            data = json.loads(f.read())
            data_frame = pd.concat([data_frame, pd.DataFrame([data])])

    # Sort by processor count, print for reference
    data_frame.sort_values(by="nproc", inplace=True)

    # Calculate speedup factor
    serial_wall_time = data_frame.iloc[0]["execution_time"]
    data_frame["speedup"] = data_frame["execution_time"].apply(
        actual_speedup,
        args=(serial_wall_time,)
    )

    # Print out the data frame as a table
    print(data_frame.to_string(index=False))

    # Create the plot object
    plt.figure()

    # Make graph more legible
    parallel_percent = 100 * data_frame["parallel_proportion"].iloc[0]
    title = "Amdahl's Law: {:.0f}% Parallel Work".format(parallel_percent)
    plt.title(title)
    plt.xlabel("Number of Processes $N$")
    plt.ylabel("Speedup Factor $S$")

    # Print the scaling study data
    plt.plot(data_frame["nproc"], data_frame["speedup"],
             "o", label="actual data")

    # Save the limits of the plotted data in x and y
    data_range = [plt.xlim(), plt.ylim()]

    # Calculate and plot theoretical speedup factor
    markers = Line2D.filled_markers
    for index, parallel_proportion in enumerate((0.7, 0.8, 0.9, 1)):
        serial_proportion = 1 - parallel_proportion
        num_cores = range(1, data_frame["nproc"].max() + 1)
        speedup = [amdahl_speedup(serial_proportion, parallel_proportion, x)
                   for x in num_cores]
        label = r"theory, $p=%.2f$" % parallel_proportion
        plt.plot(num_cores, speedup, linestyle=":", marker=markers[index+1],
                 markersize=4, label=label, zorder=0)

    # Reset plot limits to the actual data
    plt.xlim(data_range[0])
    plt.ylim(data_range[1])

    # Show the legend and store the plot as an image
    plt.legend(loc="best")
    plt.savefig(img_file, dpi=400, bbox_inches="tight")


if __name__ == "__main__":
    # Check whether filenames were supplied
    usage = "plot_amdahl.py {input_json_files} output_png_file"

    if len(sys.argv) == 0 or (".png" not in sys.argv[-1]):
        print(usage)
        sys.exit(1)

    # Get list of log file names
    log_files = sys.argv[1:-1]

    # Set plot image file name
    img_file = sys.argv[-1]

    analyze_scaling_study(log_files, img_file)
