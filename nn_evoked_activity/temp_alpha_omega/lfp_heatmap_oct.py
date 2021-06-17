import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from tools import nnm_plot as nnmp
from tools import notch_gap_params as p_tool
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
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()
lvs = [lvl[1], lvl[3]]  # choose SPL you want to show

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr121c_210503_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = sets[-8][1]
c_w = sets[-6][0]
c_c = 'strf_4'
lfp = {}  # dict for spk data regarding SPLdB
chs = 1
cf = 11314
oct_cut = p_tool.o_cut(cf)
# load file
with h5py.File(file_input, 'r') as dat:
    lp = [
        dat['lfp'][c_c], dat['lfp'][c_n]['nn'],
        dat['lfp'][c_n]['si']
         ]  # lfp

    for i in lvl:
        lfp[i] = [
                np.array(lp[0][i][chs][oct_cut[0]:oct_cut[1]+1]),
                np.array(lp[1][i][chs][oct_cut[0]:oct_cut[1]+1]),
                np.array(lp[2][i][chs][oct_cut[0]:oct_cut[1]+1])
                     ] * pq.microvolt

        lfp[i].units = pq.mV

# lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
# print(lvp)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(18, 12))

s_axs = s_fig.subplots(2, 3)

title = sets[6][0:3]  # title of plots

for i in range(len(lvs)):
    data = lfp[lvs[i]]
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(data)):
        nnmp.nnm_plot(
            axes[j], data[j], s_img, ccmap, type='octave')
        if j != 0:
            axes[j].axes.yaxis.set_ticklabels([])

    if i != 1:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    axes[0].text(0, 0, f'{lvs[i]} dB',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=axes[0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

# unit text
s_axs[0, 0].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

s_axs[1, 0].text(0, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

mx = nnmp.norm_color(s_img, 'lfp', 0.9)

# colorbar setup
for i in range(len(lvs)):
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i], 'lfp', vmax=mx[1], vmin=mx[0],
            ori='horizontal'
            )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.334417, 0.143637, 0.265889, 0.019942])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.334583, 0.156169, 0.264167, 0.019812])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].xaxis.labelpad = -4.100000
plt.figure(0).axes[0].texts[0].set_position([-0.473322, 0.484079])
plt.figure(0).axes[0].texts[1].set_position([-0.276104, -0.035858])
plt.figure(0).axes[1].set_position([0.370528, 0.589500, 0.193667, 0.290500])
plt.figure(0).axes[2].set_position([0.598224, 0.589500, 0.193667, 0.290500])
plt.figure(0).axes[3].set_position([0.142137, 0.282000, 0.193667, 0.290500])
plt.figure(0).axes[3].texts[0].set_position([-0.473322, 0.523523])
plt.figure(0).axes[3].texts[1].set_position([1.685313, -0.261761])
plt.figure(0).axes[4].set_position([0.370528, 0.282000, 0.193667, 0.290500])
plt.figure(0).axes[5].set_position([0.598224, 0.282000, 0.193667, 0.290500])
#% end: automatic generated code from pylustrator
plt.show()