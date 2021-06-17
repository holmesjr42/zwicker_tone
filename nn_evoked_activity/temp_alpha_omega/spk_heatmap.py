import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from tools import nnm_plot as nnmp
import pylustrator
import quantities as pq

# pylustrator.start()
sys.path.pop(1)

'''
Create heatmap for firing rate
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat


# some setups for plotting e.g. color scheme
val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr122b_210604_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = sets[-8][1]
c_w = sets[-6][0]
c_c = 'strf_1'
lfp = {}  # dict for spk data regarding SPLdB
chs = 8

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [
        dat['spk'][c_c], dat['spk'][c_n]['nn'],
        dat['spk'][c_n]['si']
         ]  # lfp

    for i in lvl:
        lfp[i] = [np.array(lp[0][i][chs]), np.array(lp[1][i][chs]),
                  np.array(lp[2][i][chs])] * pq.ms**(-1)
        lfp[i].units = pq.s**(-1)

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
# print(lvp)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(20, 16))

s_axs = s_fig.subplots(4, 3)

title = sets[6][0:3]  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(data)):
        nnmp.nnm_plot(
            axes[j], data[j], s_img, ccmap, type='frequency', cf=11314
            )
        if j != 0:
            axes[j].axes.yaxis.set_ticklabels([])

    if i != 3:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    axes[0].text(0, 0, f'{lvp[i]} dB',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=axes[0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

# unit text
s_axs[0, 0].text(0, 0, 'Frequency (kHz)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

s_axs[2, 0].text(0, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[2, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

mx = nnmp.norm_color(s_img, 'spk', 0.8)

# colorbar setup
for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'spk', vmax=mx[1], vmin=mx[0],
            ori='horizontal'
            )

#% start: automatic generated code from pylustrator
# plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
# import matplotlib as mpl
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.329825, 0.177299, 0.362493, 0.022656])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.329825, 0.190525, 0.362493, 0.022656])
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).axes[0].set_position([0.329825, 0.741065, 0.111148, 0.138935])
# plt.figure(0).axes[0].texts[0].set_position([-0.790454, 0.494837])
# plt.figure(0).axes[0].texts[1].set_position([-0.430573, -1.156761])
# plt.figure(0).axes[2].set_position([0.581170, 0.741065, 0.111148, 0.138935])
# plt.figure(0).axes[3].set_position([0.329825, 0.586624, 0.111148, 0.138935])
# plt.figure(0).axes[3].texts[0].set_position([-0.790454, 0.494837])
# plt.figure(0).axes[4].set_position([0.456926, 0.586624, 0.111148, 0.138935])
# plt.figure(0).axes[5].set_position([0.581170, 0.586624, 0.111148, 0.138935])
# plt.figure(0).axes[6].set_position([0.329825, 0.433076, 0.111148, 0.138935])
# plt.figure(0).axes[6].texts[0].set_position([-0.790454, 0.494837])
# plt.figure(0).axes[6].texts[1].set_position([1.792979, -1.465230])
# plt.figure(0).axes[7].set_position([0.456926, 0.433076, 0.111148, 0.138935])
# plt.figure(0).axes[8].set_position([0.581170, 0.433076, 0.111148, 0.138935])
# plt.figure(0).axes[9].set_position([0.329825, 0.277742, 0.111148, 0.138935])
# plt.figure(0).axes[9].texts[0].set_position([-0.790454, 0.494837])
# plt.figure(0).axes[10].set_position([0.456926, 0.277742, 0.111148, 0.138935])
# plt.figure(0).axes[11].set_position([0.581170, 0.277742, 0.111148, 0.138935])
# #% end: automatic generated code from pylustrator
# plt.show()
plt.show()