import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
import seaborn as sns
import pylustrator

pylustrator.start()
sys.path.pop(1)

'''
Create heatmap for firing rate
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
sets = val.extra_setup()
lvl = com.db['lv']  # SPLdB list

file_input = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5',
              '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_wn_3_1.hdf5'
              ]
# file_input = snakemake.input[0]

# stimulus conditions for this script: 0, NN; 1, WN
conds = [
    [sets[-2][0], sets[-5][0], sets[-4][0]],
    [sets[-1][0], sets[-5][0], sets[-3][0]]
    ]
bc_map = [dcmap[1], dcmap[2], dcmap[4]]  # bar plot colour map
layer_name = sets[0]
l_list = sets[2]

spk = {}  # dict for spk data regarding SPLdB

# index list of low edge, high edge
finx = [sets[3][1], sets[3][3]]
paradigm = [sets[6][1:3], [sets[6][-1]]]
l_style = sets[5]

# coordination of cond sublist and paired test execution
k_list = [[1, 2], [2]]


diff = {}
quan = {}
d_list = [paradigm[0][0], paradigm[0][1], paradigm[1][0]]

for a in [diff, quan]:
    for i in layer_name:
        a[i] = {}
        for j in d_list:
            a[i][j] = []


# load file
for f in range(len(file_input)):
    file = file_input[f]
    kl = k_list[f]
    pdm = paradigm[f]
    cond = conds[f]
    with h5py.File(file, 'r') as dat:
        lp = dat['fps']
        for ln in range(len(l_list)):
            layer = l_list[ln]
            l_name = layer_name[ln]
            for lv in lvl:
                for k in range(len(kl)):
                    k1 = kl[k]
                    pdm1 = pdm[k]
                    # getting coord of nn condition. check cn for details
                    ctrl = cond[0]
                    cn = cond[k1]  # condition which you want to calculate
                    # difference
                    cnn = cond[1]  # nn-on to find frequency indice for each animal
                    # storing level-wise data temporarily.
                    # 3 indicates: median and 2 quartiles

                    teemp = nt.diff_on_off(
                        lp, layer, lv, cn, ctrl, cnn, types='spk'
                        )

                    diff[l_name][pdm1].append(teemp[0])
                    quan[l_name][pdm1].append([teemp[1], teemp[2]])

# plot start

b_fig = plt.figure(0, figsize=(16, 9))
b_axs = b_fig.subplots(1, 3)
x = np.arange(len(lvl))
width = 0.18
w_list = [-(width * 1.1), 0, width * 1.1]
for i in range(len(layer_name)):
    l_name = layer_name[i]
    for j in range(len(d_list)):
        cond = d_list[j]
        err = np.array(quan[l_name][cond])
        test = b_axs[i].bar(
            x + w_list[j], diff[l_name][cond],
            width, label=cond, color=bc_map[j]
            )
        for lv in x:
            ex = [lv + w_list[j], lv + w_list[j]]
            ey = err[lv]
            print(ex, ey)
            test2 = b_axs[i].plot(ex, ey, c='k')

    b_axs[i].set_xticks(x)
    b_axs[i].set_xticklabels(lvl)
    b_axs[i].set_ylim([-0.3, 4.5])
    b_axs[i].set_yticks(np.linspace(0, 3.5, 8, endpoint=True), minor=True)
    b_axs[i].set_yticks(np.linspace(0, 3, 4, endpoint=True))

    b_axs[i].tick_params(axis='y', which='major', labelsize=15)
    b_axs[i].tick_params(axis='x', which='major', labelsize=20)

b_axs[2].legend(prop={'size': 13},
                loc='upper left',
                bbox_to_anchor=(0, 1))

b_axs[0].text(0, 0.5, 'Ratio of changes\nto control',
              horizontalalignment='center',
              verticalalignment='center',
              rotation='vertical',
              transform=b_axs[0].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )

b_axs[1].text(0.5, 0, 'dB SPL',
              horizontalalignment='center',
              verticalalignment='center',
              # rotation='vertical',
              transform=b_axs[1].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )
#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.125000, 0.273333, 0.227941, 0.430000])
plt.figure(0).axes[0].texts[0].set_position([-0.279677, 0.523088])
plt.figure(0).axes[1].set_position([0.398529, 0.273333, 0.227941, 0.430000])
plt.figure(0).axes[1].texts[0].set_position([0.502742, -0.202691])
plt.figure(0).axes[2].set_position([0.672059, 0.273333, 0.227941, 0.430000])
#% end: automatic generated code from pylustrator
plt.show()