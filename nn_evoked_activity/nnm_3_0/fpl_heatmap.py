import os
import sys
import h5py

import numpy as np

import matplotlib.pyplot as plt
import pylustrator
import quantities as pq

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
print(sys.path)

from nn_tool.parameter import parameters as pm
from nn_tool.tools import nnm_plot as nnmp

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
param = pm.Setup(hcmap_mode='lfp', mode='fun')  # parameters for plot setting
ccmap = param.hcmap
lcolor = param.ref_line_color
lvl = com.db['lv']  # SPLdB list

# load data
data_path = 'OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
            '/data/dataset/nnm_spk_lfp_avg'
file_name = 'all_spk_lfp_avg_nnm.hdf5'
partition = pm.data_path_selection()

file_input = os.path.join(partition, data_path, file_name)

# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = param.c_n[0]
c_s = param.c_s[0]

lfp = {}  # dict for spk data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['fpl'][c_s], dat['fpl'][c_n]]  # spk

    for i in lvl:
        lfp[i] = [np.array(lp[0][i]), np.array(lp[1][i])] * pq.microvolt
        lfp[i].units = pq.mV

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
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
    data = lfp[lvp[i]]
    axes = [s_axs[row[i], col[i]], s_axs[row[i], col[i] + 1]]
    nnmp.fph_plot(axes[0], data[0], s_img, ccmap, line_color=lcolor)
    nnmp.fph_plot(axes[1], data[1], s_img, ccmap, line_color=lcolor)
    axes[1].axes.yaxis.set_ticklabels([])

    if row[i] == 0:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    # Plot title

    if row[i] == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 20})

    # SPL dB
    axes[0].text(1, 1, f'{lvp[i]} dB',
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

s_axs[0, 0].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 3].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

mn, mx = nnmp.norm_color(s_img, 'lfp', 0.8)

# colorbar setup

cbaxes = s_fig.add_axes([0.8, 0.1, 0.01, 0.299517])

cbar = nnmp.colorbar_set(s_fig, cbaxes, s_img[0], 'lfp', vmax=mx, vmin=mn)

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].texts[0].set_position([1.000000, 1.192903])
plt.figure(0).axes[0].texts[1].set_position([-0.426613, -0.189194])
plt.figure(0).axes[0].texts[2].set_position([-1.272419, -0.248548])
plt.figure(0).axes[1].set_position([0.305924, 0.555242, 0.168478, 0.299517])
plt.figure(0).axes[2].set_position([0.550598, 0.555242, 0.168478, 0.299517])
plt.figure(0).axes[2].texts[0].set_position([0.999492, 1.193612])
plt.figure(0).axes[4].texts[0].set_position([1.000000, 1.085323])
plt.figure(0).axes[5].set_position([0.305924, 0.135242, 0.168478, 0.299517])
plt.figure(0).axes[6].set_position([0.550598, 0.135242, 0.168478, 0.299517])
plt.figure(0).axes[6].texts[0].set_position([0.999492, 1.085535])
plt.figure(0).axes[7].set_position([0.731522, 0.135242, 0.168478, 0.299517])
plt.figure(0).axes[8].set_position([0.904375, 0.135241, 0.010000, 0.299517])
#% end: automatic generated code from pylustrator
plt.show()
