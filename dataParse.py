# Instructions on how to install venv
# Open file location in terminal
# Run the following commands
# 1) python -m venv .env
# 2) .env\Scripts\activate
# 3) pip install -r requirements.txt
# 4) Change file path before running code
# 5) python dataParse.py

import numpy as np
import scipy.signal as sig

# no need to add the extension of the file
filepath = "data/new_sensor_2sec_on_2min_off_3"

data = np.genfromtxt(filepath + ".txt", delimiter=",", names=True)

# save the first coloumn and secound column as timestamp and resitance
timestamp = data['timestamp']
resistance = data['S15']

idxs, properties = sig.find_peaks(resistance,
                                  width=1700,
                                  distance=1000,
                                  height=54000)

start_idx = np.zeros([len(idxs), 1], dtype=int)
for i in range(len(idxs)):
    # Find the trough to the left of the peak
    tmp = idxs[i]
    for j in range(1500):
        # if the value is within +/- 2 of the base value (left of the peak)
        if resistance[start_idx[i]] > resistance[tmp]:
            start_idx[i] = tmp
        tmp += 1
        if tmp == len(resistance):
            start_idx[i] = len(resistance) - 1
            break


ratio = np.zeros([len(idxs), 1], dtype=float)

for i in range(len(idxs)):
    ratio[i] = resistance[idxs[i]] / resistance[start_idx[i]]

# save ratio as a csv file and text file
save_file = filepath + "_ratio"
np.savetxt(save_file+".txt", ratio, delimiter=",")
np.savetxt(save_file+".csv", ratio, delimiter=",")
