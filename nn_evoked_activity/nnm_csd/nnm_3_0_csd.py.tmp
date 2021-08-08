import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import nnm_plot as nnmp
import numpy as np
from parameter import parameters as pm
import h5py
import matplotlib.pyplot as plt
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
lvl = db['lv']  # SPLdB list
lfp = {}  # dict of lfp: 0, ctrl; 1, nn
csds = {}  # this is dict to store csd data

ccmap = pm.Setup(hcmap_mode='csd', mode='fun').hcmap
lcmap = pm.Setup(hcmap_mode='lfp', mode='fun').hcmap
line_c = pm.Setup(mode='fun').ref_line_color

cond = [pm.Setup().c_s[0], pm.Setup().c_n[0]]

# file_input = snakemake.input[0]
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_lfp_avg/csd_lfp_avg_nnm.hdf5'

# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]
# loading data
with h5py.File(file_input, 'r') as dat:
    if '30' in list(dat['lfp'][cond[0]].keys()):
        dat['lfp'][cond[0]].pop('30')
        dat['csd'][cond[0]].pop('30')
    else:
        pass

    if '30' in list(dat['lfp'][cond[1]].keys()):
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
    # names = ['LFP', 'CSD']  # plot title
    conds = ['Control', 'NN']

    # col map
    lfmap = [0, 3]
    csmap = [1, 2]

    lvp = lvl

    c_fig = plt.figure(0, figsize=(15, 18))

    axes = c_fig.subplots(len(lvp), 4)

    for i in range(len(lvp)):

        plfp = [lfp[lvp[i]][0], lfp[lvp[i]][1]] * pq.microvolt
        plfp.units = pq.mV

        pcsd = [csds[lvp[i]][0], csds[lvp[i]][1]] * pq.mV / (pq.mm ** 2)

        for j in range(len(plfp)):
            mps = [lfmap[j], csmap[j]]

            lfm = nnmp.heat_plot(plfp[j], axes[i, mps[0]], l_img, clmap=lcmap, hcolor=line_c)
            csm = nnmp.heat_plot(pcsd[j], axes[i, mps[1]], c_img, clmap=ccmap, hcolor=line_c)

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

# plot texts
axes[0, 0].text(1, 1, f'{conds[0]}',
                horizontalalignment='center',
                verticalalignment='center',
                rotation='horizontal',
                transform=axes[0, 0].transAxes,
                fontdict={'weight': 'bold',
                          'size': 25
                          })

axes[0, 2].text(1, 1, f'{conds[1]}',
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

# axes[1, 0].text(-.3, .5, f'Depth' + ' (' + r'$\mu$' + 'm' + ')',
#                 horizontalalignment='center',
#                 verticalalignment='center',
#                 rotation='vertical',
#                 transform=axes[len(lvp) - 1, 1].transAxes,
#                 fontdict={'weight': 'bold', 'size': 23}
#                 )

axes[1, 0].text(0, 0, 'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                horizontalalignment='center',
                verticalalignment='center',
                rotation='vertical',
                transform=axes[1, 0].transAxes,
                fontdict={'weight': 'bold', 'size': 23}
                )

lmn, lmx = nnmp.norm_color(l_img, 'lfp', 0.8)
cmn, cmx = nnmp.norm_color(c_img, 'csd', 0.4)

l_cbaxs_0 = c_fig.add_axes([0.5, 0.5, 0.3, 0.01])
c_cbaxs_0 = c_fig.add_axes([0.5, 0.8, 0.3, 0.01])
l_cbaxs_1 = c_fig.add_axes([0.8, 0.5, 0.3, 0.01])
c_cbaxs_1 = c_fig.add_axes([0.8, 0.8, 0.3, 0.01])

l_cbar_0 = nnmp.colorbar_set(c_fig, l_cbaxs_0, l_img[0], types='lfp', vmax=lmx, vmin=lmn, ori='horizontal')
c_cbar_0 = nnmp.colorbar_set(c_fig, c_cbaxs_0, c_img[0], types='csd', vmax=cmx, vmin=cmn, ori='horizontal')

l_cbar_1 = nnmp.colorbar_set(c_fig, l_cbaxs_1, l_img[0], types='lfp', vmax=lmx, vmin=lmn, ori='horizontal')
c_cbar_1 = nnmp.colorbar_set(c_fig, c_cbaxs_1, c_img[0], types='csd', vmax=cmx, vmin=cmn, ori='horizontal')

# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl

plt.figure(0).axes[0].set_position([0.106429, 0.726526, 0.168478, 0.139556])
plt.figure(0).axes[0].texts[0].set_position([-0.489770, 0.500000])
plt.figure(0).axes[1].set_position([0.308602, 0.726526, 0.168478, 0.139556])
plt.figure(0).axes[2].set_position([0.580776, 0.726526, 0.168478, 0.139556])
plt.figure(0).axes[3].set_position([0.782950, 0.726526, 0.168478, 0.139556])
plt.figure(0).axes[4].set_position([0.106429, 0.525657, 0.168478, 0.139556])
plt.figure(0).axes[4].texts[0].set_position([-0.489770, 0.500000])
plt.figure(0).axes[5].set_position([0.308602, 0.525657, 0.168478, 0.139556])
plt.figure(0).axes[6].set_position([0.580776, 0.525657, 0.168478, 0.139556])
plt.figure(0).axes[7].set_position([0.782950, 0.525657, 0.168478, 0.139556])
plt.figure(0).axes[8].set_position([0.106429, 0.324787, 0.168478, 0.139556])
plt.figure(0).axes[8].texts[0].set_position([-0.489770, 0.500000])
plt.figure(0).axes[9].set_position([0.308602, 0.324787, 0.168478, 0.139556])
plt.figure(0).axes[10].set_position([0.580776, 0.324787, 0.168478, 0.139556])
plt.figure(0).axes[11].set_position([0.782950, 0.324787, 0.168478, 0.139556])
plt.figure(0).axes[12].set_position([0.106429, 0.123918, 0.168478, 0.139556])
plt.figure(0).axes[12].texts[0].set_position([-0.489770, 0.500000])
plt.figure(0).axes[13].set_position([0.308602, 0.123918, 0.168478, 0.139556])
plt.figure(0).axes[14].set_position([0.580776, 0.123918, 0.168478, 0.139556])
plt.figure(0).axes[15].set_position([0.782950, 0.123918, 0.168478, 0.139556])
plt.figure(0).axes[17].set_position([0.270031, 0.927396, 0.300000, 0.010000])
# % end: automatic generated code from pylustrator
#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.158712, 0.726525, 0.157246, 0.139556])
plt.figure(0).axes[0].texts[0].set_position([-0.828941, 0.493365])
plt.figure(0).axes[0].texts[1].set_position([1.120123, 1.159235])
plt.figure(0).axes[1].set_position([0.364218, 0.726526, 0.157246, 0.139556])
plt.figure(0).axes[2].set_position([0.604170, 0.726525, 0.157246, 0.139556])
plt.figure(0).axes[2].texts[0].set_position([1.134255, 1.159235])
plt.figure(0).axes[3].set_position([0.809676, 0.726525, 0.157246, 0.139556])
plt.figure(0).axes[4].set_position([0.158712, 0.575657, 0.157246, 0.139556])
plt.figure(0).axes[4].texts[0].set_position([-0.828941, 0.500000])
plt.figure(0).axes[4].texts[1].set_position([-0.537021, 0.000000])
plt.figure(0).axes[5].set_position([0.364218, 0.575657, 0.157246, 0.139556])
plt.figure(0).axes[6].set_position([0.604170, 0.575656, 0.157246, 0.139556])
plt.figure(0).axes[7].set_position([0.809676, 0.575656, 0.157246, 0.139556])
plt.figure(0).axes[8].set_position([0.158712, 0.423861, 0.157246, 0.139556])
plt.figure(0).axes[8].texts[0].set_position([-0.828941, 0.500000])
plt.figure(0).axes[9].set_position([0.364218, 0.423861, 0.157246, 0.139556])
plt.figure(0).axes[10].set_position([0.604170, 0.423859, 0.157246, 0.139556])
plt.figure(0).axes[11].set_position([0.809676, 0.423859, 0.157246, 0.139556])
plt.figure(0).axes[12].set_position([0.158712, 0.271140, 0.157246, 0.139556])
plt.figure(0).axes[12].texts[0].set_position([-0.828941, 0.500000])
plt.figure(0).axes[13].set_position([0.364218, 0.271140, 0.157246, 0.139556])
plt.figure(0).axes[13].texts[0].set_position([1.298465, -0.347400])
plt.figure(0).axes[14].set_position([0.604170, 0.271140, 0.157246, 0.139556])
plt.figure(0).axes[15].set_position([0.809676, 0.271140, 0.157246, 0.139556])
plt.figure(0).axes[16].set_position([0.158712, 0.173669, 0.157246, 0.010000])
plt.figure(0).axes[17].set_position([0.364218, 0.173669, 0.157246, 0.010000])
plt.figure(0).axes[18].set_position([0.809676, 0.173669, 0.157246, 0.010000])
plt.figure(0).axes[19].set_position([0.604170, 0.173669, 0.157246, 0.010000])
#% end: automatic generated code from pylustrator
plt.show()
