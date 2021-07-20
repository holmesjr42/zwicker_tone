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

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

file_input = snakemake.input.data
lv = snakemake.input.lv
condition = snakemake.input.condition
# file_input = f'{path}/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/dataset/cr50_190724_offset.hdf5'
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
# condition setups
if condition == '3_1':
    c_ind = 0
elif condition == '1_1':
    c_ind = 1
else:
    print('you did not choose condition from snakefile')
    raise ValueError

if lv == '70':
    l_ind = 0
elif lv == '60':
    l_ind = 1
else:
    print('you did not choose condition from snakefile')
    raise ValueError

cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
t_ind = [pm.Nn.ind_3_1, pm.Nn.ind_1_1]
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
lvs = ['70', '60']  # spl db you are going to use
group = {}
types = ['spk', 'lfp']
cd = cond[c_ind]
ch = np.arange(0, 16).reshape(4, 4)
st = [[2950, 3150], [1000, 1150]]
lt = [
    [nt.lfp_index(2950), nt.lfp_index(3150)],
    [nt.lfp_index(1000), nt.lfp_index(1150)]
]
time = [st, lt]
with h5py.File(file_input, 'r') as dat:
    a = nt.Offset(dat, file_input, condition, lv)
    th = a.threshold()
    tha = a.threshold_alt()
    # tha = a.thrshold_alt()
    n_spk = dat['spk'][cd[0]]['smooth_psth'][l_ind]
    n_lfp = dat['lfp'][cd[0]]['mean'][l_ind]
    w_spk = dat['spk'][cd[1]]['smooth_psth'][l_ind]
    w_lfp = dat['lfp'][cd[1]]['mean'][l_ind]
    data = [[n_spk, w_spk], [n_lfp, w_lfp]]

    for k in range(len(data)):
        figs = plt.figure()
        axs = figs.subplots(4, 4)
        dat = data[k]
        tt = time[k]
        for i in range(4):
            for j in range(4):
                h = ch[i][j]
                t = np.linspace(1000, 1150, len(dat[0][h][tt[1][0]:tt[1][1]]))
                axs[i, j].plot(t, dat[0][h][tt[1][0]:tt[1][1]], color='blue')
                axs[i, j].plot(t, dat[1][h][tt[1][0]:tt[1][1]], color='orange')
                axs[i, j].axhline(th[k][h], color='k')
                axs[i, j].axhline(tha[k][h], color='r')
        plt.savefig(snakemake.output[k], dpi=150)
        plt.clf()

