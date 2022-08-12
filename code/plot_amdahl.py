"""
Plotting script for HPC Workflows scaling study
"""

import pandas as pd
import glob
import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("AGG")

# Get list of log files, read first one into dataframe
log_files = glob.glob('amdahl_*.json')
with open(log_files[0], 'r') as f:
    df = pd.DataFrame([json.loads(f.read())])

# Append rest of log files into same dataframe
for log_file in log_files[1:]:
    with open(log_file, 'r') as f:
        df = pd.concat([df, pd.DataFrame([json.loads(f.read())])])

# Sort by processor count, print for reference
df.sort_values(by='nproc', inplace=True)
print(df)

# Calculate and plot speedup factor
serial_time = df.iloc[0]['execution_time']
plt.plot(df['nproc'], serial_time/df['execution_time'], 'o', label='Actual')

# Calculate and plot theoretical speedup factor
parallel_proportion = df.iloc[0]['parallel_proportion']
processors_range = range(1, df['nproc'].max())
speedup = 1.0/((1-parallel_proportion)+parallel_proportion/processors_range)
plt.plot(processors_range, speedup, ':', label='Theoretical')

# Make graph more legible
plt.xlabel('Number of Processes')
plt.ylabel('Speedup Factor')
plt.legend()
parallel_percent = int(100 * df.iloc[0]['parallel_proportion'])

title = "Amdahl's Law Example, {}% parallel".format(parallel_percent)
plt.title(title)

filename = 'amdahl-{}-percent.png'.format(parallel_percent)
plt.savefig(filename, dpi=400, bbox_inches='tight')
