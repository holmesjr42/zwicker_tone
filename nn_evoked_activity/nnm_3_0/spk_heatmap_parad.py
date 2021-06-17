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
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = sets[7][0]
c_s = sets[8][0]
spk = {}  # dict for spk data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['tsp'][c_s], dat['tsp'][c_n]]  # spk
# 800 um is chosen for the representation
    for i in lvl:
        spk[i] = [np.array(sk[0][i][8]), np.array(sk[1][i][8])] * pq.ms**(-1)
        spk[i].units = pq.s**(-1)
lvp = nnmp.db_lv(spk)  # SPL dB which actually has data
print(lvp)
# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(12, 16))

s_axs = s_fig.subplots(4, 2)

# col = [0, 2, 0, 2]  # location of ctrl and nn column
# row = [0, 0, 1, 1]  # location of each dB data
title = ['Control', 'NN']  # title of plots

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


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.852061, 0.110000, 0.051333, 0.770000])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.312203, 0.074053, 0.514526, 0.019295])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].xaxis.labelpad = -5.000000
plt.figure(0).ax_dict["<colorbar>"].yaxis.labelpad = 18.800000
plt.figure(0).axes[0].set_position([0.312203, 0.796359, 0.223188, 0.167391])
plt.figure(0).axes[0].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[1].set_position([0.603541, 0.795109, 0.223188, 0.167391])
plt.figure(0).axes[2].set_position([0.312203, 0.595489, 0.223188, 0.167391])
plt.figure(0).axes[2].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[3].set_position([0.603541, 0.594239, 0.223188, 0.167391])
plt.figure(0).axes[4].set_position([0.313870, 0.393370, 0.223188, 0.167391])
plt.figure(0).axes[4].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[5].set_position([0.603541, 0.393370, 0.223188, 0.167391])
plt.figure(0).axes[6].set_position([0.313870, 0.192500, 0.223188, 0.167391])
plt.figure(0).axes[6].texts[0].set_position([-0.352041, 0.485390])
plt.figure(0).axes[6].texts[1].set_position([1.219697, -0.298701])
plt.figure(0).axes[7].set_position([0.603541, 0.192500, 0.223188, 0.167391])
#% end: automatic generated code from pylustrator
plt.show()
