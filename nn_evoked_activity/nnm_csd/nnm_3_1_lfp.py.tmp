import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import csd_tool as ct
from tools import nnm_plot as nnmp
from tools import nn_tool as nt
import numpy as np
from parameters import parameters as pm
import h5py
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import quantities as pq
import neo.core
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
lvl = db['lv']  # SPLdB list
lfp = {}  # dict of lfp: 0, ctrl; 1, nn
csds = {}  # this is dict to store csd data

val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')
ccmap = val.values()[-1]
lcmap = val2.values()[-1]
cond = ['nnm_3_1_strf', 'nnm_3_1', 'nnm_wn_3_1']

# file_input = snakemake.input[0]
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_lfp_avg/csd_lfp_avg_nnm.hdf5'

# loading data
with h5py.File(file_input, 'r') as dat:
    for lv in lvl:
        lfp[lv] = []
        csds[lv] = []
        for c in range(len(cond)):
            if cond[c] == cond[0]:
                lfp[lv].append(dat['lfp'][cond[c]][lv])
                csds[lv].append(dat['csd'][cond[c]][lv])
            elif cond[c] == cond[1]:
                # nn-on/off range 2
                for k in range(2):
                    lfp[lv].append(dat['lfp'][cond[c]][lv][k])
                    csds[lv].append(dat['csd'][cond[c]][lv][k])
            else:
                # wn-off
                lfp[lv].append(dat['lfp'][cond[c]][lv][1])
                csds[lv].append(dat['csd'][cond[c]][lv][1])

    '''
    plot
    '''
    # setup
    l_img = []  # for normalization, csd
    names = ['LFP']  # plot title
    conds = ['Control', 'NN-ON', 'NN-OFF', 'WN-OFF']

    # col map
    # csmap = [1, 2]

    lvp = lvl

    c_fig = plt.figure(0, figsize=(14, 18))

    axes = c_fig.subplots(len(lvp), 4)

    for i in range(len(lvp)):

        temp = [
                   lfp[lvp[i]][0], lfp[lvp[i]][1],
                   lfp[lvp[i]][2], lfp[lvp[i]][3]
                   ]

        plfp = nt.dat_unit(temp)
        
        for j in range(len(plfp)):

            lsm = ct.heat_plot(plfp[j], axes[i, j], type='lfp')
            l_img = np.append(l_img, lsm)

            if j == 0:
                axes[i, j].text(-.6, .5, f'{lvp[i]} dB',
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation='vertical',
                                transform=axes[i, j].transAxes,
                                fontdict={'weight': 'bold', 'size': 25}
                                )

            axes[i, j].label_outer()

            if i == 0:
                axes[i, j].text(0.5, 1, f'{conds[j]}',
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation='horizontal',
                                transform=axes[i, j].transAxes,
                                fontdict={'weight': 'bold',
                                          'size': 25
                                          })

    axes[1, 3].text(.5, -.5, f't (ms)',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='horizontal',
                    transform=axes[3, 3].transAxes,
                    fontdict={'weight': 'bold', 'size': 23}
                    )

    axes[1, 0].text(-.3, .5, f'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='vertical',
                    transform=axes[1, 0].transAxes,
                    fontdict={'weight': 'bold', 'size': 23}
                    )

    mn = nnmp.norm_color(l_img, 'lfp', ratio=0.7)

    for i in range(len(lvp)):
        for j in range(len(conds)):
            lb = nnmp.colorbar_set(
                c_fig, axes[j, i], mn, l_img[j], types='lfp'
                )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.901027, 0.188061, 0.035356, 0.549989])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.856827, 0.188061, 0.035356, 0.549989])
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
plt.figure(0).axes[0].set_position([0.146429, 0.608263, 0.156685, 0.129787])
plt.figure(0).axes[0].texts[0].set_position([-0.698773, 0.500000])
plt.figure(0).axes[0].texts[1].set_position([0.500000, 1.078476])
plt.figure(0).axes[1].set_position([0.325984, 0.608263, 0.156685, 0.129787])
plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.078476])
plt.figure(0).axes[2].set_position([0.505539, 0.608263, 0.156685, 0.129787])
plt.figure(0).axes[2].texts[0].set_position([0.500000, 1.078476])
plt.figure(0).axes[3].set_position([0.685094, 0.608263, 0.156685, 0.129787])
plt.figure(0).axes[3].texts[0].set_position([0.500000, 1.078476])
plt.figure(0).axes[4].set_position([0.147620, 0.469430, 0.156685, 0.129787])
plt.figure(0).axes[4].texts[0].set_position([-0.698773, 0.500000])
plt.figure(0).axes[4].texts[1].set_position([-0.436762, -0.027930])
plt.figure(0).axes[5].set_position([0.327174, 0.469430, 0.156685, 0.129787])
plt.figure(0).axes[6].set_position([0.506729, 0.469430, 0.156685, 0.129787])
plt.figure(0).axes[7].set_position([0.685094, 0.468504, 0.156685, 0.129787])
plt.figure(0).axes[7].texts[0].set_position([-1.171542, -0.278840])
plt.figure(0).axes[8].set_position([0.147620, 0.329672, 0.156685, 0.129787])
plt.figure(0).axes[8].texts[0].set_position([-0.698773, 0.500000])
plt.figure(0).axes[9].set_position([0.325984, 0.329672, 0.156685, 0.129787])
plt.figure(0).axes[10].set_position([0.505539, 0.329672, 0.156685, 0.129787])
plt.figure(0).axes[11].set_position([0.685093, 0.329672, 0.156685, 0.129787])
plt.figure(0).axes[12].set_position([0.146429, 0.188061, 0.156685, 0.129787])
plt.figure(0).axes[12].texts[0].set_position([-0.698773, 0.500000])
plt.figure(0).axes[13].set_position([0.327174, 0.188987, 0.156685, 0.129787])
plt.figure(0).axes[14].set_position([0.505539, 0.188061, 0.156685, 0.129787])
plt.figure(0).axes[15].set_position([0.685094, 0.188061, 0.156685, 0.129787])
#% end: automatic generated code from pylustrator
plt.show()
