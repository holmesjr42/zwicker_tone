import sys
import pathlib

# add path to the tool directory to sys.path
tool_path = pathlib.Path(__file__).parents[2] / "nn_tool"
sys.path.insert(1, str(tool_path))

import h5py
import numpy as np

import matplotlib.pyplot as plt
from parameter import parameters as pm
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
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')
ccmap2 = val2.values()[-1]
cmaps = [ccmap, ccmap2]

sets = val.extra_setup()

lv = com.db['lv'][2]  # 50 dB as an example

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/all_spk_lfp_avg_nnm.hdf5'

# stimulus conditions for this script
c_n = sets[-8][1]
c_w = sets[-6][0]
c_c = sets[-7][1]

dats = {}  # dict for spk data regarding dB SPL

# load file
with h5py.File(file_input, 'r') as dat:
    sk = [dat['fpt'][c_c], dat['fpt'][c_n], dat['fpt'][c_w]]  # spk
    lp = [dat['fpl'][c_c], dat['fpl'][c_n], dat['fpl'][c_w]]  # spk

    dats['spk'] = [
                      np.array(sk[0][lv]), np.array(sk[1][lv][0]),
                      np.array(sk[1][lv][1]), np.array(sk[2][lv][1])
                      ] * (pq.ms ** -1)
    dats['lfp'] = [
                      np.array(lp[0][lv]), np.array(lp[1][lv][0]),
                      np.array(lp[1][lv][1]), np.array(lp[2][lv][1])
                      ] * (pq.microvolt)

    dats['spk'].units = pq.s ** (-1)
    dats['lfp'].units = pq.mV

d_list = list(dats.keys())
# plot start
s_img = [[] for _ in range(2)]  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(2, 4)

title = sets[6]  # title of plots

for i in range(len(d_list)):
    d = d_list[i]
    print(d)
    data = dats[d]
    cmap = cmaps[i]
    for j in range(len(data)):
        axes = s_axs[i, j]
        nnmp.fph_plot(axes, data[j], s_img[i], cmap)
        axes.label_outer()

        # Plot title
        if i == 0:
            axes.set_title(title[j], fontdict={'fontsize': 25})

# unit text
s_axs[0, 0].text(0, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

s_axs[1, 0].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )

# colorbar setup
ms = [
    nnmp.norm_color(s_img[0], 'spk', 0.8),
    nnmp.norm_color(s_img[1], 'lfp', 0.8)
     ]

for i in range(len(d_list)):
    d = d_list[i]
    data = dats[d]
    for j in range(len(data)):
        axes = s_axs[i, j]
        cbar = nnmp.colorbar_set(
            s_fig, axes, s_img[i][j], d, vmax=ms[i][1], vmin=ms[i][0]
            )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.894398, 0.565725, 0.007834, 0.278551])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.894398, 0.197114, 0.007834, 0.278551])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.212500, 0.565725, 0.156685, 0.278551])
plt.figure(0).axes[0].texts[0].set_position([-0.508585, -0.204431])
plt.figure(0).axes[1].set_position([0.384986, 0.565725, 0.156685, 0.278551])
plt.figure(0).axes[2].set_position([0.557473, 0.565725, 0.156685, 0.278551])
plt.figure(0).axes[4].set_position([0.212500, 0.197114, 0.156685, 0.278551])
plt.figure(0).axes[4].texts[0].set_position([2.134062, -0.299168])
plt.figure(0).axes[5].set_position([0.384986, 0.197114, 0.156685, 0.278551])
plt.figure(0).axes[6].set_position([0.557473, 0.197114, 0.156685, 0.278551])
plt.figure(0).axes[7].set_position([0.731522, 0.197114, 0.156685, 0.278551])
#% end: automatic generated code from pylustrator
plt.show()
