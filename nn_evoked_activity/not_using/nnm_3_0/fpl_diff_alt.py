import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
import pylustrator
from tools import nn_tool as nt

pylustrator.start()
sys.path.pop(1)

'''
Difference rate comparison between NN and control with edge and band min/max 
freq.
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cn = sets[7][0]
cs = sets[8][0]

layer_name = sets[0]
l_list = sets[2]

# index list of low edge, center, high edge, 0.5 oct above/below  of notch gap
finx = [sets[3][1], sets[3][3]]

# name list for low, center high edge frequecies
f_name = [sets[4][0], sets[4][2]]
c_name = sets[4][1]

l_style = [sets[5][0], sets[5][2]]

# dic for difference ratio and quartile 25/75
ratio = {}
ratioc = {}

# load file
with h5py.File(file_input, 'r') as dat:
    lfp = dat['fpl']  # lfp
    base = dat['base']
    for layer in l_list:
        ratio[layer] = []
        for ind in finx:
            templv = [[] for _ in range(3)]
            templvc = [[] for _ in range(3)]
            # list storing level-wise data temporarily
            # 3 means: median and 2 quartiles
            for lv in lvl:
                teemp = nt.diff(
                    lfp, layer, lv, cn, cs, ind=ind, bdata=base, types='lfp')
                for i in range(3):
                    templv[i].append(teemp[i])
            ratio[layer].append(templv)

        for lv in lvl:
            teempc = nt.diff(lfp, layer, lv, cn, cs, bdata=base,
                             types='lfp', fqtype='center')
            for i in range(3):
                templvc[i].append(teempc[i])
        ratioc[layer] = templvc

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(1, 3)
xs = np.arange(len(lvl))

# ticks
maps = [1, 4]  # plot color selection
mapc = 2

for j in range(len(l_list)):
    ls = l_list[j]
    for i in range(len(f_name)):
        ftext = f_name[i]
        s_axs[j].plot(xs, ratio[ls][i][0],
                      color=dcmap[maps[i]],
                      label=f_name[i],
                      lw=5,
                      linestyle=l_style[i], zorder=2)

        s_axs[j].fill_between(xs,
                              ratio[ls][i][1],
                              ratio[ls][i][2],
                              color=dcmap[maps[i]], zorder=2, alpha=0.1)

    # min within band
    s_axs[j].plot(xs, ratioc[ls][0],
                  color=dcmap[mapc],
                  label=c_name,
                  lw=5,
                  linestyle=sets[5][1], zorder=2)

    s_axs[j].fill_between(xs,
                          ratioc[ls][1],
                          ratioc[ls][2],
                          color=dcmap[mapc], zorder=2, alpha=0.1)

    s_axs[j].set_yticks(np.arange(-1.2, 1.3, 0.4))
    s_axs[j].set_ylim(-1.3, 1.3)

# extra texts
for i in range(len(layer_name)):
    # s_axs[i].text(0.5, 0.9, layer_name[i],
    #               horizontalalignment='center',
    #               verticalalignment='center',
    #               # rotation='vertical',
    #               transform=s_axs[i].transAxes,
    #               fontdict={'weight': 'bold', 'size': 25}
    #               )

    s_axs[i].set_xticks(np.arange(4))

    s_axs[i].set_xticklabels(['70', '60', '50', '40'])
    s_axs[i].tick_params(axis='y', which='major', labelsize=15)
    s_axs[i].tick_params(axis='x', which='major', labelsize=20)
    s_axs[i].axhline(y=0, c='k', lw=1.5, alpha=0.5, linestyle='dotted',
                     zorder=1)

s_axs[2].legend(prop={'size': 10},
                loc='upper left',
                bbox_to_anchor=(0, 1))

s_axs[0].text(0, 0.5, 'Ratio peak to peak\nchanges to control',
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

# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl

plt.figure(0).axes[0].set_position([0.128125, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[0].texts[0].set_position([-0.311923, 0.478626])
plt.figure(0).axes[1].set_position([0.398622, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[1].texts[0].set_position([0.527430, -0.214101])
plt.figure(0).axes[2].set_position([0.666998, 0.383202, 0.227854, 0.384952])
# % end: automatic generated code from pylustrator

plt.show()
