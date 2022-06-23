import os
import sys
import pathlib
import h5py

import numpy as np

import matplotlib.pyplot as plt
import pylustrator

# add path to the tool directory to sys.path
tool_path = pathlib.Path(__file__).parents[2] / "nn_tool"
sys.path.insert(1, str(tool_path))

from nn_tool.tools import nn_tools as nt
from nn_tool.parameter import parameters as pm

pylustrator.start()
sys.path.pop(1)

'''
spk/lfp difference rate comparison between NN and control with edge and band 
min/max 
freq.
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(hcmap_mode='spk', mode='fun')
# mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
#     val.values()
lvl = com.db['lv']  # SPLdB list

# load data
data_path = 'OneDrive\\Work\\PhD\\projects\\zwicker_tone_2018_2021' \
            '\\data\\dataset\\fp_layer'
file_name = 'fp_layer_nnm_3_0.hdf5'

partition = pm.data_path_selection()

file_input = os.path.join(partition, data_path, file_name)

# file_input = snakemake.input[0]

# stimulus conditions for this script
cn = val.c_n[0]
cs = val.c_s[0]

# layer name list and dic key list of layers
# layer_name = sets[0]
bc_map = [val.d_cmap[1], val.d_cmap[2], val.d_cmap[4]]  # bar plot colour map
layer_name = ['Supragranular layer', 'Granular layer', 'Infragranular layer']
l_list = val.l_list[2]

# index list of low edge, high edge
finx = [val.freq[1], val.freq[3]]

# line style for plots
l_style = val.l_style[5]

# dic for difference ratio and quartile 25/75
ratio = {'spk': {}, 'lfp': {}}
quan = {'spk': {}, 'lfp': {}}

r_list = list(ratio.keys())
r_name = ['SPK', 'LFP']
# load file
with h5py.File(file_input, 'r') as dat:
    # spk, lfp, baseline data
    data = [dat['fps'], dat['fpl'], dat['base']]
    for d in range(len(r_list)):
        for layer in l_list:
            ratio[r_list[d]][layer] = []
            quan[r_list[d]][layer] = []
            for lv in lvl:
                temp = nt.diff(
                    data[d], layer, lv, cn, cs,
                    bdata=data[2], types=r_list[d], fqtype='center'
                    )

                ratio[r_list[d]][layer].append(temp[0])
                quan[r_list[d]][layer].append([temp[1], temp[2]])

# plot start

b_fig = plt.figure(0, figsize=(13, 9))
b_axs = b_fig.subplots(1, 2)
x = np.arange(len(lvl))
width = 0.2
w_list = [-(width * 1.1), 0, width * 1.1]
ylim = [[-0.5, 2.5], [-0.3, 1.2]]
# ylim = [[-0.25, 1.3], [-0.01, 1.0]]
for i in range(len(r_list)):
    for j in range(len(layer_name)):
        lab = layer_name[j]
        cond = l_list[j]
        err = np.array(quan[r_list[i]][cond])
        test = b_axs[i].bar(
            x + w_list[j], ratio[r_list[i]][cond],
            width, label=lab, color=bc_map[j]
            )

        for lv in x:
            ex = [lv + w_list[j], lv + w_list[j]]
            ey = err[lv]
            print(ex, ey)
            test2 = b_axs[i].plot(ex, ey, c='k')

    b_axs[i].set_xticks(x)
    b_axs[i].set_xticklabels(lvl)
    b_axs[i].set_ylim([ylim[i][0], ylim[i][1]])
    # b_axs[i].set_yticks(np.linspace(0, 3.5, 8, endpoint=True), minor=True)
    # b_axs[i].set_yticks(np.linspace(0, 3, 4, endpoint=True))

    b_axs[i].tick_params(axis='y', which='major', labelsize=15)
    b_axs[i].tick_params(axis='x', which='major', labelsize=20)

b_axs[0].legend(
    prop={'size': 13},
    loc='upper left',
    bbox_to_anchor=(0, 1)
    )

b_axs[0].text(
    0, 0.5, 'Ratio of changes\nto control',
    horizontalalignment='center',
    verticalalignment='center',
    rotation='vertical',
    transform=b_axs[0].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

b_axs[0].text(
    0.5, 0, 'dB SPL',
    horizontalalignment='center',
    verticalalignment='center',
    # rotation='vertical',
    transform=b_axs[0].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

b_axs[0].text(
    0.5, 1, 'SPK',
    horizontalalignment='center',
    verticalalignment='center',
    rotation='horizontal',
    transform=b_axs[0].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

b_axs[1].text(
    0, 0.5, 'Ratio peak to peak\nchanges to control',
    horizontalalignment='center',
    verticalalignment='center',
    rotation='vertical',
    transform=b_axs[1].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

b_axs[1].text(
    0.5, 0, 'dB SPL',
    horizontalalignment='center',
    verticalalignment='center',
    # rotation='vertical',
    transform=b_axs[1].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

b_axs[1].text(
    0.5, 1, 'LFP',
    horizontalalignment='center',
    verticalalignment='center',
    rotation='horizontal',
    transform=b_axs[1].transAxes,
    fontdict={'weight': 'bold', 'size': 25}
    )

plt.show()
