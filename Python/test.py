import pandas as pd
import os
import numpy as np
dir_path = '/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/RID'
count = 0
for path in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path, path)):
        count += 1

ranches = np.arange(1,count+1)

for r in ranches:
    file = f"/Users/cherryleheu/Codes/NIDIS-Codes/H-RIP/RID/RID{r:03d}/RID{r:03d}_tmean.csv"

    # Read CSV
    df = pd.read_csv(file)

    # Drop last row
    df = df.iloc[:-1]

    # Save back (overwrite)
    df.to_csv(file, index=False)
