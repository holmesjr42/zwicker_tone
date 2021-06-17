import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import pickle
from parameter import parameters as pm
import h5py
import quantities as pq
from tools import spike_tools as st

sys.path.pop(1)

file_input = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
              "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
              "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
              "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
              ".hdf5"
              ]

type = ['lfp,', 'tsp']
group = {'lfp': {}, 'spk': {}}
conds = ['nnm_3_0', 'nnm_3_0_strf']
db = ['70', '60', '50', '40']
ch = 16
cf = 12
for cond in conds:
    for d in db:
        a_temp = []
        for file in file_input:
            f_temp = []
            with h5py.File(file, 'r') as dat:
                spk = dat['tsp']
                for c in range(16):
                    f_temp.append(spk[cond][d][c][cf])

            a_temp.append(f_temp)

