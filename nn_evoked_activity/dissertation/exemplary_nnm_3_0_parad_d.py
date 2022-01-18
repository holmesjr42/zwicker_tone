import os
import sys
import pathlib

# add path to the tool directory to sys.path
tool_path = pathlib.Path(__file__).parents[2] / "nn_tool"
sys.path.insert(1, str(tool_path))

import platform
import numpy as np
import h5py
import matplotlib.pyplot as plt
from parameter import parameters as pm
from tools import nnm_plot as nnmp
import pylustrator
import quantities as pq

pylustrator.start()
sys.path.pop(1)

'''
Create heatmap for firing rate for nnm_3_0 exemplary animal cr 79
'''
s_fig = plt.figure(0, figsize=(12, 16))

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(hcmap_mode='spk', mode='fun')
# mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
#     val.values()
lvl = com.db['lv']  # SPLdB list
# sets = val.extra_setup()

# load data
data_path = 'OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
            '/data/dataset/nnm_spk_lfp_avg'
file_name = 'cr79_200211_spk_lfp_avg_nnm.hdf5'

partition = pm.data_path_selection()

file_input = os.path.join(partition, data_path, file_name)

# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = val.c_n[0]
c_s = val.c_s[0]
spk = {}  # dict for spk data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['tsp'][c_s], dat['tsp'][c_n]]  # spk

    for i in lvl:
        # 800 um is chosen for the representation
        spk[i] = [np.array(sk[0][i][8]), np.array(sk[1][i][8])] * pq.ms ** (-1)
        spk[i].units = pq.s ** (-1)

lvp = nnmp.db_lv(spk)  # SPL dB which actually has data
print(lvp)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 2)

col = [0, 2, 0, 2]  # location of ctrl and nn column
# row = [0, 0, 1, 1]  # location of each dB data
title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = spk[lvp[i]]
    axes = [s_axs[i, 0], s_axs[i, 1]]
    nnmp.nnm_plot(axes[0], data[0], s_img, val.hcmap, col_ref='k')
    nnmp.nnm_plot(axes[1], data[1], s_img, val.hcmap, col_ref='k')

    axes[1].axes.yaxis.set_ticklabels([])

    if i != 3:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    # Plot title

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    # SPL dB
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
mx = nnmp.norm_color(s_img, 'spk', 0.9)

for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'spk', vmax=mx[1], ori='horizontal'
            )

        if i != len(lvp) - 1:
            nnmp.remove_colorbar(s_fig)

plt.show()
