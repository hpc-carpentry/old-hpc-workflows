"""
Plotting script for HPC Workflows scaling study
"""

import pandas as pd
import json
import matplotlib
import matplotlib.pyplot as plt
import sys
matplotlib.use("AGG")  # plot to disk, rather than to a window

usage = "plot_amdahl.py list_of_inputs.json"

# Check whether filenames were supplied
if len(sys.argv) == 0:
    print(usage)
    sys.exit(1)

# Get list of log files
log_files = sys.argv[1:]

df = None  # Initialize an empty DataFrame

# Append log files to the dataframe
for log_file in log_files:
    with open(log_file, 'r') as f:
        data = json.loads(f.read())
        df = pd.concat([df, pd.DataFrame([data])])

# Sort by processor count, print for reference
df.sort_values(by='nproc', inplace=True)
print(df)

# Calculate and plot speedup factor
serial_time = df.iloc[0]['execution_time']
plt.plot(df['nproc'], serial_time/df['execution_time'], 'o', label='Actual')

# Calculate and plot theoretical speedup factor
parallel_proportion = df.iloc[0]['parallel_proportion']
serial_proportion = 1 - parallel_proportion
processors_range = range(1, df['nproc'].max())
speedup = 1.0 / (serial_proportion + (parallel_proportion/processors_range))
plt.plot(processors_range, speedup, ':', label='Theoretical')

# Make graph more legible
plt.xlabel('Number of Processes')
plt.ylabel('Speedup Factor')
plt.legend()
parallel_percent = int(100 * df.iloc[0]['parallel_proportion'])

title = "Amdahl's Law Example, {}% parallel".format(parallel_percent)
plt.title(title)

filename = 'amdahl-{}-pct-parallel.png'.format(parallel_percent)
plt.savefig(filename, dpi=400, bbox_inches='tight')
