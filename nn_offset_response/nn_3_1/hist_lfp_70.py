import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))

import numpy as np
import h5py
from tools import nn_tool as nt
from parameters import parameters as pm
import matplotlib.pyplot as plt
import pickle
import quantities as pq
import pylustrator
from tools import nn_tool as nt

pylustrator.start()
sys.path.pop(1)

'''
This is for a single animal data
plots psth and averaged raw lfp in the same figure
'''
# exemplary animals
d_lfp = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
        "/dataset/nn_lfp_avg/cr95_201117_nn_lfp_a.pk"
d_spk = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
        "/dataset/tsp/cr95_201117_tsp.hdf5"


# file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data\
#         /dataset/nn_layer/nn_layer_nn_3_1.hdf5"
'''
setup
'''
val = pm.Setup(cond2='tsp')

dbs, db, dcmap, names, legendl, ch_l, l_list, layer_name = val.nn31_plot()
legends = legendl[1]
nn = names[0]
wn = names[1]
dbl = dbs[0]

# spk
nrastor = {}
npsth = {}
nsmooth = {}
ntime = {}

'''
data retrieve
'''
g_sf = {}  # storing spk data exp
g_lf = {}  # storing lfp data exp
g_cf = {}  # confidence interval for lfp
# lfp/spk partition
for g in [g_lf, g_sf, g_cf]:
    for d in db:
        s = dbs[d]
        g[s] = {}
        for n in names:
            g[s][n] = {}
            for l in l_list:
                g[s][n][l] = []

# lfp
for n in names:
    for lv in db:
        d = dbs[lv]
        # lfp
        with open(d_lfp, 'rb') as datas:
            dat = pickle.load(datas)
            la = dat['la']  # lfp session averaged
            lc = dat['lc']  # lfp confidence interval
        # onset/offset points and change the unit
        la_n = la[n][d] * pq.microvolt
        la_n.units = pq.mV

        lc_n = lc[n][d] * pq.microvolt
        lc_n.units = pq.mV

        for i in range(len(ch_l)):
            g_lf[d][n][l_list[i]].append(la_n[ch_l[i]])
            g_lf[d][n][l_list[i]] = np.concatenate(g_lf[d][n][l_list[i]])

            g_cf[d][n][l_list[i]].append(lc_n[ch_l[i]])
            g_cf[d][n][l_list[i]] = np.concatenate(g_cf[d][n][l_list[i]])

# spike
with h5py.File(d_spk, 'r') as h_5:
    for n in names:
        for lv in db:
            d = dbs[lv]
            mua = h_5[n][lv]
            nn = nt.index_spike(mua)
            nrastor[n], npsth[n], nsmooth[n], ntime[n] = nt.psth(nn, n)

            ns = nsmooth[n] * pq.ms ** (-1)
            ns.units = pq.s ** (-1)

            for i in range(len(ch_l)):
                g_sf[d][n][l_list[i]].append(ns[ch_l[i]])
                g_sf[d][n][l_list[i]] = np.concatenate(g_sf[d][n][l_list[i]])

n_fig = plt.figure(0, figsize=(10, 9))
n_axs = n_fig.subplots(3, 2)

# spk
for n in range(len(names)):
    for layer in range(len(l_list)):
        axs = n_axs[layer, 0]
        s_hist = g_sf[dbl][names[n]][l_list[layer]]
        s_hist[2800:2811] = np.nan
        times = np.arange(len(s_hist)) / 1000
        axs.axvspan(2.8, 3.0, alpha=0.3, color='#bccbe3')
        axs.plot(
            times[::20], s_hist[::20], color=dcmap[n],
            alpha=1, linewidth=1.7, label=legends[n]
            )
        axs.set_xlim([2.8, 4.010])
        axs.set_xticks(np.arange(2.9, 4, 0.2), minor=True)
        axs.set_ylim([0, 160])
        axs.set_yticks(np.arange(0, 160, 50))
        # axs.tick_params(axis='both', which='major', labelsize=10)

n_axs[0, 0].legend(prop={'size': 9},
                   loc='upper right',
                   bbox_to_anchor=(1, 1))

n_axs[0, 0].text(0.5, 1.1, 'MUA',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=n_axs[0, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 20}
                 )

n_axs[1, 0].text(-0.2, 0.5, 'Firing rate (spk / s)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=n_axs[1, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 15}
                 )

n_axs[2, 0].text(0.5, -0.3, 'Time (s)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=n_axs[2, 0].transAxes,
                 fontdict={'weight': 'bold', 'size': 15}
                 )

# lfp

ylims = [[-0.13, 0.12], [-0.25, 0.16], [-0.2, 0.13]]  # ylim for each layer

# time index
ti = nt.lfp_index(2800)
tf = nt.lfp_index(4000)
times = np.linspace(
    2800, 4000,
    num=len(g_lf[dbl][names[0]][l_list[0]][ti:tf]),
    endpoint=False) / 1000

for n in range(len(names)):
    for layer in range(len(l_list)):
        axl = n_axs[layer, 1]
        lfp_p = g_lf[dbl][names[n]][l_list[layer]][ti:tf]
        lfp_c = g_cf[dbl][names[n]][l_list[layer]][ti:tf]
        lfp_c = np.transpose(lfp_c)

        # just to make borderlines
        # lfp_p[2800:2811] = np.nan
        # lfp_p[4000:4010] = np.nan

        axl.axvspan(2.8, 3.0, alpha=0.3, color='#bccbe3')
        axl.plot(
            times, lfp_p, color=dcmap[n],
            alpha=1, linewidth=1.5, label=legends[n]
            )

        axl.fill_between(
            times,
            lfp_c[0],
            lfp_c[1],
            color=dcmap[n], alpha=0.2
            )

        axl.set_xlim([2.8, 4.010])
        axl.set_xticks(np.arange(2.9, 4, 0.2), minor=True)
        axl.set_yticks(np.arange(-0.2, 0.2, 0.1))
        axl.set_yticks([-0.15, -0.05, 0.05], minor=True)
        axl.set_ylim(ylims[layer])


n_axs[0, 1].text(0.5, 1.1, 'LFP',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=n_axs[0, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 20}
                 )

n_axs[1, 1].text(-0.2, 0.5, 'Amplitude (mV))',
                 horizontalalignment='center',
                 verticalalignment='center',
                 rotation='vertical',
                 transform=n_axs[1, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 15}
                 )

n_axs[2, 1].text(0.5, -0.3, 'Time (s)',
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=n_axs[2, 1].transAxes,
                 fontdict={'weight': 'bold', 'size': 15}
                 )

# % start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl

plt.figure(0).axes[0].set_position([0.125000, 0.653529, 0.293273, 0.226471])
plt.figure(0).axes[1].set_position([0.606727, 0.653529, 0.293273, 0.226471])
plt.figure(0).axes[2].set_position([0.125000, 0.381765, 0.293273, 0.226471])
plt.figure(0).axes[2].texts[0].set_position([-0.251147, 0.500000])
plt.figure(0).axes[3].set_position([0.606727, 0.381765, 0.293273, 0.226471])
plt.figure(0).axes[3].texts[0].set_position([-0.251147, 0.500000])
plt.figure(0).axes[4].set_position([0.125000, 0.110000, 0.293273, 0.226471])
plt.figure(0).axes[5].set_position([0.606727, 0.110000, 0.293273, 0.226471])
# % end: automatic generated code from pylustrator
plt.show()
