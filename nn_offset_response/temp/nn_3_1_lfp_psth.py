import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nn_tool as nt
from parameter import parameters as pm
import pylustrator
from parameter import parameters as pm
import matplotlib.pyplot as plt
pylustrator.start()
sys.path.pop(1)

'''
This is to create offset response table.
'''

'''
setup
'''

val = pm.Setup(cond2='tsp')

dbs, db, dcmap, names, legendl, ch_l, l_list, layer_name = val.nn31_plot()
legends = legendl[1]
nn = names[0]
wn = names[1]
db_n = 1
ont = [0, 251]
oft = [3000, 3251]
bt = [3300, 3501]

blt = [nt.lfp_index(bt[0]), nt.lfp_index(bt[1])]
r = 6
file ="/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
      "/dataset/nn_mean/cl118_210329_nn_mean.hdf5"

with h5py.File(file, 'r') as dat:
    l_n = dat['lfp']['mean']['nn_3_1'][db_n]
    l_w = dat['lfp']['mean']['nn_wn_3_1'][db_n]
    s_n = dat['spk']['s_psth']['nn_3_1'][db_n]
    s_w = dat['spk']['s_psth']['nn_wn_3_1'][db_n]
    st = dat['spk']['time']['nn_3_1'][0]

    lt = np.linspace(
        0, 4100, num=len(l_n[0]), endpoint=True
        )


    n_fig = plt.figure(0, figsize=(16, 9))
    n_axs = n_fig.subplots(3, 4)

    for i in range(len(ch_l)):
        ch = ch_l[i]
        # onset
        n_axs[i, 2].plot(lt, l_n[ch], label='NN-ON')
        n_axs[i, 2].plot(lt, l_w[ch], label='WN-ON')
        n_axs[i, 0].plot(st, s_n[ch], label='NN-ON')
        n_axs[i, 0].plot(st, s_w[ch], label='WN-ON')

        # offset
        n_axs[i, 3].plot(lt, l_n[ch], label='NN-OFF', zorder=3)
        n_axs[i, 3].plot(lt, l_w[ch], label='WN-OFF', zorder=2)
        n_axs[i, 1].plot(st, s_n[ch], label='NN-OFF', zorder=3)
        n_axs[i, 1].plot(st, s_w[ch], label='WN-OFF', zorder=2)

        # threshold
        tln = nt.nn_threshold(l_n[ch], blt, r, 'lfp')
        tlw = nt.nn_threshold(l_w[ch], blt, r, 'lfp')
        tsn = nt.nn_threshold(s_n[ch], bt, r, 'spk')
        tsw = nt.nn_threshold(s_w[ch], bt, r, 'spk')

        n_axs[i, 2].set_xlim(ont[0], ont[1])
        n_axs[i, 2].set_ylim(-1.5, 0.45)

        n_axs[i, 3].set_xlim(oft[0], oft[1])
        n_axs[i, 3].set_ylim(-0.25, 0.15)
        n_axs[i, 3].axhline(y=tln, linestyle='--', color="#0c3b70", zorder=5)
        n_axs[i, 3].axhline(y=tlw, linestyle='-.', color="#6e5d44", zorder=4)
        n_axs[i, 3].axvspan(
            oft[0] + 100, oft[1], alpha=0.3, color='#bccbe3', zorder=0
            )

        n_axs[i, 0].set_xlim(ont[0], ont[1])
        n_axs[i, 0].set_ylim(0, 650)

        n_axs[i, 1].set_ylim(0, 300)
        n_axs[i, 1].set_xlim(oft[0], oft[1])
        n_axs[i, 1].axhline(y=tsn, linestyle='--', color="#0c3b70", zorder=5)
        n_axs[i, 1].axhline(y=tsw, linestyle='-.', color="#6e5d44", zorder=4)
        n_axs[i, 1].axvspan(
            oft[0] + 100, oft[1], alpha=0.3, color='#bccbe3', zorder=0
            )


n_axs[0, 0].legend(prop={'size': 9},
                   loc='upper right',
                   bbox_to_anchor=(1, 1))
n_axs[0, 1].legend(prop={'size': 9},
                   loc='upper right',
                   bbox_to_anchor=(1, 1))
n_axs[0, 2].legend(prop={'size': 9},
                   loc='lower right',
                   bbox_to_anchor=(1, 0))
n_axs[0, 3].legend(prop={'size': 9},
                   loc='lower right',
                   bbox_to_anchor=(1, 0))

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.066250, 0.654641, 0.168478, 0.226471])
plt.figure(0).axes[1].set_position([0.268424, 0.654641, 0.168478, 0.226471])
plt.figure(0).axes[4].set_position([0.066250, 0.382876, 0.168478, 0.226471])
plt.figure(0).axes[5].set_position([0.268424, 0.382876, 0.168478, 0.226471])
plt.figure(0).axes[8].set_position([0.066250, 0.111111, 0.168478, 0.226471])
plt.figure(0).axes[9].set_position([0.268424, 0.110000, 0.168478, 0.226471])
#% end: automatic generated code from pylustrator
plt.show()



