import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nn_tool as nt
from tools import nnm_plot as nnmp
from parameter import parameters as pm
import pylustrator
from parameter import parameters as pm
import matplotlib.pyplot as plt
import quantities as pq

pylustrator.start()
sys.path.pop(1)

'''
This is to create offset response table.
'''

'''
setup
'''

val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
val2 = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1)
ccmap = [val2.values()[-1], val.values()[-1], 'rainbow_r']

dbs, db, dcmap, names, legendl, ch_l, l_list, layer_name = val.nn11_plot()
legends = legendl[1]
nn = names[0]
wn = names[1]
db_n = 1
ont = [0, 251]
oft = [1000, 1251]
bt = [1300, 1701]
blt = [nt.lfp_index(bt[0]), nt.lfp_index(bt[1])]

file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
       "/dataset/nn_mean/all_nn_mean.hdf5"

with h5py.File(file, 'r') as dat:
    l_n = dat['lfp']['mean']['nn_1_1'][db_n]
    l_w = dat['lfp']['mean']['nn_wn_1_1'][db_n]

    s_n = dat['spk']['s_psth']['nn_1_1'][db_n]
    s_w = dat['spk']['s_psth']['nn_wn_1_1'][db_n]

#     c_n = nt.nn_csd(l_n)
#     c_w = nt.nn_csd(l_w)
#
#     st = dat['spk']['time']['nn_1_1'][db_n]
#     lt = np.linspace(
#         0, 2101, num=len(l_n[0]), endpoint=True
#         )
#
#
#     ln = nt.noise_sep(l_n, ont, oft, 'lfp')
#     lw = nt.noise_sep(l_w, ont, oft, 'lfp')
#     sn = nt.noise_sep(s_n, ont, oft, 'spk')
#     sw = nt.noise_sep(s_w, ont, oft, 'spk')
#     cn = nt.noise_sep(c_n, ont, oft, 'lfp')  # this is csd data
#     cw = nt.noise_sep(c_w, ont, oft, 'lfp')  # this is csd data
#
#     data = [
#         [sn[0], sw[0], sn[1], sw[1]],
#         [ln[0], lw[0], ln[1], lw[1]],
#         [cn[0], cw[0], cn[1], cw[1]]
#         ]
#
#     t = [
#         np.arange(len(sn[0][0])),
#         np.linspace(0, 250, num=len(ln[0][0]), endpoint=True),
#         np.linspace(0, 250, num=len(ln[0][0]), endpoint=True)
#         ]
#
# # plot setup
#
# h_fig = plt.figure(0, figsize=(16, 9))
#
# h_axs = h_fig.subplots(3, 4)
# title = ['Noise On', 'Noise Off']
# d_type = ['spk', 'lfp', 'csd']
# n_cond = ['NN-ON', 'WN-ON', 'NN-OFF', 'WN-OFF']
#
# c_mnx = [[] for _ in range(6)]
# c_ind = [0, 2, 4]
# for i in range(len(d_type)):
#     d_img = []
#     for j in range(len(n_cond)):
#         img = h_axs[i, j].imshow(
#             data[i][j], cmap=ccmap[i], aspect=len(t[i]) / 1500,
#             extent=[t[i][0], t[i][-1], 1500, 0], interpolation='gaussian'
#             )
#         h_axs[i, j].label_outer()
#         d_img.append(img)
#
#
#     mnn, mxn = nnmp.norm_color(d_img[0:2], d_type[i], 0.8)
#     mnf, mxf = nnmp.norm_color(d_img[2:4], d_type[i], 0.8)
#
#     mn = [mnn, mnn, mnf, mnf]
#     mx = [mxn, mxn, mxf, mxf]
#
#     for j in range(len(n_cond)):
#         nnmp.colorbar_set(
#             h_fig, h_axs[i, j], d_img[j], d_type[i], vmax=mx[j], vmin=mn[j]
#             )
#
# #% start: automatic generated code from pylustrator
# plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
# import matplotlib as mpl
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.840728, 0.110126, 0.006745, 0.239831])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.437617, 0.706861, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.440805, 0.435097, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.437617, 0.163332, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.833832, 0.163332, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.833832, 0.435097, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_position([0.833832, 0.706861, 0.003370, 0.119807])
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).ax_dict["<colorbar>"].set_visible(False)
# plt.figure(0).axes[1].set_position([0.294477, 0.653529, 0.126882, 0.226471])
# plt.figure(0).axes[2].set_position([0.556650, 0.653529, 0.126882, 0.226471])
# plt.figure(0).axes[3].set_position([0.698824, 0.653529, 0.126882, 0.226471])
# plt.figure(0).axes[4].set_position([0.154321, 0.384025, 0.126969, 0.241032])
# plt.figure(0).axes[5].set_position([0.294477, 0.384458, 0.126969, 0.240168])
# plt.figure(0).axes[6].set_position([0.556650, 0.384294, 0.126969, 0.240168])
# plt.figure(0).axes[7].set_position([0.698732, 0.384458, 0.126882, 0.240005])
# plt.figure(0).axes[8].set_position([0.154321, 0.110000, 0.127363, 0.240915])
# plt.figure(0).axes[9].set_position([0.294477, 0.109874, 0.126969, 0.240168])
# plt.figure(0).axes[10].set_position([0.556650, 0.110126, 0.126835, 0.239916])
# plt.figure(0).axes[11].set_position([0.698824, 0.110126, 0.126790, 0.239831])
# #% end: automatic generated code from pylustrator
# plt.show()
#
#
