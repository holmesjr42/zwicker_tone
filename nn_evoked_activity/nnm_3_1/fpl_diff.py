import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import json
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
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
val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
sets = val.extra_setup()
lvl = com.db['lv']  # SPLdB list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
nconds = [sets[-5][0], sets[-4][0], sets[-3][0]]
cconds = [sets[-2][0], sets[-2][0], sets[-1][0]]

layer_name = sets[0]
l_list = sets[2]

# index of low edge, center, high edge, 0.5 oct above/below  of notch gap
mid = sets[3][2]
paradigm = sets[6][1:]
l_style = sets[5]

ratio = {}


# load file
with h5py.File(file_input, 'r') as dat:
    ind = mid
    lfp = dat['fpl']
    base = dat['base']
    for layer in l_list:
        ratio[layer] = []

        for c in range(len(nconds)):
            cn = nconds[c]
            cs = cconds[c]
            templv = [[] for _ in range(3)]
            # storing level-wise data temporarily.
            # 3 means: median and 2 quartiles

            for lv in lvl:
                teemp = nt.diff(
                    lfp, layer, lv, cn, cs, bdata=base,
                    types='lfp'
                    )
                for i in range(3):
                    templv[i].append(teemp[i])
            ratio[layer].append(templv)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(1, 3)
xs = np.arange(len(lvl))

# ticks
# ticks
maps = [1, 2, 4]  # color selection
for j in range(len(l_list)):
    ls = l_list[j]
    for i in range(len(paradigm)):

        s_axs[j].plot(xs, ratio[ls][i][0],
                      color=dcmap[maps[i]],
                      label=paradigm[i],
                      lw=5,
                      linestyle=l_style[i], zorder=2)

        s_axs[j].fill_between(xs,
                              ratio[ls][i][1],
                              ratio[ls][i][2],
                              color=dcmap[maps[i]], zorder=2, alpha=0.1)

        # s_axs[j].set_yticks(np.arange(-0.02, 0.13, 0.02))
        # s_axs[j].set_ylim(-0.03, 0.13)

for i in range(len(layer_name)):
    # s_axs[i].text(0.5, 0, layer_name[i],
    #               horizontalalignment='center',
    #               verticalalignment='center',
    #               # rotation='vertical',
    #               transform=s_axs[i].transAxes,
    #               fontdict={'weight': 'bold', 'size': 25}
    #               )
    s_axs[i].set_ylim(-.5, 2.0)
    s_axs[i].set_xticks(xs)
    s_axs[i].set_xticklabels(['70', '60', '50', '40'])
    s_axs[i].tick_params(axis='y', which='major', labelsize=15)
    s_axs[i].tick_params(axis='x', which='major', labelsize=20)
    s_axs[i].axhline(y=0, c='k', lw=1.5, alpha=0.5, linestyle='dotted',
                     zorder=1)

s_axs[2].legend(prop={'size': 10},
                loc='upper left',
                bbox_to_anchor=(0, 1))

s_axs[0].text(0, 0.5, 'Ratio peak to peak',
              horizontalalignment='center',
              verticalalignment='center',
              rotation='vertical',
              transform=s_axs[0].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )

s_axs[1].text(0.5, 0, 'dB SPL',
              horizontalalignment='center',
              verticalalignment='center',
              # rotation='vertical',
              transform=s_axs[1].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.118750, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[0].texts[0].set_position([-0.273522, 0.493058])
plt.figure(0).axes[1].set_position([0.398622, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[1].texts[0].set_position([0.513715, -0.185238])
plt.figure(0).axes[2].set_position([0.678248, 0.383202, 0.227854, 0.384952])
#% end: automatic generated code from pylustrator
plt.show()