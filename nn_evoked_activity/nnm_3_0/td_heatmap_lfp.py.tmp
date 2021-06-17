import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import matplotlib.image as mpimg
from parameter import parameters as pm
import seaborn as sns
import h5py
from matplotlib.colors import ListedColormap
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
val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1,  ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # dB SPL list
d_map = sns.color_palette("vlag", as_cmap=True)  # difference colormap

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
            '/data/dataset/nnm_spk_lfp_avg/nnm_time_depth.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cond = ['nnm_3_0_strf', 'nnm_3_0']
lfp = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    for db in lvl:
        ctemp = dat['lfp'][cond[0]][db]
        ntemp = dat['lfp'][cond[1]][db]
        dtemp = []
        for ani in range(len(ctemp)):
            dtemp.append(ntemp[ani] - ctemp[ani])
        lfp[db] = [
            np.mean(ctemp, axis=0), np.mean(ntemp, axis=0),
            np.mean(dtemp, axis=0)
            ]

# plot start
s_img = []  # for normalizing heatmap
d_img = []  # for difference heatmap normalizastion
s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 3)

title = ['Control', 'NN', 'NN - Control']  # title of plots

for i in range(len(lvl)):
    data = lfp[lvl[i]]
    nnmp.tdh_plot(s_axs[i, 0], data[0], s_img, ccmap)  # control heatmap
    nnmp.tdh_plot(s_axs[i, 1], data[1], s_img, ccmap)  # nn heatmap
    nnmp.tdh_plot(s_axs[i, 2], data[2], d_img, d_map, hc='k')
    # difference heatmap

    # Plot title

    if i == 0:
        for j in range(len(title)):
            s_axs[i, j].set_title(title[j], fontdict={'fontsize': 20})

    # SPL dB
    s_axs[i, 0].text(
        0, 0.5, f'{lvl[i]} dB',
        horizontalalignment='center',
        verticalalignment='center',
        rotation='vertical',
        transform=s_axs[i, 0].transAxes,
        fontdict={'weight': 'bold', 'size': 25}
        )

# unit text
s_axs[0, 0].text(-0.5, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[3, 1].text(0.5, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[3, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

# colorbar setup
mn, mx = nnmp.norm_color(s_img, 'lfp', 0.8)
d_mn, d_mx = nnmp.norm_color(d_img, 'd_lfp', 0.8)

for i in range(len(lvl)):
    for j in range(len(title) - 1):
        cbar = nnmp.colorbar_set(
            s_fig, s_axs[i, j], s_img[i], 'lfp', vmin=mn, vmax=mx,
            ori='horizontal'
            )

    cbar2 = nnmp.colorbar_set(
        s_fig, s_axs[i, 2], d_img[i], 'd_lfp', vmin=d_mn, vmax=d_mx,
        ori='horizontal'
        )


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.693408, 0.193025, 0.185245, 0.006947])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.234840, 0.189295, 0.224990, 0.008437])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.672935, 0.189295, 0.224990, 0.008437])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.257459, 0.740024, 0.185246, 0.138935])
plt.figure(0).axes[0].texts[0].set_position([-0.777602, 0.500000])
plt.figure(0).axes[0].texts[1].set_position([-0.542843, -1.135370])
plt.figure(0).axes[1].set_position([0.476821, 0.740024, 0.185246, 0.138935])
plt.figure(0).axes[2].set_position([0.693406, 0.740024, 0.185246, 0.138935])
plt.figure(0).axes[3].set_position([0.257459, 0.579779, 0.185246, 0.138935])
plt.figure(0).axes[3].texts[0].set_position([-0.777602, 0.500000])
plt.figure(0).axes[4].set_position([0.476821, 0.579779, 0.185246, 0.138934])
plt.figure(0).axes[5].set_position([0.693406, 0.579204, 0.185245, 0.138934])
plt.figure(0).axes[6].set_position([0.257459, 0.419534, 0.185246, 0.138935])
plt.figure(0).axes[6].texts[0].set_position([-0.777602, 0.500000])
plt.figure(0).axes[7].set_position([0.475432, 0.419534, 0.185246, 0.138934])
plt.figure(0).axes[8].set_position([0.693407, 0.419769, 0.185246, 0.138934])
plt.figure(0).axes[9].set_position([0.257459, 0.260332, 0.185246, 0.138935])
plt.figure(0).axes[9].texts[0].set_position([-0.777602, 0.500000])
plt.figure(0).axes[10].set_position([0.475432, 0.260333, 0.185245, 0.138934])
plt.figure(0).axes[10].texts[0].set_position([0.500000, -0.269912])
plt.figure(0).axes[11].set_position([0.693406, 0.260333, 0.185246, 0.138935])
#% end: automatic generated code from pylustrator
plt.show()
