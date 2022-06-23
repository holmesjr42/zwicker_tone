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
Create heatmap for firing rate
Heatmap 4 x 2 (dB x condition) which will be re-included in the paper, 
possibly?

'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
# some setups for plotting e.g. color scheme
val = pm.Setup(hcmap_mode='lfp', mode='fun')  # parameters for plot setting
ccmap = val.hcmap
lcolor = val.ref_line_color
lvl = com.db['lv']  # dB SPL list

data_path = 'OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
            '/data/dataset/nnm_spk_lfp_avg'
file_name = 'all_spk_lfp_avg_nnm.hdf5'
partition = pm.data_path_selection()

file_input = os.path.join(partition, data_path, file_name)

# stimulus conditions for this script
c_n = 'nnm_3_0'
c_s = 'nnm_3_0_strf'
lfp = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['fpl'][c_s], dat['fpl'][c_n]]  # spk

    for i in lvl:
        lfp[i] = [np.array(lp[0][i]), np.array(lp[1][i])] * pq.microvolt
        lfp[i].units = pq.mV
lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(9, 16))

s_axs = s_fig.subplots(4, 2)

title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    for j in range(len(data)):
        axs = s_axs[i, j]
        nnmp.fph_plot(axs, data[j], s_img, ccmap)
        # axs.set_yticklabels([])
        # Plot title
        if i == 0:
            axs.set_title(title[j], fontdict={'fontsize': 25})

        # if j == 0:
        #     # SPL dB
        #     axs.text(0, 0.5, f'{lvp[i]} dB',
        #              horizontalalignment='center',
        #              verticalalignment='center',
        #              rotation='vertical',
        #              transform=axs.transAxes,
        #              fontdict={'weight': 'bold', 'size': 25}
        #              )
        axs.label_outer()

# unit text
# s_axs[0, 0].text(0, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
#                  horizontalalignment='center',
#                  verticalalignment='center',
#                  rotation='vertical',
#                  transform=s_axs[0, 0].transAxes,
#                  fontdict={'weight': 'bold', 'size': 23}
#                  )

s_axs[3, 0].text(
    1, 0, 'octaves',
    horizontalalignment='center',
    verticalalignment='center',
    # rotation='vertical',
    transform=s_axs[3, 0].transAxes,
    fontdict={'weight': 'bold', 'size': 23}
    )

mn, mx = nnmp.norm_color(s_img, 'lfp', 0.8)

# colorbar setup

for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'lfp',
            vmax=mx, vmin=mn, ori='horizontal'
            )

        if i != len(lvp) - 1:
            nnmp.remove_colorbar(s_fig)

plt.show()
