import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import csd_tool as ct
from tools import nn_tool as nt
from tools import nnm_plot as nnmp
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
    c_img = []  # for normalization, csd
    names = ['CSD']  # plot title
    conds = ['Control', 'NN-ON', 'NN-OFF', 'WN-OFF']

    # col map
    # csmap = [1, 2]

    lvp = lvl

    c_fig = plt.figure(0, figsize=(14, 18))

    axes = c_fig.subplots(len(lvp), 4)

    for i in range(len(lvp)):

        temp = [
                   csds[lvp[i]][0], csds[lvp[i]][1],
                   csds[lvp[i]][2], csds[lvp[i]][3]
                   ]
        pcsd = nt.dat_unit(temp, 'csd')
        for j in range(len(pcsd)):

            csm = ct.heat_plot(
                pcsd[j], axes[i, j],
                type='csd', zoom='no'
                )
            c_img = np.append(c_img, csm)

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
                axes[i, j].text(0.5, 0, f'{conds[j]}',
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

    mx = nnmp.norm_color(c_img, 'csd', 0.7)

    for i in range(len(lvp)):
        for j in range(len(conds)):
            nnmp.colorbar_set(c_fig, axes[i, j], mx, c_img[j], 'csd')

    # % start: automatic generated code from pylustrator

    # % start: automatic generated code from pylustrator
    plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
    import matplotlib as mpl

    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.279327, 0.314947, 0.623489, 0.024247])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.274225, 0.312325, 0.639816, 0.024882])
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
    plt.figure(0).axes[0].set_position(
        [0.274225, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[0].texts[0].set_position([-0.780339, 0.500000])
    plt.figure(0).axes[0].texts[1].set_position([0.500000, 1.085756])
    plt.figure(0).axes[1].set_position(
        [0.440684, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.085229])
    plt.figure(0).axes[2].set_position(
        [0.606123, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[2].texts[0].set_position([0.500000, 1.085229])
    plt.figure(0).axes[3].set_position(
        [0.772583, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[3].texts[0].set_position([0.500000, 1.085229])
    plt.figure(0).axes[4].set_position(
        [0.274225, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[4].texts[0].set_position([-0.780339, 0.500000])
    plt.figure(0).axes[4].texts[1].set_position([-0.480339, -0.092663])
    plt.figure(0).axes[5].set_position(
        [0.440684, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[6].set_position(
        [0.606123, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[7].set_position(
        [0.772583, 0.637512, 0.141457, 0.117174])
    plt.figure(0).axes[7].texts[0].set_position([-1.209613, -0.283255])
    plt.figure(0).axes[8].set_position(
        [0.274225, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[8].texts[0].set_position([-0.780339, 0.500000])
    plt.figure(0).axes[9].set_position(
        [0.440684, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[10].set_position(
        [0.606123, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[11].set_position(
        [0.772583, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[12].set_position(
        [0.274225, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[12].texts[0].set_position([-0.780339, 0.500000])
    plt.figure(0).axes[13].set_position(
        [0.440684, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[14].set_position(
        [0.606123, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[15].set_position(
        [0.772583, 0.384821, 0.141457, 0.117174])
    # % end: automatic generated code from pylustrator
    #% start: automatic generated code from pylustrator
    plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
    import matplotlib as mpl
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.440684, 0.325767, 0.306896, 0.011935])
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.859507, 0.384820, 0.031833, 0.495180])
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
    plt.figure(0).axes[0].set_position([0.203689, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[1].set_position([0.370148, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[2].set_position([0.535587, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[3].set_position([0.702047, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[4].set_position([0.203689, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[5].set_position([0.370148, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[6].set_position([0.535587, 0.637513, 0.141457, 0.117174])
    plt.figure(0).axes[7].set_position([0.702047, 0.637512, 0.141457, 0.117174])
    plt.figure(0).axes[8].set_position([0.203689, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[9].set_position([0.370148, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[10].set_position([0.535587, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[11].set_position([0.702047, 0.511087, 0.141457, 0.117174])
    plt.figure(0).axes[12].set_position([0.203689, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[13].set_position([0.370148, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[14].set_position([0.535587, 0.384820, 0.141457, 0.117174])
    plt.figure(0).axes[15].set_position([0.702047, 0.384821, 0.141457, 0.117174])
    #% end: automatic generated code from pylustrator
    plt.show()
