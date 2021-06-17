import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from tools import nnm_plot as nnmp
from tools import notch_gap_params as p_tool
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
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap_l = \
    val.values()
ccmap_s = val2.values()[-1]
ccmaps = [ccmap_s, ccmap_l]
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()
lvs = [lvl[1]]  # choose SPL you want to show

file_input1 = [
    '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
    '/data/dataset/nnm_spk_lfp_avg/cr121c_210503_spk_lfp_avg_nnm'
    '.hdf5',
    '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
    '/data/dataset/nnm_spk_lfp_avg/cr122b_210604_spk_lfp_avg_nnm'
    '.hdf5'
    ]
# file_input = snakemake.input[0]


# stimulus conditions for this script
c_n = sets[-8][1]
c_w = sets[-6][0]
c_c1 = ['strf_4', 'strf_1']
lfp = {}  # dict for spk data regarding SPLdB
spk = {}
chs1 = [1, 8]
cf = 11314
ls = []
sps = []
oct_cut = p_tool.o_cut(cf)
# load file
for num in range(len(file_input1)):
    chs = chs1[num]
    file_input = file_input1[num]
    c_c = c_c1[num]
    with h5py.File(file_input, 'r') as dat:
        lp = [
            dat['lfp'][c_c], dat['lfp'][c_n]['nn'],
            dat['lfp'][c_n]['si']
            ]  # lfp

        # for i in lvl:
        #     lfp[i] = [
        #                  np.array(lp[0][i][chs][oct_cut[0]:oct_cut[1] + 1]),
        #                  np.array(lp[1][i][chs][oct_cut[0]:oct_cut[1] + 1]),
        #                  np.array(lp[2][i][chs][oct_cut[0]:oct_cut[1] + 1])
        #                  ] * pq.microvolt
        #
        #     lfp[i].units = pq.mV
        #
        # sp = [
        #     dat['spk'][c_c], dat['spk'][c_n]['nn'],
        #     dat['spk'][c_n]['si']
        #     ]  # lfp
        #
        # for i in lvl:
        #     spk[i] = [
        #                  np.array(sp[0][i][chs][oct_cut[0]:oct_cut[1] + 1]),
        #                  np.array(sp[1][i][chs][oct_cut[0]:oct_cut[1] + 1]),
        #                  np.array(sp[2][i][chs][oct_cut[0]:oct_cut[1] + 1])
        #                  ] * pq.ms ** (-1)
        #
        #     spk[i].units = pq.s ** (-1)
        for i in lvs:
            ls.append([
                         np.array(lp[0][i][chs][oct_cut[0]:oct_cut[1] + 1]),
                         np.array(lp[1][i][chs][oct_cut[0]:oct_cut[1] + 1]),
                         np.array(lp[2][i][chs][oct_cut[0]:oct_cut[1] + 1])
                         ] * pq.microvolt)
            
            ls.units = pq.mV

        sp = [
            dat['spk'][c_c], dat['spk'][c_n]['nn'],
            dat['spk'][c_n]['si']
            ]  # lfp

        for i in lvl:
            spk[i] = [
                         np.array(sp[0][i][chs][oct_cut[0]:oct_cut[1] + 1]),
                         np.array(sp[1][i][chs][oct_cut[0]:oct_cut[1] + 1]),
                         np.array(sp[2][i][chs][oct_cut[0]:oct_cut[1] + 1])
                         ] * pq.ms ** (-1)

            spk[i].units = pq.s ** (-1)
    both = [spk, lfp]
lvp = nnmp.db_lv(lfp)  # SPL dB which actually has data
# print(lvp)

# plot start
s_img = [[] for _ in range(2)]  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(18, 12))

s_axs = s_fig.subplots(2, 3)

title = sets[6][0:3]  # title of plots

for i in range(len(both)):
    data = both[i][lvs[0]]
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(data)):
        nnmp.nnm_plot(
            axes[j], data[j], s_img[i], ccmaps[i], type='octave')
        if j != 0:
            axes[j].axes.yaxis.set_ticklabels([])

    if i != 1:
        for j in axes:
            j.axes.xaxis.set_ticklabels([])

    if i == 0:
        for j in range(len(title)):
            axes[j].set_title(title[j], fontdict={'fontsize': 30})

    # axes[0].text(0, 0, f'{lvs[0]} dB',
    #              horizontalalignment='center',
    #              verticalalignment='center',
    #              rotation='vertical',
    #              transform=axes[0].transAxes,
    #              fontdict={'weight': 'bold', 'size': 30}
    #              )

# unit text
s_axs[0, 0].text(0, 0, 'octaves',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=s_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

s_axs[1, 1].text(0.5, 0, 'time (ms)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=s_axs[1, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 30}
                 )

mx = [
    nnmp.norm_color(s_img[0], 'spk', 0.8),
    nnmp.norm_color(s_img[1], 'lfp', 0.9)
    ]
modes = ['spk', 'lfp']
print(mx)
# colorbar setup
for i in range(2):
    max = mx[i]
    axes = [s_axs[i, 0], s_axs[i, 1], s_axs[i, 2]]
    for j in range(len(axes)):
        cbar = nnmp.colorbar_set(
            s_fig, axes[j], s_img[i][0], modes[i],
            vmax=max[1], vmin=max[0], ori='vertical'
            )

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).ax_dict["<colorbar>"].set_position([0.839191, 0.468928, 0.010599, 0.317978])
plt.figure(0).ax_dict["<colorbar>"].set_position([0.839191, 0.126011, 0.010599, 0.317978])
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
plt.figure(0).axes[0].set_position([0.125000, 0.468928, 0.211985, 0.317978])
plt.figure(0).axes[0].texts[0].set_position([-0.245693, 0.000000])
plt.figure(0).axes[1].set_position([0.374918, 0.468928, 0.211985, 0.317978])
plt.figure(0).axes[2].set_position([0.622753, 0.468928, 0.211985, 0.317978])
plt.figure(0).axes[4].set_position([0.374918, 0.126011, 0.211985, 0.317978])
plt.figure(0).axes[4].texts[0].set_position([0.500000, -0.206382])
plt.figure(0).axes[5].set_position([0.622753, 0.126011, 0.211985, 0.317978])
#% end: automatic generated code from pylustrator
plt.show()
# plt.show()
