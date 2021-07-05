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
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr103_201215_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr103_201215_lfp_fil.hdf5']
file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr31_190312_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr31_190312_lfp_fil.hdf5']
# condition setups
cond = ['nn_3_1', 'nn_wn_3_1', 'nn_1_1', 'nn_wn_1_1']  # conditions for offset response experiment

lvs = ['70', '60']  # spl db you are going to use
group = {}
types = ['spk', 'lfp']

for f in range(len(file_spk)):
    s_input = file_spk[f]
    l_input = file_lfp[f]
    s_ref = [[] for _ in range(len(cond))]
    l_ref = [[] for _ in range(len(cond))]
    animal = nnp.animal_name(s_input)
    group[animal] = {}
    a = nt.OffsetPrepare(s_input, l_input, '1_1')
    b = a.threshold()
    c = a.spk_psth()
print(1)

# with h5py.File(snakemake.output[0], 'w') as h:
#     for t0 in list(group.keys()):
#         d1 = h.create_group(t0)
#         for t1 in types:
#             d2 = d1.create_dataset(t1, data=group[t0][t1])
