import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from matplotlib.colors import ListedColormap
from tools import nnm_plot as nnmp
import pylustrator
import quantities as pq
from tools import nn_tool as nt

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

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cc = sets[-2][0]
cnn = sets[-5][0]
cnf = sets[-4][0]
cwf = sets[-3][0]

# control, nn-on, nn-off, wn-off
paradigm = sets[6]
l_n = sets[1]
l_list = sets[2]
octs = com.octaves  # list of octaves
# list of layer names
layer_name = sets[0]

lfp = [[] for _ in range(3)]  # list for lfp data regarding layers
stat = {}  # dict for stat regarding layers

# asterisk color
c_as = '#404040'

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['fpl'][cc], dat['fpl'][cnn],
          dat['fpl'][cnf], dat['fpl'][cwf]]  # spk

    for l in range(len(l_list)):
        ly = l_list[l]
        stat[ly] = {}
        for lv in lvl:
            # list of the max/min spk/lfp frequency in nn band
            fm = []

            lfp[l].append([
                np.mean(lp[0][ly][lv], axis=0), np.mean(lp[1][ly][lv], axis=0),
                np.mean(lp[2][ly][lv], axis=0), np.mean(lp[3][ly][lv], axis=0)
                ])
            dt = lp[1][ly][lv]
            for a in range(len(dt)):
                fm.append(nt.freq_find(dt[a], find, type='lfp'))
            d_test = [
                lp[0][ly][lv], lp[1][ly][lv], lp[2][ly][lv], lp[3][ly][lv]
                ]
            test = nt.fp_friedman(d_test, fm)
            stat[ly][lv] = test


# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(3, 4)
lim_min = [[-0.22, 0.01], [-0.15, 0.01], [-0.093, 0.005]]
lim_tick = [[-0.20, 0.001, 0.05], [-0.12, 0.01, 0.04], [-0.08, 0.001, 0.02]]

for i in range(len(lvl)):
    for j in range(len(l_list)):
        data = lfp[j][i]
        stat2 = stat[l_list[j]][lvl[i]]
        s_axs[j, i].axvspan(-0.5, 0.5, alpha=0.3, color='#bccbe3', zorder=0)

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[0], label=paradigm[0],
                         color=dcmap[0], linestyle='-', linewidth=3, zorder=1
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[1], label=paradigm[1],
                         color=dcmap[1], linestyle='--', linewidth=3, zorder=2
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[2], label=paradigm[2],
                         color=dcmap[2], linestyle='-.', linewidth=3, zorder=4
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[3], label=paradigm[3],
                         color=dcmap[4], linestyle=(0, (1, 1)), linewidth=3,
                         zorder=3
                         )

        s_axs[j, i].set_xticks([-1.5, -0.5, 0, 0.5, 1.5])

        if stat2[1] < 0.05:
            x = stat2[0]
            s_axs[j, i].scatter(
                octs[x],
                np.min([
                    data[0][x], data[1][x], data[2][x], data[3][x]
                    ]) - lim_tick[j][2] * 0.5,
                marker=(5, 2), color=c_as, zorder=5
                                )


        s_axs[j, i].set_ylim([lim_min[j][0], lim_min[j][1]])
        s_axs[j, i].set_yticks(np.arange(
           lim_tick[j][0], lim_tick[j][1], lim_tick[j][2]
            ))

        s_axs[j, i].set_xticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5], minor=True)
        s_axs[j, i].set_xticks([-1., 0., 1.])
        s_axs[j, i].set_xlim([-1.5, 1.5])
        s_axs[j, i].tick_params(axis='both', which='major', labelsize=15)
        s_axs[j, i].label_outer()

        if j == 0:
            s_axs[j, i].text(0, 0, f'{lvl[i]} dB',
                             horizontalalignment='center',
                             verticalalignment='center',
                             # rotation='vertical',
                             transform=s_axs[j, i].transAxes,
                             fontdict={'weight': 'bold', 'size': 25}
                             )

        if i == 0:
            s_axs[j, i].text(0, 0, layer_name[j],
                             horizontalalignment='center',
                             verticalalignment='center',
                             rotation='vertical',
                             transform=s_axs[j, i].transAxes,
                             fontdict={'size': 15}
                             )

s_axs[2, 3].legend(prop={'size': 11},
                   loc='lower left',
                   bbox_to_anchor=(0, 0))

s_axs[1, 2].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 2].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[0, 0].text(0, 0, 'Amplitude (mV)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[1, 3].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].texts[0].set_position([0.508226, 1.236364])
plt.figure(0).axes[0].texts[1].set_position([-0.534749, 0.558907])
plt.figure(0).axes[0].texts[2].set_position([-3.928548, 0.539683])
plt.figure(0).axes[1].texts[0].set_position([0.474839, 1.236364])
plt.figure(0).axes[2].texts[0].set_position([0.497097, 1.236364])
plt.figure(0).axes[3].texts[0].set_position([0.504516, 1.236364])
plt.figure(0).axes[4].texts[0].set_position([-0.534193, 0.495527])
plt.figure(0).axes[6].texts[0].set_position([-0.159516, -1.506205])
plt.figure(0).axes[8].texts[0].set_position([-0.534193, 0.534776])
#% end: automatic generated code from pylustrator
plt.show()
