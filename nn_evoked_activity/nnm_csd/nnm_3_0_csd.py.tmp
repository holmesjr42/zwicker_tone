import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import csd_tool as ct
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
cond = ['nnm_3_0_strf', 'nnm_3_0']

# file_input = snakemake.input[0]
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_lfp_avg/csd_lfp_avg_nnm.hdf5'

# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]
# loading data
with h5py.File(file_input, 'r') as dat:
    if '30' in list(dat['lfp']['nnm_3_0_strf'].keys()):
        dat['lfp'][cond[0]].pop('30')
        dat['csd'][cond[0]].pop('30')
    else:
        pass

    if '30' in list(dat['lfp']['nnm_3_0'].keys()):
        dat['lfp'][cond[1]].pop('30')
        dat['csd'][cond[1]].pop('30')
    else:
        pass

    for lv in lvl:
        lfp[lv] = []
        csds[lv] = []
        for c in range(len(cond)):
            lfp[lv].append(dat['lfp'][cond[c]][lv])
            csds[lv].append(dat['csd'][cond[c]][lv])

    '''
    plot
    '''
    # setup
    l_img = []  # for normalization, lfp
    c_img = []  # for normalization, csd
    names = ['LFP', 'CSD']  # plot title
    conds = ['CTRL', 'NN']

    # col map
    lfmap = [0, 3]
    csmap = [1, 2]

    lvp = lvl

    c_fig = plt.figure(0, figsize=(14, 18))

    axes = c_fig.subplots(len(lvp), 4)

    for i in range(len(lvp)):

        plfp = [lfp[lvp[i]][0], lfp[lvp[i]][1]] * pq.microvolt
        plfp.units = pq.mV

        pcsd = [csds[lvp[i]][0], csds[lvp[i]][1]] * pq.mV / (pq.mm ** 2)

        for j in range(len(plfp)):
            mps = [lfmap[j], csmap[j]]

            lfm = ct.heat_plot(plfp[j], axes[i, mps[0]])
            csm = ct.heat_plot(pcsd[j], axes[i, mps[1]], type='csd')
            l_img.append(lfm)
            c_img.append(csm)

            if mps[0] == 0:
                axes[i, mps[0]].text(-.6, .5, f'{lvp[i]} dB',
                                     horizontalalignment='center',
                                     verticalalignment='center',
                                     rotation='vertical',
                                     transform=axes[i, mps[0]].transAxes,
                                     fontdict={'weight': 'bold', 'size': 25}
                                     )

            if i != len(lvp) - 1:
                for k in [0, 1]:
                    axes[i, mps[k]].get_xaxis().set_ticks([])

            for k in [0, 1]:
                if mps[k] != 0:
                    axes[i, mps[k]].get_yaxis().set_ticks([])

    axes[0, 0].text(0, 0, f'{conds[0]}',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='horizontal',
                    transform=axes[0, 0].transAxes,
                    fontdict={'weight': 'bold',
                              'size': 25
                              })

    axes[0, 2].text(0, 0, f'{conds[1]}',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='horizontal',
                    transform=axes[0, 2].transAxes,
                    fontdict={'weight': 'bold',
                              'size': 25
                              })

    axes[len(lvp) - 1, 1].text(.5, -.5, f't (ms)',
                               horizontalalignment='center',
                               verticalalignment='center',
                               rotation='horizontal',
                               transform=axes[len(lvp) - 1, 1].transAxes,
                               fontdict={'weight': 'bold', 'size': 23}
                               )

    axes[1, 0].text(-.3, .5, f'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                    horizontalalignment='center',
                    verticalalignment='center',
                    rotation='vertical',
                    transform=axes[len(lvp) - 1, 1].transAxes,
                    fontdict={'weight': 'bold', 'size': 23}
                    )

    ct.norm_color(l_img, 'lfp')
    ct.norm_color(c_img, 'csd', ratio=0.4)

    for i in range(len(lvp)):
        for j in range(len(lfmap)):
            mps = [lfmap[j], csmap[j]]
            lb = plt.colorbar(l_img[i], ax=axes[i, mps[0]],
                              orientation='horizontal', format='%.2f',
                              ticks=ticker.MaxNLocator(3))

            cb = plt.colorbar(c_img[i], ax=axes[i, mps[1]],
                              orientation='horizontal', format='%.2f',
                              ticks=ticker.MaxNLocator(3))

            ct.cbar_t(lb, 'lfp')
            ct.cbar_t(cb, 'csd')

    # % start: automatic generated code from pylustrator
    plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
    import matplotlib as mpl

    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.823604, 0.329952, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.502113, 0.329952, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.662858, 0.329426, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.311778, 0.329952, 0.168478, 0.006552])
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
        [0.340684, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[0].texts[0].set_position([-0.953463, 0.500000])
    plt.figure(0).axes[1].set_position(
        [0.502113, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[2].set_position(
        [0.662858, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[3].set_position(
        [0.823604, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[4].set_position(
        [0.340227, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[4].texts[0].set_position([-0.953463, 0.500000])
    plt.figure(0).axes[4].texts[1].set_position([-1.723952, 2.145640])
    plt.figure(0).axes[5].set_position(
        [0.501656, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[6].set_position(
        [0.662401, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[7].set_position(
        [0.823147, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[8].set_position(
        [0.338799, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[8].texts[0].set_position([-0.953463, 0.500000])
    plt.figure(0).axes[9].set_position(
        [0.501656, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[10].set_position(
        [0.662401, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[11].set_position(
        [0.823147, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[12].set_position(
        [0.339256, 0.389136, 0.141457, 0.117174])
    plt.figure(0).axes[12].texts[0].set_position([-0.953463, 0.500000])
    plt.figure(0).axes[13].set_position(
        [0.502113, 0.389136, 0.141457, 0.117174])
    plt.figure(0).axes[13].texts[0].set_position([1.055442, -0.281901])
    plt.figure(0).axes[14].set_position(
        [0.661430, 0.389136, 0.141457, 0.117174])
    plt.figure(0).axes[15].set_position(
        [0.823604, 0.389136, 0.141457, 0.117174])
    # % end: automatic generated code from pylustrator
    # % start: automatic generated code from pylustrator
    plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
    import matplotlib as mpl

    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.314465, 0.328864, 0.143342, 0.005574])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.823604, 0.329961, 0.141000, 0.005483])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.655152, 0.330495, 0.141000, 0.005483])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.484309, 0.330495, 0.141000, 0.005483])
    plt.figure(0).ax_dict["<colorbar>"].set_position(
        [0.317778, 0.330495, 0.142428, 0.005539])
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
        [0.318235, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[0].texts[0].set_position([-0.910182, 0.500000])
    plt.figure(0).axes[0].texts[1].set_position([1.095018, 1.242222])
    plt.figure(0).axes[1].set_position(
        [0.484766, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[2].set_position(
        [0.654695, 0.762826, 0.141457, 0.117174])
    plt.figure(0).axes[2].texts[0].set_position([1.084919, 1.242222])
    plt.figure(0).axes[4].set_position(
        [0.317778, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[4].texts[0].set_position([-0.910182, 0.500000])
    plt.figure(0).axes[4].texts[1].set_position([-1.760020, 2.145640])
    plt.figure(0).axes[5].set_position(
        [0.484309, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[6].set_position(
        [0.654238, 0.639108, 0.141457, 0.117174])
    plt.figure(0).axes[8].set_position(
        [0.316350, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[8].texts[0].set_position([-0.910182, 0.500000])
    plt.figure(0).axes[9].set_position(
        [0.484309, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[10].set_position(
        [0.654238, 0.514463, 0.141457, 0.117174])
    plt.figure(0).axes[12].set_position(
        [0.316807, 0.389136, 0.141457, 0.117174])
    plt.figure(0).axes[12].texts[0].set_position([-0.910182, 0.500000])
    plt.figure(0).axes[13].set_position(
        [0.484766, 0.389136, 0.141457, 0.117174])
    plt.figure(0).axes[14].set_position(
        [0.653267, 0.389136, 0.141457, 0.117174])
    # % end: automatic generated code from pylustrator
    #% start: automatic generated code from pylustrator
    plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
    import matplotlib as mpl
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.823604, 0.329961, 0.141000, 0.005483])
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.823604, 0.330477, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.654695, 0.330477, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.485786, 0.330477, 0.141457, 0.005501])
    plt.figure(0).ax_dict["<colorbar>"].set_position([0.318235, 0.330477, 0.141914, 0.005519])
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
    #% end: automatic generated code from pylustrator
    plt.show()
