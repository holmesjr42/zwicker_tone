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
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # dB SPL list
d_map = sns.color_palette("vlag", as_cmap=True)  # difference colormap

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
            '/data/dataset/nnm_spk_lfp_avg/nnm_time_depth.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cond = ['nnm_3_1_strf', 'nnm_3_1_on', 'nnm_3_1_off', 'nnm_wn_3_1_off']
spk = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    for db in lvl:
        ctemp = dat['spk'][cond[0]][db]
        nntemp = dat['spk'][cond[1]][db]
        nftemp = dat['spk'][cond[2]][db]
        wftemp = dat['spk'][cond[3]][db]
        dnn = []
        dnf = []
        dwf = []
        for ani in range(len(ctemp)):
            dnn.append(nntemp[ani] - ctemp[ani])
            dnf.append(nftemp[ani] - ctemp[ani])
            dwf.append(wftemp[ani] - ctemp[ani])
        spk[db] = [
            np.mean(ctemp, axis=0), np.mean(nntemp, axis=0),
            np.mean(nftemp, axis=0), np.mean(wftemp, axis=0),
            np.mean(dnn, axis=0), np.mean(dnf, axis=0), np.mean(dwf, axis=0)
            ]

# plot start
s_img = []  # for normalizing heatmap
d_img = []  # for difference heatmap normalizastion
s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(4, 7)

title = [
    'Control', 'NN-ON', 'NN-OFF', 'WN-OFF', 'dNN-ON', 'dNN-OFF', 'dWN-OFF'
         ]  # title of plots

for i in range(len(lvl)):
    data = spk[lvl[i]]
    nnmp.tdh_plot(s_axs[i, 0], data[0], s_img, ccmap)  # control heatmap
    nnmp.tdh_plot(s_axs[i, 1], data[1], s_img, ccmap)  # nn-on heatmap
    nnmp.tdh_plot(s_axs[i, 2], data[2], s_img, ccmap)  # nn-off heatmap
    nnmp.tdh_plot(s_axs[i, 3], data[3], s_img, ccmap)  # wn-off heatmap
    # nn-on difference
    nnmp.tdh_plot(s_axs[i, 4], data[4], d_img, d_map, hc='k')
    # nn-off difference
    nnmp.tdh_plot(s_axs[i, 5], data[5], d_img, d_map, hc='k')
    # wn-off difference
    nnmp.tdh_plot(s_axs[i, 6], data[6], d_img, d_map, hc='k')

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

s_axs[3, 3].text(0.5, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[3, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

# colorbar setup
mn, mx = nnmp.norm_color(s_img, 'spk', 0.8)
d_mn, d_mx = nnmp.norm_color(d_img, 'd_spk', 0.8)

for i in range(4):
    for j in range(4):
        cbar = nnmp.colorbar_set(
            s_fig, s_axs[i, j], s_img[3], 'spk', vmax=mx, ori='horizontal'
            )

    for k in range(3):
        cbar2 = nnmp.colorbar_set(
            s_fig, s_axs[i, k + 4], d_img[3], 'd_spk', vmin=d_mn, vmax=d_mx,
            ori='horizontal'
            )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.617464, 0.145290, 0.078151, 0.006947])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.314095, 0.138376, 0.180316, 0.016028])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.667129, 0.138376, 0.175315, 0.015584])
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
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].xaxis.labelpad = -4.280000
plt.figure(0).axes[0].set_position([0.215056, 0.739954, 0.078151, 0.138935])
plt.figure(0).axes[0].texts[0].set_position([-1.255585, 0.500000])
plt.figure(0).axes[0].texts[1].set_position([-0.811897, -1.135625])
plt.figure(0).axes[1].set_position([0.314095, 0.739954, 0.078151, 0.138935])
plt.figure(0).axes[2].set_position([0.416260, 0.741065, 0.078151, 0.138935])
plt.figure(0).axes[3].set_position([0.517800, 0.741065, 0.078151, 0.138935])
plt.figure(0).axes[4].set_position([0.617464, 0.741065, 0.078151, 0.138935])
plt.figure(0).axes[5].set_position([0.716504, 0.741065, 0.078151, 0.138935])
plt.figure(0).axes[7].set_position([0.215056, 0.574995, 0.078151, 0.138935])
plt.figure(0).axes[7].texts[0].set_position([-1.255585, 0.500000])
plt.figure(0).axes[8].set_position([0.314095, 0.574995, 0.078151, 0.138935])
plt.figure(0).axes[9].set_position([0.416260, 0.576106, 0.078151, 0.138935])
plt.figure(0).axes[10].set_position([0.517800, 0.576862, 0.078151, 0.138935])
plt.figure(0).axes[11].set_position([0.617464, 0.576862, 0.078151, 0.138935])
plt.figure(0).axes[12].set_position([0.716504, 0.576862, 0.078151, 0.138935])
plt.figure(0).axes[13].set_position([0.813668, 0.576862, 0.078151, 0.138935])
plt.figure(0).axes[14].set_position([0.215056, 0.415993, 0.078151, 0.138935])
plt.figure(0).axes[14].texts[0].set_position([-1.255585, 0.500000])
plt.figure(0).axes[15].set_position([0.314095, 0.415993, 0.078151, 0.138935])
plt.figure(0).axes[16].set_position([0.416260, 0.417104, 0.078151, 0.138935])
plt.figure(0).axes[17].set_position([0.517800, 0.417104, 0.078151, 0.138935])
plt.figure(0).axes[18].set_position([0.617464, 0.417104, 0.078151, 0.138935])
plt.figure(0).axes[19].set_position([0.716504, 0.417104, 0.078151, 0.138935])
plt.figure(0).axes[20].set_position([0.813668, 0.417104, 0.078151, 0.138935])
plt.figure(0).axes[21].set_position([0.211931, 0.251790, 0.078151, 0.138935])
plt.figure(0).axes[21].texts[0].set_position([-1.255585, 0.500000])
plt.figure(0).axes[22].set_position([0.314095, 0.250679, 0.078151, 0.138935])
plt.figure(0).axes[23].set_position([0.416260, 0.251790, 0.078151, 0.138935])
plt.figure(0).axes[24].set_position([0.517800, 0.251790, 0.078151, 0.138935])
plt.figure(0).axes[24].texts[0].set_position([3.062064, -0.502379])
plt.figure(0).axes[25].set_position([0.617464, 0.251790, 0.078151, 0.138935])
plt.figure(0).axes[26].set_position([0.716504, 0.251790, 0.078151, 0.138935])
plt.figure(0).axes[27].set_position([0.813668, 0.251790, 0.078151, 0.138935])
#% end: automatic generated code from pylustrator
plt.show()
