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
# file_spk = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr31_190312_tsp.hdf5'
# file_lfp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr31_190312_lfp_fil.hdf5'

# condition setups
cond = ['nn_3_1', 'nn_wn_3_1', 'nn_1_1', 'nn_wn_1_1']  # conditions for offset response experiment
group = {'spk': {}, 'lfp': {}}
# cond = ['nn_1_1']
for c in cond:
    data = nt.OffsetPrepare(file_spk, file_lfp, c)
    spk = data.spk_psth()
    lfp = data.lfp_seg()

    if np.any(lfp[1][0][8]):
        group['spk'][c] = spk
        group['lfp'][c] = lfp
    else:
        continue

s_group = ['raster', 'psth', 'smooth_psth', 'time']
l_group = ['segments', 'mean', 'time']

with h5py.File(snakemake.output[0], 'w') as h:
    d1 = h.create_group('spk')
    for t1 in list(group['spk'].keys()):
        d2 = d1.create_group(t1)
        for t2 in range(len(s_group)):
            d3 = d2.create_dataset(s_group[t2], data=group['spk'][t1][t2])

    e1 = h.create_group('lfp')
    for v1 in list(group['spk'].keys()):
        e2 = e1.create_group(v1)
        for v2 in range(len(l_group)):
            e3 = e2.create_dataset(l_group[v2], data=group['lfp'][v1][v2])


