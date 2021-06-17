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

dbs, db, dcmap, names, legendl, chl, l_list, layer_name = val.nn11_plot()
legends = legendl[1]

nn = 'nn_1_1_nt'
wn = 'nn_wn_1_1_nt'
db_n = 1
file ="/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
      "/dataset/nn_mean/cl116_210318_nn_mean.hdf5"
ch_l = [0, 8, 15]
with h5py.File(file, 'r') as dat:
    lfp = dat['lfp']['mean']
    spk = dat['spk']['s_psth']
    st = dat['spk']['time'][nn][0]

    lt = np.linspace(
        0, 2100, num=len(lfp[nn][0][0]), endpoint=False
        )


    n_fig = plt.figure(0, figsize=(16, 9))
    n_axs = n_fig.subplots(3, 4)

    for i in range(len(ch_l)):
        # onset
        ch = ch_l[i]
        n_axs[i, 2].plot(lt, lfp[nn][db_n][ch], label='NN-ON')
        n_axs[i, 2].plot(lt, lfp[wn][db_n][ch], label='WN-ON')
        n_axs[i, 0].plot(st, spk[nn][db_n][ch], label='NN-ON')
        n_axs[i, 0].plot(st, spk[wn][db_n][ch], label='WN-ON')

        # offset
        n_axs[i, 3].plot(lt, lfp[nn][db_n][ch], label='NN-OFF')
        n_axs[i, 3].plot(lt, lfp[wn][db_n][ch], label='WN-OFF')
        n_axs[i, 1].plot(st, spk[nn][db_n][ch], label='NN-OFF')
        n_axs[i, 1].plot(st, spk[wn][db_n][ch], label='WN-OFF')

        n_axs[i, 2].set_xlim(0, 150)
        n_axs[i, 3].set_xlim(900, 1200)
        # n_axs[i, 3].set_ylim(-0.02, 0.01)
        n_axs[i, 0].set_xlim(0, 150)
        n_axs[i, 1].set_xlim(900, 1200)
        # n_axs[i, 1].set_ylim(0, 0.06)


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



