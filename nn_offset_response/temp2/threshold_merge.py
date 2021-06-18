import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np

# file_name = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/offset_mean_std_0.hdf5'

files = snakemake.input

group = {}
for file_input in files:
    with h5py.File(file_input, 'r') as dat:
        animal = list(dat.keys())
        for a in animal:
            group[a] = np.array(dat[a])

with h5py.File(snakemake.output[0], 'w') as h:
    for t in list(group.keys()):
        d1 = h.create_dataset(t, data=group[t])


