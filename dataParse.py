#Instructions on how to install venv
#Open file location in terminal
#Run the following commands
#1) python3 -m venv .env
#2) .env/bin/activate
#3) pip install -r requirements.txt
#4) python3 dataParse.py

import numpy as np
import scipy.signal as sig

filepath = "data/new_sensor_2sec_on_2min_off_3"

data = np.genfromtxt(filepath + ".txt", delimiter = ",", names = True)

#save the first coloumn and secound column as timestamp and resitance
timestamp = data['timestamp']
resistance = data['S15']

idxs, properties = sig.find_peaks(resistance, 
                     width = 1700, 
                     distance = 1000,
                     height = 54000)

rnge = np.zeros([len(idxs), 1], dtype=int)
for i in range(len(idxs)):
    #Finding Peak Start
    """tmp = idxs[i]
    while(True):
        if base - 2 < raw[tmp] and base + 2 > raw[tmp]: # if the value is within +/- 2 of the base value (right of the peak)
            rnge[i][0] = tmp
            break
        tmp -= 1"""
    #Finding Peak End
    tmp = idxs[i]
    for j in range(1500):
        if resistance[rnge[i]] > resistance[tmp]: # if the value is within +/- 2 of the base value (left of the peak)
            rnge[i] = tmp
        tmp += 1
        if tmp == len(resistance):
            rnge[i] = len(resistance) - 1
            break
#print(rnge)

ratio = np.zeros([len(idxs), 1], dtype=float)

for i in range(len(idxs)):
    ratio[i] = resistance[idxs[i]] / resistance[rnge[i]]

#save ratio as a csv file and text file
save_file = filepath + "_ratio"
np.savetxt(save_file+".txt", ratio, delimiter = ",")
np.savetxt(save_file+".csv", ratio, delimiter = ",")




