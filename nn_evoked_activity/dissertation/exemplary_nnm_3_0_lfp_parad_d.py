import os
import sys
import pathlib
import h5py

import numpy as np

import matplotlib.pyplot as plt
import pylustrator
import quantities as pq

# add path to the tool directory to sys.path
tool_path = pathlib.Path(__file__).parents[2] / "nn_tool"
sys.path.insert(1, str(tool_path))

from nn_tool.parameter import parameters as pm
from nn_tool.tools import nnm_plot as nnmp

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
val = pm.Setup(hcmap_mode='lfp', mode='fun')
ccmap = val.hcmap
lcolor = val.ref_line_color

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
lfp = {}  # dict for lfp data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['lfp'][c_s], dat['lfp'][c_n]]  # lfp

    for i in lvl:
        # 800 um is chosen for the representation
        lfp[i] = [np.array(sk[0][i][8]), np.array(sk[1][i][8])] * pq.ms ** (-1)
        lfp[i].units = pq.s ** (-1)

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
print(lvp)


# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 2)

col = [0, 2, 0, 2]  # location of ctrl and nn column
# row = [0, 0, 1, 1]  # location of each dB data
title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    axes = [s_axs[i, 0], s_axs[i, 1]]
    nnmp.nnm_plot(axes[0], data[0], s_img, ccmap, col_ref=lcolor)
    nnmp.nnm_plot(axes[1], data[1], s_img, ccmap, col_ref=lcolor)

    axes[1].axes.yaxis.set_ticklabels([])

    if i != 3:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    # Plot title

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    # SPL dB
    axes[0].text(
        0, 0, f'{lvp[i]} dB',
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

s_axs[3, 0].text(
    0, 0, 'time (ms)',
    horizontalalignment='center',
    verticalalignment='center',
    # rotation='vertical',
    transform=s_axs[3, 0].transAxes,
    fontdict={'weight': 'bold', 'size': 30}
    )

# colorbar setup
mx = nnmp.norm_color(s_img, 'lfp', 0.9)

for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'lfp', vmax=mx[1], ori='horizontal'
            )

        if i != len(lvp) - 1:
            nnmp.remove_colorbar(s_fig)

plt.show()
