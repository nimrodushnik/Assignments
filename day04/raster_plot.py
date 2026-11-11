
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import re

# Select MATLAB file
file = filedialog.askopenfilename(filetypes=[("MAT files", "*.mat")])
if not file:
    exit()

data = sio.loadmat(file, simplify_cells=True)
fs = 1000

# Find and sort trials
trial_names = sorted(
    [name for name in data if re.fullmatch(r"Trial\d+", name)],
    key=lambda name: int(name[5:])
)

# Plot licks
plt.figure()

for i, name in enumerate(trial_names, start=1):
    licks = np.ravel(data[name]["AnalogData"]["Button"]["Btn1"])

    lick_idx = np.where(np.diff(np.r_[0, licks]) == 1)[0]
    lick_times = lick_idx / fs

    plt.plot(lick_times, [i] * len(lick_times), "k.", markersize=4)

# Odor markers
plt.axvline(0, color="red", linestyle="--", label="Odor Start")
plt.axvline(2, color="red", linestyle="--", label="Odor End")

plt.xlim(-0.01, 7)
plt.ylim(len(trial_names), 1)
plt.yticks([1, 50, 100, 150, 200])
plt.xlabel("Time (s)")
plt.ylabel("Trial #")
plt.title("Lick Raster Plot")
plt.grid(True)
plt.legend()
plt.show()
