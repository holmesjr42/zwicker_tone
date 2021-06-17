import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

from tools import icsd
from tools import nnm_plot as nnmp
from tools import csd_tool as ct
from tools import notch_gap_params as p_tool
import numpy as np
from parameter import parameters as pm
import pickle
import h5py
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import pylustrator
# import seaborn as sns
import quantities as pq
import neo.core

pylustrator.start()

'''
This is for a single data file.
CSD for nnm 3 s/ 1 s condition. Following traditional way with dividing 
with h**2 and no sigma is used. Uses gaussian filter
'''

fnum = 1  # choose which file to use

# setup, some parameters for plots
types = ['spk', 'lfp', 'csd']
ccmap = []
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
sets = val.extra_setup()

for i in types:
    temp = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap=i)
    ccmap.append(temp.values()[-1])  # heatmap color for types
print(ccmap)
comm = pm.Commonfeat
b_list = comm.list_freq  # list of the 1/8 octave frequency to find index

sr_lfp = 1061.5 * pq.Hz  # for convert time into data coord in the data file
bf = 11314  # best frequencies for 121c and 122b
oct_cut = p_tool.o_cut(bf)  # octave transform
lv = '60'  # which SPL dB?
ch = [1, 8]  # which channle?
cond = ['nn', 'si']
control = ['strf_4', 'strf_1']
lfp = []
csd = []

# neo csd process setup
coord = np.arange(0, 1501, 100) * pq.micrometer
sigma = 1 / (100 * pq.micrometer)
file_path = '/home/bhc/OneDrive/'
# files I'm using for this analysis
file_input1 = [
    f'{file_path}Work/PhD/projects/zwicker_tone_2018_2021' \
    '/data/dataset/nnm_spk_lfp_avg/cr121c_210503_spk_lfp_avg_nnm'
    '.hdf5',
    f'{file_path}Work/PhD/projects/zwicker_tone_2018_2021' \
    '/data/dataset/nnm_spk_lfp_avg/cr122b_210604_spk_lfp_avg_nnm'
    '.hdf5'
]
file_input = file_input1[fnum]

# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]

# loading file
with h5py.File(file_input, 'r') as dat:
    b_ind = np.where(b_list == bf)[0][0]

    lp = [
             dat['lfp'][control[fnum]][lv],
             dat['lfp']['nnm_3_1']['nn'][lv],
             dat['lfp']['nnm_3_1']['si'][lv]
         ] * pq.microvolt

    lp.units = pq.mV

    for i in range(len(lp)):
        lfp.append(lp[i][ch[fnum]][oct_cut[0]:oct_cut[1] + 1])
    print(np.shape(lfp))

    spk = [
              dat['spk'][control[fnum]][lv][ch[fnum]][oct_cut[0]:oct_cut[1] + 1],
              dat['spk']['nnm_3_1']['nn'][lv][ch[fnum]][oct_cut[0]:oct_cut[1] + 1],
              dat['spk']['nnm_3_1']['si'][lv][ch[fnum]][oct_cut[0]:oct_cut[1] + 1]
          ] * pq.ms ** (-1)

    spk.units = pq.s ** (-1)
    for i in range(len(lp)):
        lfp_neo = neo.core.AnalogSignal(lp[i][:, b_ind].T, sampling_rate=sr_lfp)

        csd.append(ct.csd_calc(lfp_neo, 'gaussian', (3, 1)))

data = [spk, lfp, csd]
mnl = []
mxs = []
for i in range(3):

    a = np.max(spk[i][12][13:30])
    b = np.min(lfp[i][12][19:30])
    mxs.append(a)
    mnl.append(b)
# plot start
p_img = [[] for _ in range(3)]  # for normalizing heatmap

p_fig = plt.figure(0, figsize=(18, 12))

p_axs = p_fig.subplots(3, 3)

title = sets[6][0:3]  # title of plots

for i in range(len(types)):
    for j in range(len(title)):
        p_dat = data[i][j]
        axes = [p_axs[i, 0], p_axs[i, 1], p_axs[i, 2]]

        if types[i] == 'csd':
            c_im = ct.heat_plot(p_dat, axes[j], type='csd')
            p_img[i].append(c_im)

        else:
            nnmp.nnm_plot(
                axes[j], p_dat, p_img[i], ccmap[i], type='octave')



        if i == 0:
            axes[j].set_title(title[j], fontdict={'fontsize': 30})
            axes[j].label_outer()
        elif i != 2:
            axes[j].axes.yaxis.set_ticklabels([])

        elif i == 2:
            axes[1].axes.yaxis.set_ticklabels([])
            axes[2].axes.yaxis.set_ticklabels([])

# p_axs[1, 0].text(0, 0.5, f'{lv} dB',
#                  horizontalalignment='center',
#                  verticalalignment='center',
#                  rotation='vertical',
#                  transform=p_axs[1, 0].transAxes,
#                  fontdict={'weight': 'bold', 'size': 30}
#                  )

# unit text
p_axs[0, 0].text(0, -0.5, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=p_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

p_axs[2, 0].text(0, 0.5, f'Depth' + ' (' + r'$\mu$' + 'm' + ')',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=p_axs[2, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

p_axs[1, 1].text(0.5, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=p_axs[1, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

mx = [
    nnmp.norm_color(p_img[0], 'spk', 0.7),
    nnmp.norm_color(p_img[1], 'lfp', 0.8),
    nnmp.norm_color(p_img[2], 'csd', 0.5)
    ]
modes = ['spk', 'lfp', 'csd']
# print(mx)
# colorbar setup
for i in range(len(mx)):
    max = mx[i]
    axes = [p_axs[i, 0], p_axs[i, 1], p_axs[i, 2]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            p_fig, axes[j], p_img[i][0], modes[i],
            vmax=max[1], vmin=max[0], ori='vertical'
            )

print(mxs, mnl)

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.894225, 0.661863, 0.007549, 0.226470])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.891928, 0.110000, 0.008072, 0.242158])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.893009, 0.409890, 0.007549, 0.226470])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.894555, 0.661863, 0.007549, 0.226470])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.379060, 0.661863, 0.150980, 0.226470])
plt.figure(0).axes[0].texts[0].set_position([-0.465018, 0.051947])
plt.figure(0).axes[1].set_position([0.556756, 0.661863, 0.150980, 0.226470])
plt.figure(0).axes[2].set_position([0.733064, 0.661863, 0.150980, 0.226471])
plt.figure(0).axes[3].set_position([0.379060, 0.409891, 0.150980, 0.226470])
plt.figure(0).axes[4].set_position([0.556757, 0.409891, 0.150980, 0.226470])
plt.figure(0).axes[4].texts[0].set_position([0.601190, -1.591450])
plt.figure(0).axes[5].set_position([0.732459, 0.409890, 0.150980, 0.226471])
plt.figure(0).axes[6].set_position([0.379060, 0.110000, 0.151586, 0.242158])
plt.figure(0).axes[6].texts[0].set_position([-0.463163, 0.499795])
plt.figure(0).axes[7].set_position([0.556757, 0.110000, 0.151586, 0.242158])
plt.figure(0).axes[8].set_position([0.731854, 0.110000, 0.151586, 0.242158])
#% end: automatic generated code from pylustrator
plt.show()