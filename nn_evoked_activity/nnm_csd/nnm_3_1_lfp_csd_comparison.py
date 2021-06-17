import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import csd_tool as ct
from tools import nn_tool as nt
import numpy as np
from parameters import parameters as pm
import h5py
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import quantities as pq
import pylustrator

sys.path.pop(1)
pylustrator.start()
'''
This is for a single data file.
CSD for nnm continuous condition. Following traditional way with dividing
with h**2 and no sigma is used. Uses rappel filter
'''

comm = pm.Commonfeat
bfs = comm.bf_dic  # best frequency dictionary\\
b_list = comm.list_freq  # list of the 1/8 octave frequency to find index
# for bf/cf frequency
db = comm.db
lfp = []  # dict of lfp: 0, ctrl; 1, nn
csds = []  # this is dict to store csd data
lv = '50'  # SPL dB I'm going to use for this comparison
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')
ccmap = val.values()[-1]
lcmap = val2.values()[-1]
cond = ['nnm_3_1', 'nnm_wn_3_1']
data = {'lfp': [], 'csd': []}  # data dict for plotting
d_list = list(data.keys())
# file_input = snakemake.input[0]
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_lfp_avg/csd_lfp_avg_nnm.hdf5'

# loading data
with h5py.File(file_input, 'r') as dat:
    for d in d_list:
        data[d].append(dat[d]['nnm_3_1_strf'][lv])
        for c in range(len(cond)):
            if cond[c] == cond[0]:
                for i in range(2):
                    data[d].append(dat[d][cond[c]][lv][i])
            elif cond[c] == cond[1]:
                data[d].append(dat[d][cond[c]][lv][1])
            else:
                print('something is wrong with choosing condition')
                raise ValueError

    '''
    plot
    '''
    # setup
    imgs = [[] for _ in range(len(d_list))]
    # for normalization, 0, lfp; 1, csd
    names = ['LFP', 'CSD']  # plot title
    conds = ['Control', 'NN-ON', 'NN-OFF', 'WN-OFF']

    c_fig = plt.figure(0, figsize=(16, 9))

    axes = c_fig.subplots(len(d_list), len(conds))

    # pcsd = [csds[0], csds[1]] * pq.mV / (pq.mm ** 2)
    # plfp = [lfp[0], lfp[1]] * pq.microvolt
    # plfp.units = pq.mV

    for d in range(len(d_list)):
        dp = data[d_list[d]]
        for c in range(len(conds)):
            cp = nt.dat_unit(dp[c], d_list[d])
            img = ct.heat_plot(cp, axes[d, c], type=d_list[d], zoom='no')
            imgs[d].append(img)

            axes[d, c].label_outer()

            if d == 0:
                axes[0, c].text(.5, 1, f'{conds[c]}',
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation='horizontal',
                                transform=axes[0, c].transAxes,
                                fontdict={'weight': 'bold',
                                          'size': 25
                                          })

        ct.norm_color(imgs[d], d_list[d], ratio=0.8)

        for c in range(len(conds)):
            cb = plt.colorbar(imgs[d][c], ax=axes[d, c],
                              orientation='vertical', format='%.2f',
                              ticks=ticker.MaxNLocator(3))

            ct.cbar_t(cb, d_list[d])

        axes[d, 0].text(0, 0.5, f'{names[d]}',
                        horizontalalignment='center',
                        verticalalignment='center',
                        rotation='vertical',
                        transform=axes[d, 0].transAxes,
                        fontdict={'weight': 'bold',
                                  'size': 25
                                  })


    axes[1, 1].text(.5, 0, f't (ms)',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='horizontal',
                    transform=axes[1, 1].transAxes,
                    fontdict={'weight': 'bold', 'size': 23}
                    )

    axes[0, 0].text(-.5, 0, f'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='vertical',
                    transform=axes[0, 0].transAxes,
                    fontdict={'weight': 'bold', 'size': 23}
                    )




#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.872937, 0.429571, 0.007177, 0.255188])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.872228, 0.157332, 0.007179, 0.255262])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.872228, 0.430012, 0.007179, 0.255262])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].yaxis.labelpad = -120.247198
plt.figure(0).axes[0].set_position([0.261811, 0.429650, 0.134783, 0.255188])
plt.figure(0).axes[0].texts[0].set_position([0.500000, 1.069665])
plt.figure(0).axes[0].texts[1].set_position([-0.639445, 0.508708])
plt.figure(0).axes[0].texts[2].set_position([-0.370161, -0.000000])
plt.figure(0).axes[1].set_position([0.418307, 0.429571, 0.134783, 0.255188])
plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.074019])
plt.figure(0).axes[2].set_position([0.575049, 0.429571, 0.134783, 0.255188])
plt.figure(0).axes[2].texts[0].set_position([0.500000, 1.074019])
plt.figure(0).axes[3].set_position([0.731545, 0.429571, 0.134783, 0.255188])
plt.figure(0).axes[3].texts[0].set_position([0.500000, 1.074019])
plt.figure(0).axes[4].set_position([0.261875, 0.157406, 0.134783, 0.255188])
plt.figure(0).axes[4].texts[0].set_position([-0.639919, 0.500000])
plt.figure(0).axes[5].set_position([0.418430, 0.157480, 0.134783, 0.255188])
plt.figure(0).axes[5].texts[0].set_position([1.084274, -0.283015])
plt.figure(0).axes[6].set_position([0.574973, 0.157406, 0.134783, 0.255188])
#% end: automatic generated code from pylustrator
plt.show()
