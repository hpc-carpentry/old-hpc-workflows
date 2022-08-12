"""
Plotting script for HPC Workflows scaling study
"""

import pandas as pd
import json
import matplotlib
import matplotlib.pyplot as plt
import sys
matplotlib.use("AGG")  # plot to disk, rather than to a window


def amdahl_speedup(parallel_wall_time, serial_wall_time):
    return serial_wall_time / parallel_wall_time


def analyze_scaling_study(log_files, img_file):
    # Initialize empty variable to hold data(frame)
    df = None

    # Append log files to the dataframe
    for log_file in log_files:
        with open(log_file, 'r') as f:
            data = json.loads(f.read())
            df = pd.concat([df, pd.DataFrame([data])])

    # Sort by processor count, print for reference
    df.sort_values(by='nproc', inplace=True)

    # Calculate speedup factor
    serial_wall_time = df.iloc[0]['execution_time']
    df["speedup"] = df["execution_time"].apply(amdahl_speedup,
                                               args=(serial_wall_time,))

    # Print out the data frame as a table
    print(df.to_string(index=False))

    plt.plot(df['nproc'], df["speedup"], 'o', label='Actual')

    # Calculate and plot theoretical speedup factor
    parallel_proportion = df.iloc[0]['parallel_proportion']
    serial_proportion = 1 - parallel_proportion
    processors_range = range(1, df['nproc'].max())
    speedup = 1.0 / (serial_proportion + (parallel_proportion/processors_range))
    plt.plot(processors_range, speedup, ':', label='Theoretical')

    # Make graph more legible
    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup Factor')

    parallel_percent = int(100 * df.iloc[0]['parallel_proportion'])

    title = "Amdahl's Law Example, {}% parallel".format(parallel_percent)
    plt.title(title)
    plt.legend(loc="best")

    plt.savefig(img_file, dpi=400, bbox_inches='tight')


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
