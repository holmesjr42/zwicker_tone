import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import matplotlib.pyplot as plt
from parameters import parameters as pm
import h5py
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

# file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
#              '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5'

# file_input = snakemake.input[0]

# stimulus conditions for this script
cc = sets[-2][0]
cnn = sets[-5][0]
cnf = sets[-4][0]
cwf = sets[-3][0]
paradigm = sets[6]
l_list = sets[2]
spk = [[] for _ in range(3)]  # list for spk data regarding layers
stat = {}  # dict for stat regarding layers
octs = com.octaves  # list of octaves
# list of layer names
layer_name = sets[0]

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]

# asterisk color
c_as = '#404040'

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [
        dat['fps'][cc], dat['fps'][cnn], dat['fps'][cnf], dat['fps'][cwf]
        ]  #
    for l in range(len(l_list)):
        ly = l_list[l]
        stat[ly] = {}
        for lv in lvl:
            # list of the max/min spk/lfp frequency in nn band
            fm = []

            spk[l].append([
                np.mean(sk[0][ly][lv], axis=0), np.mean(sk[1][ly][lv], axis=0),
                np.mean(sk[2][ly][lv], axis=0), np.mean(sk[3][ly][lv], axis=0)
                ])
            dt = sk[1][ly][lv]
            for a in range(len(dt)):
                fm.append(nt.freq_find(dt[a], find))
            d_test = [
                sk[0][ly][lv], sk[1][ly][lv], sk[2][ly][lv], sk[3][ly][lv]
                ]
            test = nt.fp_friedman(d_test, fm)
            stat[ly][lv] = test

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(3, 4)
lim_max = [235, 270, 220]
lim_tick = [[201, 50], [251, 50], [201, 50]]

for i in range(len(lvl)):
    for j in range(len(l_list)):
        data = spk[j][i]
        stat2 = stat[l_list[j]][lvl[i]]
        s_axs[j, i].axvspan(-0.5, 0.5, alpha=0.3, color='#bccbe3', zorder=0)

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[0], label='Control',
                         color=dcmap[0], linestyle='-', linewidth=3, zorder=1
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[1], label='NN-ON',
                         color=dcmap[1], linestyle='--', linewidth=3, zorder=2
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[2], label='NN-OFF',
                         color=dcmap[2], linestyle='-.', linewidth=3, zorder=4
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[3], label='WN-OFF',
                         color=dcmap[4], linestyle=(0, (1, 1)), linewidth=3,
                         zorder=3
                         )

        if stat2[1] < 0.05:
            x = stat2[0]
            s_axs[j, i].scatter(
                octs[x],
                np.max([
                    data[0][x], data[1][x], data[2][x], data[3][x]
                    ]) + lim_tick[j][1] * 0.5,
                marker=(5, 2), color=c_as, zorder=5
                                )

        s_axs[j, i].set_xticks([-1.5, -0.5, 0, 0.5, 1.5])

        # ticks
        s_axs[j, i].set_ylim([0, lim_max[j]])
        s_axs[j, i].set_yticks(np.arange(0, lim_tick[j][0], lim_tick[j][1]))
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

s_axs[0, 0].legend(prop={'size': 11},
                   loc='upper left',
                   bbox_to_anchor=(0, 1))

s_axs[1, 2].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 2].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[0, 0].text(0, 0, 'Firing rate (spk / s)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[1, 3].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].texts[0].set_position([0.508226, 1.157865])
plt.figure(0).axes[0].texts[1].set_position([-0.485967, 0.559307])
plt.figure(0).axes[0].texts[2].set_position([-3.839516, 0.539683])
plt.figure(0).axes[1].texts[0].set_position([0.474839, 1.157865])
plt.figure(0).axes[2].texts[0].set_position([0.497097, 1.157865])
plt.figure(0).axes[3].texts[0].set_position([0.504516, 1.157865])
plt.figure(0).axes[4].texts[0].set_position([-0.485967, 0.495527])
plt.figure(0).axes[6].texts[0].set_position([-0.107581, -1.506205])
plt.figure(0).axes[8].texts[0].set_position([-0.485967, 0.534776])
#% end: automatic generated code from pylustrator
plt.show()
