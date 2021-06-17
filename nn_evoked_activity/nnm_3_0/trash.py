import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import pickle
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
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()
octs = pm.Commonfeat.octaves  # list of octaves

# file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
#              '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'

# stimulus conditions for this script
cn = sets[7][0]
cs = sets[8][0]
layer_name = sets[0]
l_list = sets[2]
spk = [[] for _ in range(3)]  # list for spk data regarding layers
stat = {}  # dict for stat regarding layers

# indice of frequencies in octaves
find = [sets[3][1], sets[3][2], sets[3][-2]]
# foct = [octs[find[0]], octs[find[1]], octs[find[2]]]

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['fps'][cs], dat['fps'][cn]]
    for l in range(len(l_list)):
        ly = l_list[l]
        stat[ly] = {}
        for lv in lvl:
            stat[ly][lv] = []
            spk[l].append([
                np.mean(sk[0][ly][lv], axis=0),
                np.mean(sk[1][ly][lv], axis=0)
                ])
            for f in range(len(find)):
                test = nt.fp_wilcoxon([sk[0][ly][lv], sk[1][ly][lv]], find[f])
                stat[ly][lv].append(test)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(3, 4)

for j in range(len(l_list)):
    stat1 = stat[l_list[j]]
    for i in range(len(lvl)):
        stat2 = stat1[lvl[i]]
        data = spk[j][i]
        s_axs[j, i].axvspan(-0.5, 0.5, alpha=0.3, color='#bccbe3')
        s_axs[j, i].tick_params(axis='both', which='major',
                                labelsize=13, length=6, width=1.5)


        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[0], label='Control',
                         color=dcmap[0], linestyle='-', linewidth=3
                         )

        s_axs[j, i].plot(np.linspace(-1.5, 1.5, 25, endpoint=True),
                         data[1], label='NN',
                         color=dcmap[1], linestyle='--', linewidth=3
                         )
        for k in range(len(find)):
            if stat2[k][1] < 0.05:
                x = np.int(stat2[k][0])
                s_axs[j, i].scatter(octs[x],
                                    np.max([data[0][x], data[1][x]]) + 10,
                                    marker=(5, 2), color="k"
                                    )
            else:
                pass

        s_axs[j, i].set_xticks([-1.5, -0.5, 0, 0.5, 1.5])
        s_axs[j, i].set_xlim([-1.5, 1.5])

        # p-value asterisk
        # if pv[j] < 0.05:
        #     s_axs[j, i].scatter(0, data[1][j][12] * 1.05,
        #                         marker=(5, 2), c='black', alpha=0.7)

        if j == 0:
            s_axs[j, i].set_yticks(np.arange(0, 81, 20))
            s_axs[j, i].set_ylim([0, 87])
        elif j == 1:
            s_axs[j, i].set_yticks(np.arange(0, 161, 40))
            s_axs[j, i].set_ylim([0, 190])
        elif j == 2:
            s_axs[j, i].set_yticks(np.arange(0, 121, 30))
            s_axs[j, i].set_ylim([0, 125])


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
                             fontdict={'size': 17}
                             )

s_axs[0, 3].legend(prop={'size': 12},
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
# s_axs[j, i].label_outer()
# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl

plt.figure(0).axes[0].texts[0].set_position([0.500806, 1.152975])
plt.figure(0).axes[0].texts[1].set_position([-0.363548, 0.529871])
plt.figure(0).axes[0].texts[2].set_position([-4.232742, 0.470996])
plt.figure(0).axes[1].texts[0].set_position([0.497103, 1.152975])
plt.figure(0).axes[2].texts[0].set_position([0.504529, 1.152975])
plt.figure(0).axes[3].texts[0].set_position([0.508208, 1.152975])
plt.figure(0).axes[4].texts[0].set_position([-0.363548, 0.529870])
plt.figure(0).axes[6].texts[0].set_position([-0.100161, -1.520924])
plt.figure(0).axes[8].texts[0].set_position([-0.363548, 0.524964])
# % end: automatic generated code from pylustrator
# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}

# % end: automatic generated code from pylustrator
# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
plt.figure(0).axes[0].texts[1].set_position([-0.486523, 0.529934])
plt.figure(0).axes[0].texts[2].set_position([-3.872904, 0.470996])
plt.figure(0).axes[4].texts[0].set_position([-0.486523, 0.529593])
plt.figure(0).axes[8].texts[0].set_position([-0.486523, 0.525389])
# % end: automatic generated code from pylustrator
plt.show()
