# import os
import sys
import pathlib

# add path to the tool directory to sys.path
tool_path = pathlib.Path(__file__).parents[2] / "nn_tool"
sys.path.insert(1, str(tool_path))

import numpy as np
import matplotlib.pyplot as plt
from nn_tool.parameter import parameters as pm
import h5py
from nn_tool.tools import nnm_plot as nnmp
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
val = pm.Setup(mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'

with h5py.File(file_input, 'r') as dat:
    lv = np.array([
        dat['tsp']['nnm_3_0_strf']['70'][8],
        dat['tsp']['nnm_3_0_strf']['60'][8],
        dat['tsp']['nnm_3_0_strf']['50'][8],
        dat['tsp']['nnm_3_0_strf']['40'][8]
        ]) * pq.ms**(-1)
    lv.units = pq.s**(-1)

# getting animal cr number
animal = nnmp.animal_name(file_input)

# plot start
# s_img = []  # for normalizing heatmap
s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4)

# for i in range(len(lv)):

for i in range(len(lvp)):
    data = spk[lvp[i]]
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