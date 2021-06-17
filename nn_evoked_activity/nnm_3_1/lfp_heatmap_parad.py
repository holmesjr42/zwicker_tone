import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
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
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script
c_n = sets[-8][1]
c_w = sets[-6][0]
c_c = sets[-7][1]
lfp = {}  # dict for spk data regarding SPLdB

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [
        dat['lfp'][c_c], dat['lfp'][c_n]['nn'],
        dat['lfp'][c_n]['si'], dat['lfp'][c_w]['si']
         ]  # lfp

    for i in lvl:
        lfp[i] = [np.array(lp[0][i][8]), np.array(lp[1][i][8]),
                  np.array(lp[2][i][8]), np.array(lp[3][i][8])] * pq.microvolt
        lfp[i].units = pq.mV

lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
# print(lvp)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(20, 16))

s_axs = s_fig.subplots(4, 4)

title = sets[6]  # title of plots

for i in range(len(lvp)):
    data = lfp[lvp[i]]
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2], s_axs[i, 3]]

    for j in range(len(data)):
        nnmp.nnm_plot(axes[j], data[j], s_img, ccmap)
        if j != 0:
            axes[j].axes.yaxis.set_ticklabels([])

    if i != 3:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    axes[0].text(0, 0, f'{lvp[i]} dB',
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

s_axs[3, 0].text(0, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[3, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

mx = nnmp.norm_color(s_img, 'lfp', 0.8)

# colorbar setup
for i in range(len(lvp)):
    axes = [s_axs[i, 0], s_axs[i, 1]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(s_fig, axes[j], mx, s_img[i], 'lfp')

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.903699, 0.110000, 0.030800, 0.770000])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.899783, 0.110000, 0.030800, 0.770000])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.248605, 0.712609, 0.133913, 0.167391])
plt.figure(0).axes[0].texts[0].set_visible(False)
plt.figure(0).axes[0].texts[1].set_visible(False)
plt.figure(0).axes[1].set_position([0.416612, 0.712609, 0.133913, 0.167391])
plt.figure(0).axes[2].set_position([0.583297, 0.712609, 0.133913, 0.167391])
plt.figure(0).axes[4].set_position([0.248605, 0.511739, 0.133913, 0.167391])
plt.figure(0).axes[4].texts[0].set_visible(False)
plt.figure(0).axes[5].set_position([0.416612, 0.511739, 0.133913, 0.167391])
plt.figure(0).axes[6].set_position([0.583297, 0.511739, 0.133913, 0.167391])
plt.figure(0).axes[8].set_position([0.248605, 0.310870, 0.133913, 0.167391])
plt.figure(0).axes[8].texts[0].set_visible(False)
plt.figure(0).axes[9].set_position([0.416612, 0.310870, 0.133913, 0.167391])
plt.figure(0).axes[10].set_position([0.583297, 0.310870, 0.133913, 0.167391])
plt.figure(0).axes[12].set_position([0.249438, 0.110000, 0.133913, 0.167391])
plt.figure(0).axes[12].texts[0].set_visible(False)
plt.figure(0).axes[12].texts[1].set_position([2.458063, -0.311147])
plt.figure(0).axes[13].set_position([0.416612, 0.110000, 0.133913, 0.167391])
plt.figure(0).axes[14].set_position([0.583297, 0.110000, 0.133913, 0.167391])
#% end: automatic generated code from pylustrator
plt.show()