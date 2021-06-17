import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import seaborn as sns
import h5py

sys.path.pop(1)

np.random.seed(0)
a = np.random.randint(1, 50, size=10)
a = a.astype(float)
a[5] = np.nan
print(np.nanmax(a))
k = np.inf

