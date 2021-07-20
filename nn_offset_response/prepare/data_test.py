import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nnm_plot as nnp
from tools import nn_tool as nt
from parameter import parameters as pm
# import pylustrator
import matplotlib.pyplot as plt
# pylustrator.start()
sys.path.pop(1)

# file_spk = snakemake.input.spk
# file_lfp = snakemake.input.lfp
# file_spk = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr90_201023_tsp.hdf5'
# file_lfp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr90_201023_lfp_fil.hdf5'
file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']

# condition setups
cond = ['nn_3_1', 'nn_wn_3_1', 'nn_1_1', 'nn_wn_1_1']

with h5py.File(file_spk[0], 'r') as dat:
    print(np.shape(dat[cond[0]]))
