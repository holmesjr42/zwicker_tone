import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nnm_plot as nnp
from tools import nn_tool as nt
from parameter import parameters as pm
import pandas as pd
# import pylustrator
import matplotlib.pyplot as plt

# pylustrator.start()
sys.path.pop(1)

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

# file_input = snakemake.input
# file_input = f'{path}/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/dataset/cr50_190724_offset.hdf5'
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
file_path = f'{path}/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/dataset/'
files = [file_path + i for i in os.listdir(file_path)]

# condition setups
cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
t_ind = [pm.Nn.ind_3_1, pm.Nn.ind_1_1]
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
lvs = ['70', '60']  # spl db you are going to use
group = {}
types = ['spk', 'lfp']
cd = cond[0]
ch = np.arange(0, 16).reshape(4, 4)
st = [[2950, 3150], [950, 1150]]
lt = [
    [nt.lfp_index(2950), nt.lfp_index(3150)],
    [nt.lfp_index(950), nt.lfp_index(1150)]
]
time = [st, lt]
bfd = pm.Commonfeat.bf_dic
offs = [[] for _ in range(2)]
bf = [[] for _ in range(2)]
print(os.listdir(file_path))
for file_input in files:
    with h5py.File(file_input, 'r') as dat:
        animal = file_input.split('/')[-1].split('_')[0]
        a = nt.Offset(dat, file_input, cd[0], '70')
        th = a.threshold()

        for c in range(len(cd)):
            spk = dat['spk'][cd[c]]['smooth_psth'][0]
            lfp = dat['lfp'][cd[c]]['mean'][0]

            sc = 0
            lc = 0

            for ch in range(len(spk)):
                # print(spk[ch][st[0][0]:st[0][1]])
                # print(th[0][ch])
                if any(spk[ch][st[0][0]:st[0][1]] >= th[0][ch]):
                    sc = sc + 1
                else:
                    pass

                # if any(lfp[ch][lt[0][0]:lt[0][1]] < th[1][ch]):
                #     lc = lc + 1
                # else:
                #     pass

            if sc * 100 / 16 >= 60:
                off = 1
            else:
                off = 0

            offs[c].append(off)
            bf[c].append(bfd[animal])

print(offs, bf)
# fig = plt.figure()
# plt.plot(bf[0], offs[0])
# plt.show()
#     n_spk = dat['spk'][cd[0]]['smooth_psth'][0]
#     n_lfp = dat['lfp'][cd[0]]['mean'][0]
#     w_spk = dat['spk'][cd[1]]['smooth_psth'][0]
#     w_lfp = dat['lfp'][cd[1]]['mean'][0]
#     data = [[n_spk, w_spk]]
#
#     for k in range(len(data)):
#         figs = plt.figure()
#         axs = figs.subplots(4, 4)
#         dat = data[k]
#         tt = time[k]
#         for i in range(4):
#             for j in range(4):
#                 h = ch[i][j]
#                 t = np.linspace(tt[0][0], tt[0][1], len(dat[0][h][tt[0][0]:tt[0][1]]))
#                 axs[i, j].plot(t, dat[0][h][tt[0][0]:tt[0][1]], color='blue')
#                 axs[i, j].plot(t, dat[1][h][tt[0][0]:tt[0][1]], color='orange')
#                 axs[i, j].axhline(th[k][h], color='k')
#
# plt.show()
# plt.savefig(snakemake.output[k], dpi=150)
# plt.clf()
