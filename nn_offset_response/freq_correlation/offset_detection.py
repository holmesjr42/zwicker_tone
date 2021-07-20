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
import seaborn as sns

# pylustrator.start()
sys.path.pop(1)

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))

# file_input = snakemake.input
# files = [f'{path}/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/dataset/cr50_190724_offset.hdf5']
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
file_path = f'{path}/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/dataset/'
files = [file_path + i for i in os.listdir(file_path)]

l_index = 1
c_index = 1
c_thrs = ['3_1', '1_1']
# condition setups
cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
t_ind = [pm.Nn.ind_3_1, pm.Nn.ind_1_1]
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
lvs = ['70', '60']  # spl db you are going to use
types = ['spk', 'lfp']
cd = cond[c_index]
ch = np.arange(0, 16).reshape(4, 4)
st = [[3000, 3150], [1000, 1150]]
lt = [
    [nt.lfp_index(2950), nt.lfp_index(3150)],
    [nt.lfp_index(950), nt.lfp_index(1150)]
]
time = [st, lt]
bfd = pm.Commonfeat.bf_dic
n_list = ['nn', 'wn']
n2_list = ['no_nn', 'no_wn']
group = {'condition': [], 'bf': []}

# print(os.listdir(file_path))
for file_input in files:
    with h5py.File(file_input, 'r') as dat:
        animal = file_input.split('/')[-1].split('_')[0]
        if cd[0] in list(dat['spk'].keys()):
            if len(dat['spk'][cd[0]]['smooth_psth']) - 1 >= l_index:
                print(animal)
                a = nt.Offset(dat, file_input, c_thrs[c_index], lvs[l_index])
                th = a.threshold()
                tha = a.threshold_alt()
                for c in range(len(cd)):
                    spk = dat['spk'][cd[c]]['smooth_psth'][l_index]
                    lfp = dat['lfp'][cd[c]]['mean'][l_index]

                    sc = 0
                    lc = 0

                    for ch in range(len(spk)):

                        # print(th[0][ch])
                        if any(spk[ch][st[c_index][0]:st[c_index][1]] >= tha[0][ch]):
                            sc += 1
                            # print(ch, animal, cd[c], lvs[l_index])
                        else:
                            continue

                        # if any(lfp[ch][lt[0][0]:lt[0][1]] < th[1][ch]):
                        #     lc = lc + 1
                        # else:
                        #     pass

                    if sc * 100 / 16 >= 30:
                        group['condition'].append(n_list[c])
                        group['bf'].append(bfd[animal] / 1000)
                        # print(animal, bfd[animal], n_list[c])
                        # print(animal, n_list[c])
                    else:
                        group['condition'].append(n2_list[c])
                        group['bf'].append(bfd[animal] / 1000)
                        # print('no', animal, bfd[animal], n_list[c])
                        continue

df = pd.DataFrame(group, columns=list(group.keys()))
print(
    np.count_nonzero(df['condition'] == 'nn'), np.count_nonzero(df['condition'] == 'wn'),
    np.count_nonzero(df['condition'] == 'no_nn'), np.count_nonzero(df['condition'] == 'no_wn')
)
# print(df)
# fig = plt.figure()
# ax = sns.stripplot(x='condition', y='bf', data=df, order=['nn', 'no_nn', 'wn', 'no_wn'], linewidth=1, size=5)
# ax.axhline(7.9)
# plt.show()
# plt.scatter(np.array(bf[0])/1000, np.array(offs[0]))
# plt.scatter(np.array(bf[0])/1000, np.array(offs[1]) + 0.05)
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
