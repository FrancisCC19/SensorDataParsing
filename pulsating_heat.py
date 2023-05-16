import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from datetime import datetime

#Changeable Variable
filepath = "data/Heater_repsonse_01"
sep_val = 14000 # Value that separates the 1.8v to 2.5v peaks
pk_width = 50
pk_distance = 50
pk_height = 8000
trough_range = 2850

#Extracting Variable
# v25
# v18
# gradient
# trough_val

#Reading Data
data = np.genfromtxt(filepath+".txt", delimiter="\t", skip_header=True)

timestamp = data[:, 0]
conv_dt = [datetime.fromtimestamp(ts/1000) for ts in timestamp]

adc_value = data[:, 3]

#Finding Peaks
idxs = sig.find_peaks(adc_value,
                        width=pk_width, 
                        distance=pk_distance, 
                        height=pk_height)[0] 

if not idxs.any():
    print("No peaks found")
    exit()

#Splitting Peaks
v25 = [peak for peak in idxs if adc_value[peak] > sep_val]
v18 = [peak for peak in idxs if adc_value[peak] <= sep_val]

#Finding Troughs
trough_idxs = np.zeros([len(v18), 1], dtype=int)
for i in range(len(v18)):
    tmp = v18[i]
    trough_idxs[i] = tmp
    for j in range(trough_range):
        if adc_value[v18[i]] > adc_value[tmp]:
            trough_idxs[i] = tmp
        tmp += 1
        if tmp == len(adc_value):
            trough_idxs[i] = len(v18) - 1
            break

# tmp = v18[0]
# trough_idxs[0] = tmp
# for i in range(trough_range):
#     if adc_value[v18[0]] > adc_value[tmp]:
#         trough_idxs[0] = tmp
#         print(str(trough_idxs[0]) + " : " + str(adc_value[trough_idxs[0]]) + " : " + str(i))
#     tmp += 1
#     if tmp == len(adc_value):
#         print("This is the exit!")
#         trough_idxs[0] = len(v18) - 1
#         break

regions = np.vstack((v18, trough_idxs.T))
regions = regions.T
extracted_regions = [adc_value[start:end] for start, end in regions]
np.savetxt(filepath+"_gradient.txt", extracted_regions, delimiter=",", fmt="%.10g")

save_data = np.vstack((v18, trough_idxs.T, v25))
save_data = data.T
np.savetxt(filepath+"_parsed.txt", save_data, delimiter=",", fmt="%.10g")

trough_value = [adc_value[i] for i in trough_idxs]
time_t = [conv_dt[int(i)] for i in trough_idxs]

plt.plot(conv_dt, adc_value)
plt.plot([conv_dt[i] for i in v25], adc_value[v25], "x")
plt.plot([conv_dt[i] for i in v18], adc_value[v18], "x")
plt.plot(time_t, trough_value, "o")
plt.show()

