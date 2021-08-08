import os
import sys

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
spk/lfp difference rate comparison between NN and control with edge and band 
min/max 
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

# layer name list and dic key list of layers
# layer_name = sets[0]
layer_name = ['Supragranular layer', 'Granular layer', 'Infragranular layer']
l_list = sets[2]

# index list of low edge, high edge
finx = [sets[3][1], sets[3][3]]

# line style for plots
l_style = sets[5]

# dic for difference ratio and quartile 25/75
ratio = {'spk': {}, 'lfp': {}}
r_list = list(ratio.keys())
r_name = ['SPK', 'LFP']
# load file
with h5py.File(file_input, 'r') as dat:
    # spk, lfp, baseline data
    data = [dat['fps'], dat['fpl'], dat['base']]
    for d in range(len(r_list)):
        for layer in l_list:
            temp = [[] for _ in range(3)]
            for lv in lvl:
                temp2 = nt.diff(
                    data[d], layer, lv, cn, cs,
                    bdata=data[2], types=r_list[d], fqtype='center'
                    )

                for i in range(3):
                    temp[i].append(temp2[i])

            ratio[r_list[d]][layer] = temp

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(1, 2)
xs = np.arange(len(lvl))

# ticks
maps = [1, 2, 4]  # plot color selection
yticks = [[-0.4, 2.1, 0.4], [-0.2, 1.1, 0.2]]
ylims = [[-0.45, 2.1], [-0.3, 1.1]]

for i in range(len(r_list)):
    dtype = r_list[i]
    data = ratio[dtype]
    for j in range(len(l_list)):
        lname = layer_name[j]
        s_axs[i].plot(
            xs, data[l_list[j]][0], color=dcmap[maps[j]],
            label=lname, lw=5, linestyle=l_style[j], zorder=2
            )

        s_axs[i].fill_between(xs,
                              data[l_list[j]][1],
                              data[l_list[j]][2],
                              color=dcmap[maps[j]], zorder=1, alpha=0.1)

    s_axs[i].set_yticks(np.arange(yticks[i][0], yticks[i][1], yticks[i][2]))
    s_axs[i].set_ylim(ylims[i][0], ylims[i][1])
#
    # extra texts
    s_axs[i].text(0.5, 1, r_name[i],
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='horizontal',
                  transform=s_axs[i].transAxes,
                  fontdict={'weight': 'bold', 'size': 25}
                  )

    s_axs[i].set_xticks(np.arange(4))
    s_axs[i].set_xticklabels(['70', '60', '50', '40'])
    s_axs[i].tick_params(axis='y', which='major', labelsize=15)
    s_axs[i].tick_params(axis='x', which='major', labelsize=20)
    s_axs[i].axhline(y=0, c='k', lw=1.5, alpha=0.5, linestyle='dotted',
                     zorder=1)

s_axs[0].legend(prop={'size': 12},
                loc='upper left',
                bbox_to_anchor=(0, 1))

s_axs[0].text(0, 0.5, 'Ratio of changes\nto control',
              horizontalalignment='center',
              verticalalignment='center',
              rotation='vertical',
              transform=s_axs[0].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )

s_axs[1].text(0, 0.5, 'Ratio of peak to peak\nchanges to control',
              horizontalalignment='center',
              verticalalignment='center',
              rotation='vertical',
              transform=s_axs[1].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.141250, 0.110000, 0.295276, 0.524934])
plt.figure(0).axes[0].texts[0].set_position([0.500000, 1.035983])
plt.figure(0).axes[0].texts[1].set_position([-0.218017, 0.500000])
plt.figure(0).axes[1].set_position([0.551477, 0.110000, 0.295276, 0.524934])
plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.035983])
plt.figure(0).axes[1].texts[1].set_position([-0.203200, 0.500000])
#% end: automatic generated code from pylustrator
plt.show()
