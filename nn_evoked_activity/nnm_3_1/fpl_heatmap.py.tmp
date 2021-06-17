import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import pickle
import matplotlib.pyplot as plt
from parameters import parameters as pm
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
sets = val.extra_setup()
lvl = com.db['lv']  # dB SPL list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
cond = [sets[-8][1], sets[-6][0], sets[-7][1]]
# notch noise, white noise, control

lfp = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['fpl'][cond[2]], dat['fpl'][cond[0]], dat['fpl'][cond[1]]]  # spk

    for i in lvl:
        lfp[i] = [np.array(lp[0][i]), np.array(lp[1][i][0]),
                  np.array(lp[1][i][1]), np.array(lp[2][i][1])] * pq.microvolt
        lfp[i].units = pq.mV

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
# print(lvp)
#
# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 4)

#
cols = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
# location of data column
rows = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
# dB coordination
dbc = [0, 0, 0, 0]
dbr = [0, 1, 2, 3]
# location of data row
title = sets[6]  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    col = cols[i]
    row = rows[i]
    for j in range(len(data)):
        axes = s_axs[row[j], col[j]]
        nnmp.fph_plot(axes, data[j], s_img, ccmap)
        if col[j] != 0:
            axes.axes.yaxis.set_ticklabels([])
        if row[j] != 3:
            axes.axes.xaxis.set_ticklabels([])

        # Plot title
        if row[j] == 0:
            axes.set_title(title[j], fontdict={'fontsize': 20})

    s_axs[dbr[i], dbc[i]].text(-0.3, .5, f'{lvp[i]} dB',
                               horizontalalignment='center',
                               verticalalignment='center',
                               rotation='vertical',
                               transform=s_axs[dbr[i], dbc[i]].transAxes,
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

# colorbar setup
mn = nnmp.norm_color(s_img, 'lfp', 0.9)

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    col = cols[i]
    row = rows[i]
    for j in range(len(data)):
        axes = s_axs[row[j], col[j]]
        cbar = nnmp.colorbar_set(s_fig, axes, mn, s_img[i], 'lfp')


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.856708, 0.338510, 0.034437, 0.516552])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.865563, 0.338510, 0.034437, 0.516552])
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
plt.figure(0).ax_dict["<colorbar>"].yaxis.labelpad = -153.142857
plt.figure(0).axes[0].set_position([0.162500, 0.737548, 0.156685, 0.117514])
plt.figure(0).axes[0].texts[0].set_position([-0.738779, 0.500000])
plt.figure(0).axes[0].texts[1].set_position([-0.478668, -1.090299])
plt.figure(0).axes[0].texts[2].set_position([-1.116890, -2.619374])
plt.figure(0).axes[1].set_position([0.336278, 0.737548, 0.156685, 0.117514])
plt.figure(0).axes[2].set_position([0.510057, 0.737548, 0.156685, 0.117514])
plt.figure(0).axes[3].set_position([0.683835, 0.737548, 0.156685, 0.117514])
plt.figure(0).axes[4].set_position([0.162500, 0.604535, 0.156685, 0.117514])
plt.figure(0).axes[4].texts[0].set_position([-0.738779, 0.477206])
plt.figure(0).axes[5].set_position([0.336278, 0.604535, 0.156685, 0.117514])
plt.figure(0).axes[6].set_position([0.510057, 0.604535, 0.156685, 0.117514])
plt.figure(0).axes[7].set_position([0.683835, 0.604535, 0.156685, 0.117514])
plt.figure(0).axes[8].set_position([0.162500, 0.471523, 0.156685, 0.117514])
plt.figure(0).axes[8].texts[0].set_position([-0.738779, 0.500000])
plt.figure(0).axes[9].set_position([0.336278, 0.471523, 0.156685, 0.117514])
plt.figure(0).axes[10].set_position([0.510057, 0.471523, 0.156685, 0.117514])
plt.figure(0).axes[11].set_position([0.683835, 0.471523, 0.156685, 0.117514])
plt.figure(0).axes[12].set_position([0.162500, 0.338510, 0.156685, 0.117514])
plt.figure(0).axes[12].texts[0].set_position([-0.738779, 0.454413])
plt.figure(0).axes[13].set_position([0.336278, 0.338510, 0.156685, 0.117514])
plt.figure(0).axes[14].set_position([0.510057, 0.338510, 0.156685, 0.117514])
plt.figure(0).axes[15].set_position([0.683835, 0.338510, 0.156685, 0.117514])
#% end: automatic generated code from pylustrator
plt.show()
