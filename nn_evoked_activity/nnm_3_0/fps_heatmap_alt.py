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
Heatmap 4 x 2 (dB x condition) which will be re-included in the paper, 
possibly?

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

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'

# stimulus conditions for this script
c_n = 'nnm_3_0'
c_s = 'nnm_3_0_strf'
spk = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['mfpt'][c_s], dat['mfpt'][c_n]]  # spk

    for i in lvl:
        spk[i] = [np.array(sk[0][i]), np.array(sk[1][i])] * (pq.ms ** -1)
        spk[i].units = pq.s ** (-1)
lvp = nnmp.db_lv(spk)  # SPL dB which actually has data

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(9, 16))

s_axs = s_fig.subplots(4, 2)

title = ['Control', 'NN']  # title of plots

for i in range(len(lvp)):
    data = spk[lvp[i]]
    for j in range(len(data)):
        axs = s_axs[i, j]
        nnmp.fph_plot(axs, data[j], s_img, ccmap)

        # Plot title
        if i == 0:
            axs.set_title(title[j], fontdict={'fontsize': 25})

        if j == 0:
            # SPL dB
            axs.text(0, 0.5, f'{lvp[i]} dB',
                     horizontalalignment='center',
                     verticalalignment='center',
                     rotation='vertical',
                     transform=axs.transAxes,
                     fontdict={'weight': 'bold', 'size': 25}
                     )
        axs.label_outer()

# unit text
s_axs[0, 0].text(0, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[3, 0].text(1, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[3, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

vm = nnmp.norm_color(s_img, 'spk', 0.8)

# colorbar setup

for i in range(len(lvp)):
    for j in range(len(title)):
        cbar = nnmp.colorbar_set(
            s_fig, s_axs[i, j], s_img[i], 'spk', vmax=vm[1], ori='horizontal'
            )


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.316528, 0.145967, 0.530834, 0.014930])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.316528, 0.720232, 0.246995, 0.138935])
plt.figure(0).axes[0].texts[0].set_position([-1.079643, 0.500000])
plt.figure(0).axes[0].texts[1].set_position([-0.652284, -1.312066])
plt.figure(0).axes[1].set_position([0.600366, 0.720232, 0.246995, 0.138935])
plt.figure(0).axes[2].set_position([0.316528, 0.557904, 0.246995, 0.138935])
plt.figure(0).axes[2].texts[0].set_position([-1.079643, 0.500000])
plt.figure(0).axes[3].set_position([0.600366, 0.557904, 0.246995, 0.138935])
plt.figure(0).axes[4].set_position([0.316528, 0.395576, 0.246995, 0.138935])
plt.figure(0).axes[4].texts[0].set_position([-1.079643, 0.500000])
plt.figure(0).axes[5].set_position([0.600366, 0.395576, 0.246995, 0.138935])
plt.figure(0).axes[6].set_position([0.316528, 0.229082, 0.246995, 0.138935])
plt.figure(0).axes[6].texts[0].set_position([-1.079643, 0.500000])
plt.figure(0).axes[6].texts[1].set_position([1.029990, -0.292403])
plt.figure(0).axes[7].set_position([0.600366, 0.229082, 0.246995, 0.138935])
#% end: automatic generated code from pylustrator
plt.show()
