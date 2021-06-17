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
val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # dB SPL list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = 'nnm_3_0'
c_s = 'nnm_3_0_strf'
spk = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['lfp'][c_s], dat['lfp'][c_n]]  # spk

    for i in lvl:
        c_temp = []
        n_temp = []
        for j in range(16):
            c_temp.append(np.array(sk[0][i][j][12]))
            n_temp.append(np.array(sk[1][i][j][12]))

        spk[i] = [c_temp, n_temp] * pq.microvolt
        spk[i].units = pq.mV
lvp = nnmp.db_lv(spk)  # SPL dB which actually has data
print(lvp)
# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(2, 4)
#
col = [0, 2, 0, 2]  # location of ctrl and nn column
row = [0, 0, 1, 1]  # location of each dB data
title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = spk[lvp[i]]
    axes = [s_axs[row[i], col[i]], s_axs[row[i], col[i] + 1]]
    img0 = axes[0].imshow(data[0], cmap=ccmap, aspect=101/1500,
                         extent=[0, 101, 1500, 0], interpolation='gaussian')
    img1 = axes[1].imshow(data[1], cmap=ccmap, aspect=101/1500,
                         extent=[0, 101, 1500, 0], interpolation='gaussian')

    s_img = np.append(s_img, [img0, img1])
    axes[1].axes.yaxis.set_ticklabels([])

    if row[i] == 0:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    # Plot title
#
    if row[i] == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 20})

    # SPL dB
    axes[0].text(0, 0, f'{lvp[i]} dB',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=axes[0].transAxes,
                 fontdict={'weight': 'bold', 'size': 25}
                 )

# unit text
s_axs[0, 0].text(0, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[0, 0].text(0, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 3].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

nnmp.norm_color(s_img, 'lfp', 0.8)

# colorbar setup
mx = np.around(min(ims.get_array().min() for ims in s_img) * 0.8, decimals=2)

for i in range(len(lvp)):
    axes = [s_axs[row[i], col[i]], s_axs[row[i], col[i] + 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(s_fig, axes[j], mx, s_img[i], 'lfp')

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.883288, 0.175643, 0.018805, 0.668630])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.883014, 0.175643, 0.018805, 0.668630])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].yaxis.labelpad = 7.520000
plt.figure(0).ax_dict["<colorbar>"].get_yaxis().get_label().set_position([1527.320000, 0.500003])
plt.figure(0).axes[0].set_position([0.145625, 0.567947, 0.156685, 0.278551])
plt.figure(0).axes[0].texts[0].set_position([1.049081, 1.280428])
plt.figure(0).axes[0].texts[1].set_position([-0.378946, -0.278949])
plt.figure(0).axes[0].texts[2].set_position([-1.364204, -0.259279])
plt.figure(0).axes[1].set_position([0.314675, 0.567944, 0.156685, 0.278551])
plt.figure(0).axes[2].set_position([0.546850, 0.565722, 0.156685, 0.278551])
plt.figure(0).axes[2].texts[0].set_position([1.037113, 1.280426])
plt.figure(0).axes[3].set_position([0.715600, 0.565722, 0.156685, 0.278551])
plt.figure(0).axes[4].set_position([0.145625, 0.175643, 0.156685, 0.278551])
plt.figure(0).axes[4].texts[0].set_position([1.061047, 1.140817])
plt.figure(0).axes[5].set_position([0.314375, 0.175722, 0.156685, 0.278551])
plt.figure(0).axes[6].set_position([0.546850, 0.175722, 0.156685, 0.278551])
plt.figure(0).axes[6].texts[0].set_position([1.036469, 1.129140])
plt.figure(0).axes[7].set_position([0.715600, 0.175722, 0.156685, 0.278551])
#% end: automatic generated code from pylustrator
plt.show()
# axs.text(1.3, 1.5, f'{lv} SPL dB',
# #          horizontalalignment='center',
# #          verticalalignment='center',
# #          # rotation='vertical',
# #          transform=axs[lv][0, 0].transAxes,
# #          fontdict={'weight': 'bold', 'size': 11}
# #          )
