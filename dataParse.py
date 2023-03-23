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
import matplotlib.pyplot as plt
from datetime import datetime

graph = False # Set to True to see graph of data for debugging

# no need to add the extension of the file
filepath = "data/100ml_104_S12"

data = np.genfromtxt(filepath + ".txt", delimiter=",", names=True)

# Storing resistance as variable
timestamp = data['timestamp'] 
resistance = data['O2']
if (graph == True):
    plt.plot(resistance[:10000])
    plt.show()

conv_dt = [datetime.fromtimestamp(ts/1000) for ts in timestamp]

idxs, properties = sig.find_peaks(resistance,
                                  width=1000, #Default 1700
                                  distance=500, #Default 1000
                                  height=190000) #Default 54000

if not idxs.any():
    print("No peaks found")
    exit()

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

#plotting Data
pLim = 8
tLim = 8
x_limP = [idxs[i] for i in range(pLim)]
x_limT = [start_idx[i].item() for i in range(tLim)]

plt.plot(conv_dt[:25000], resistance[:25000])
plt.plot([conv_dt[i] for i in x_limP], resistance[idxs[:pLim]], "x")
plt.plot([conv_dt[i] for i in x_limT], resistance[start_idx[:tLim]], "o")
plt.show()

plt.plot(ratio)
plt.show()