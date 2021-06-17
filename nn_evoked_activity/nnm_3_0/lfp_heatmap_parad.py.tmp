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
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
c_n = sets[7][0]
c_s = sets[8][0]
lfp = {}  # dict for spk data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['lfp'][c_s], dat['lfp'][c_n]]  # spk

    for i in lvl:
        lfp[i] = [np.array(lp[0][i][8]), np.array(lp[1][i][8])] * pq.microvolt
        lfp[i].units = pq.mV

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
print(lvp)
# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 2)

# col = [0, 0, 1, 1]  # location of ctrl and nn column
# row = [0, 2, 0, 2]  # location of each dB data
title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    axes = [s_axs[i, 0], s_axs[i, 1]]
    nnmp.nnm_plot(axes[0], data[0], s_img, ccmap)
    nnmp.nnm_plot(axes[1], data[1], s_img, ccmap)
    axes[1].axes.yaxis.set_ticklabels([])

    if i != 3:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    # Plot title

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    # dB SPL
    axes[0].text(0, 0, f'{lvp[i]} dB',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=axes[0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

# unit text
# s_axs[0, 0].text(0, 0, 'octaves',
#                  horizontalalignment='center',
#                  verticalalignment='center',
#                  rotation='vertical',
#                  transform=s_axs[0, 0].transAxes,
#                  fontdict={'weight': 'bold', 'size': 30}
#                  )

s_axs[3, 0].text(0, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[3, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

# colorbar setup
mn = nnmp.norm_color(s_img, 'lfp', 0.8)
print(mn)
for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'lfp', vmax=mn[1], vmin=mn[0],
            ori='horizontal'
            )


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.323870, 0.090741, 0.502859, 0.018857])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.323870, 0.096574, 0.502859, 0.018857])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].yaxis.labelpad = 18.800000
plt.figure(0).axes[0].set_position([0.323870, 0.797609, 0.223188, 0.167391])
plt.figure(0).axes[0].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[1].set_position([0.603541, 0.797609, 0.223188, 0.167391])
plt.figure(0).axes[2].set_position([0.323870, 0.596739, 0.223188, 0.167391])
plt.figure(0).axes[2].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[3].set_position([0.603541, 0.596739, 0.223188, 0.167391])
plt.figure(0).axes[4].set_position([0.323870, 0.395870, 0.223188, 0.167391])
plt.figure(0).axes[4].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[5].set_position([0.603541, 0.395870, 0.223188, 0.167391])
plt.figure(0).axes[6].set_position([0.323870, 0.195000, 0.223188, 0.167391])
plt.figure(0).axes[6].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[6].texts[1].set_position([1.219697, -0.298701])
plt.figure(0).axes[7].set_position([0.603541, 0.195000, 0.223188, 0.167391])
#% end: automatic generated code from pylustrator
plt.show()
