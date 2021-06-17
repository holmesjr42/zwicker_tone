import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import matplotlib.pyplot as plt
from parameters import parameters as pm
import h5py
from tools import nnm_plot as nnmp
from tools import nn_tool as nt
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
val2 = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1)

lcmap = val.values()[-1]
scmap = val2.values()[-1]
ccmap = [scmap, lcmap]

lvl = com.db['lv'][2]  # 50 dB
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
# file_input = snakemake.input[0]

# getting animal cr number
animal = nnmp.animal_name(file_input)

# stimulus conditions for this script: control, nn, wn
cond = [sets[-7][1], sets[-8][1], sets[-6][0]]

data = {}  # dict for spk/lfp data regarding SPLdB
d_list = ['spk', 'lfp']
dat_list = ['tsp', 'lfp']
conds = sets[6]  # stimulus condition, for plotting

# load file
with h5py.File(file_input, 'r') as dat:
    for da in range(len(dat_list)):
        d = dat_list[da]
        dats = [
            dat[d][cond[0]], dat[d][cond[1]]['nn'],
            dat[d][cond[1]]['si'], dat[d][cond[2]]['si']
            ]  # lfp

        temp = [
            np.array(dats[0][lvl][8]), np.array(dats[1][lvl][8]),
            np.array(dats[2][lvl][8]), np.array(dats[3][lvl][8])
            ]

        data[d_list[da]] = nt.dat_unit(temp, types=d_list[da])

# plot start
imgs = [[], []]  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(20, 16))

s_axs = s_fig.subplots(len(d_list), len(conds))

for da in range(len(d_list)):
    d = d_list[da]
    for c in range(len(conds)):
        nnmp.nnm_plot(s_axs[da, c], data[d][c], imgs[da], ccmap[da])
        s_axs[da, c].label_outer()

        if da == 0:
            s_axs[da, c].text(0.5, 1, conds[c],
                              horizontalalignment='center',
                              verticalalignment='center',
                              rotation='horizontal',
                              transform=s_axs[da, c].transAxes,
                              fontdict={'weight': 'bold', 'size': 30}
                              )
# unit text
s_axs[0, 0].text(0, -0.5, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

s_axs[1, 1].text(0.5, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=s_axs[1, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

# normalization colorbar setup
for d in range(len(d_list)):
    m_val = nnmp.norm_color(imgs[d], d_list[d], 0.8)

    for c in range(len(conds)):
        cbar = nnmp.colorbar_set(
            s_fig, s_axs[d, c], m_val, imgs[d][c], d_list[d]
            )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.898537, 0.187439, 0.007820, 0.195489])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.898522, 0.187072, 0.007834, 0.195856])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.898522, 0.410197, 0.007834, 0.195856])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.168000, 0.410197, 0.156685, 0.195856])
plt.figure(0).axes[0].texts[0].set_position([0.500000, 1.070205])
plt.figure(0).axes[0].texts[1].set_position([-0.344641, -0.067603])
plt.figure(0).axes[1].set_position([0.357174, 0.410197, 0.156685, 0.195856])
plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.070205])
plt.figure(0).axes[2].set_position([0.545348, 0.410197, 0.156685, 0.195856])
plt.figure(0).axes[2].texts[0].set_position([0.506382, 1.063822])
plt.figure(0).axes[3].set_position([0.732522, 0.410197, 0.156685, 0.195856])
plt.figure(0).axes[3].texts[0].set_position([0.500000, 1.070205])
plt.figure(0).axes[4].set_position([0.167000, 0.187072, 0.156685, 0.195856])
plt.figure(0).axes[5].set_position([0.356174, 0.187072, 0.156685, 0.195856])
plt.figure(0).axes[5].texts[0].set_position([1.080784, -0.338259])
plt.figure(0).axes[6].set_position([0.544348, 0.187072, 0.156685, 0.195856])
#% end: automatic generated code from pylustrator
plt.show()
