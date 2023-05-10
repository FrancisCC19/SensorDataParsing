# Instructions on how to install venv
# Open file location in terminal
# Run the following commands
# 1) python -m venv .env
# 2) .env\Scripts\activate
# 3) pip install -r requirements.txt
# 4) Change file path and find_peak function before running code
# 5) python dataParse.py

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import *
from tkinter import ttk

root = Tk()
controlFrame = ttk.Frame(root, padding="3 3 12 12")
controlFrame.grid(column=0, row=0, sticky=(N, W, E, S))


def parseData():
    global idxs, ratio, start_idx, resistance, conv_dt
    status.set("Status: Processing")
    resistance = data[selColumn.get()]
    timestamp = data['timestamp']
    conv_dt = [datetime.fromtimestamp(ts/1000) for ts in timestamp]
    idxs, properties = sig.find_peaks(resistance,
                                      width=width.get(),  # Default 1700, set based on the debug graph
                                      distance=distance.get(),  # Default 1000, set based on the debug graph
                                      height=height.get())  # Default 54000, set based on the debug graph

    if not idxs.any():
        print("No peaks found")
        status.set("No peaks found")
        return

    start_idx = np.zeros([len(idxs), 1], dtype=int)
    for i in range(len(idxs)):
        # Find the trough to the left of the peak
        tmp = idxs[i]
        start_idx[i] = tmp
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

    idx_time = [conv_dt[i] for i in idxs]

    # save ratio as a csv file and text file
    save_file = filePath.get() + "_ratio"
    with open(save_file+".txt", "w") as f:
        for a, b in zip(idx_time, ratio):
            f.write(f"{a},{b}\n")
    status.set("Status: Done Parsing")


def graphData():
    resLim = 30000  # number of data points to plot
    pLim = 8  # number of peaks to plot
    tLim = 8  # number of troughs to plot
    x_limP = [idxs[i] for i in range(pLim)]
    x_limT = [start_idx[i].item() for i in range(tLim)]
    plt.plot(conv_dt[:resLim], resistance[:resLim])
    plt.plot([conv_dt[i] for i in x_limP], resistance[idxs[:pLim]], "x")
    plt.plot([conv_dt[i] for i in x_limT], resistance[start_idx[:tLim]], "o")
    plt.show()

    plt.plot(ratio)
    plt.show()


def setFilepath():
    global data
    status.set("Status: Processing")
    data = np.genfromtxt(filePath.get() + ".txt", delimiter=",", names=True)
    resistance = data[selColumn.get()]
    if (graph.get() == True):
        plt.plot(resistance[:10000])
        plt.show()
    status.set("Status: Set File Path")


# Filepath
filePath = StringVar()
selColumn = StringVar()
selColumn.set("O2")
filePath.set("data/")

ttk.Label(controlFrame, text="Filepath:").grid(column=2, row=0, sticky=W)
ttk.Label(controlFrame, text="Column:").grid(column=3, row=0, sticky=W)

filePathEntry = ttk.Entry(controlFrame, width=20, textvariable=filePath)
filePathEntry.grid(column=2, row=1, sticky=(W, E))

columnEntry = ttk.Entry(controlFrame, width=20, textvariable=selColumn)
columnEntry.grid(column=3, row=1, sticky=(W, E))

ttk.Button(controlFrame, text="Set Filepath",
           command=setFilepath).grid(column=4, row=1, sticky=W)

# Graph true or false button
graph = BooleanVar()
graphbutton = ttk.Checkbutton(controlFrame, text="Graph", variable=graph)
graphbutton.grid(column=5, row=1, sticky=W)

# Width Entry, distance entry, height entry
width = IntVar()
width.set(1700)
distance = IntVar()
distance.set(1000)
height = IntVar()
height.set(54000)

ttk.Label(controlFrame, text="Width:").grid(column=2, row=2, sticky=W)
ttk.Label(controlFrame, text="Distance:").grid(column=3, row=2, sticky=W)
ttk.Label(controlFrame, text="Height:").grid(column=4, row=2, sticky=W)

widthEntry = ttk.Entry(controlFrame, width=20, textvariable=width)
widthEntry.grid(column=2, row=3, sticky=(W, E))
distanceEntry = ttk.Entry(controlFrame, width=20, textvariable=distance)
distanceEntry.grid(column=3, row=3, sticky=(W, E))
heightEntry = ttk.Entry(controlFrame, width=20, textvariable=height)
heightEntry.grid(column=4, row=3, sticky=(W, E))

# Parse and graph button
ttk.Button(controlFrame, text="Parse", command=parseData).grid(
    column=2, row=4, sticky=W)
ttk.Button(controlFrame, text="Graph", command=graphData).grid(
    column=3, row=4, sticky=W)

# Status label
status = StringVar()
status.set("Status: Idle")
ttk.Label(controlFrame, textvariable=status).grid(column=2, row=5, sticky=W)

root.mainloop()
