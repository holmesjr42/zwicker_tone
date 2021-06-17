import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import h5py
from tools import nn_tool as nt
from parameter import parameters as pm
import matplotlib.pyplot as plt
import pylustrator
from scipy import stats

pylustrator.start()
# I'm going to use only 60 dB here

file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/" \
       "dataset/nn_mean/all_nn_mean.hdf5"

val = pm.Setup(cond2='tsp')

dbs, db, dcmap, names, leg, ch_l, l_list, layer_name = val.nn31_plot()

with h5py.File(file, 'r') as dat:
       lfp = dat['lfp']
       spk = dat['spk']

       n_fig = plt.figure(0, figsize=(16, 9))
       n_axs = n_fig.subplots(3, 4)

       for c in range(len(ch_l)):
              for k in range(len(leg[0]) + len(leg[1])):
                     print(k)