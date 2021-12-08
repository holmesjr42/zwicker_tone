import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import matplotlib.image as mpimg
from parameters import parameters as pm
import h5py
from matplotlib.colors import ListedColormap
from tools import nnm_plot as nnmp
from tools import spike_tools as spt
import pylustrator
from scipy import stats

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
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_1_1.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cnon = 'nnm_1_1_on'
cnoff = 'nnm_1_1_off'
cwoff = 'nnm_wn_1_1_off'
cc = 'nnm_1_1_strf'
cw = 'nnm_wn_1_1_strf'

layer_name = ['Supragranular\nLayer', 'Granular\nLayer',
              'Infragranular\nLayer']

l_list = ['supr', 'gran', 'infr']

spk = {}  # dict for spk data regarding SPLdB

# index of low edge, center, high edge, 0.5 oct above/below  of notch gap
mid = 12
lef = 4
hef = 20
hbe = 8
hab = 16
finx = [lef, mid, hef]
paradigm = ['NN-ON', 'NN-OFF', 'WN-OFF']
l_style = ['dashdot', '-', 'dashed']
ratio = {}
err2 = {}
err7 = {}
# load file
with h5py.File(file_input, 'r') as dat:
    sk = dat['fps']  #
    for layer in l_list:
        meann = []
        errl = []
        errh = []

        for lv in lvl:
            tempnon = sk[cnon][layer][lv]  # temporary list for nn-on data
            tempnoff = sk[cnoff][layer][lv]  # temporary list for nn-off data
            tempwoff = sk[cwoff][layer][lv]  # temporary list for wn-off data
            tempc = sk[cc][layer][lv]  # dissertation list for control data
            tempwc = sk[cw][layer][lv]
            temp_rnon = []  # temporary list for nn-on ratio
            temp_rnoff = []  # temporary list for nn-off ratio
            temp_rwoff = []  # temporary list for wn-on ratio

            # nn-on, nn-off
            for ani in range(len(tempnon)):
                temp_rnon.append((tempnon[ani] - tempc[ani]) / tempc[ani])
                temp_rnoff.append((tempnoff[ani] - tempc[ani]) / tempc[ani])

            # wn-off

            for ani in range(len(tempwoff)):
                temp_rwoff.append((tempwoff[ani] - tempwc[ani]) / tempwc[ani])

            # median
            temp_mnon = np.median(np.array(temp_rnon), axis=0)
            temp_mnoff = np.median(np.array(temp_rnoff), axis=0)
            temp_mwoff = np.median(np.array(temp_rwoff), axis=0)

            meann.append(
                [temp_mnon[finx[1]], temp_mnoff[finx[1]], temp_mwoff[finx[1]]]
                )

            # 25, 75 percentile
            temp_enon2 = np.percentile(
                np.array(temp_rnon), 25, axis=0)[finx[1]]
            # for nn-on quartile, 0.25
            temp_enon7 = np.percentile(
                np.array(temp_rnon), 75, axis=0)[finx[1]]
            # for nn-on qaurtile, 0.75

            temp_enoff2 = np.percentile(
                np.array(temp_rnoff), 25, axis=0)[finx[1]]
            # for nn-off quartile, 0.25
            temp_enoff7 = np.percentile(
                np.array(temp_rnoff), 75, axis=0)[finx[1]]
            # for nn-off qaurtile, 0.75

            temp_ewoff2 = np.percentile(
                np.array(temp_rwoff), 25, axis=0)[finx[1]]
            # for nn-off quartile, 0.25
            temp_ewoff7 = np.percentile(
                np.array(temp_rwoff), 75, axis=0)[finx[1]]
            # for nn-off qaurtile, 0.75

            errl.append([temp_enon2, temp_enoff2, temp_ewoff2])
            errh.append([temp_enon7, temp_enoff7, temp_ewoff7])

        ratio[layer] = np.transpose(meann)
        err2[layer] = np.transpose(errl)
        err7[layer] = np.transpose(errh)

# plot start
s_img = []  # for normalizing heatmap

s_fig = plt.figure(0, figsize=(16, 9))

s_axs = s_fig.subplots(1, 3)
xs = np.arange(4)

# ticks
for j in range(len(l_list)):
    ls = l_list[j]
    for i in range(len(paradigm)):
        ftext = paradigm[i]
        s_axs[j].plot(xs, ratio[ls][i],
                      color=dcmap[i],
                      label=paradigm[i],
                      lw=3,
                      linestyle=l_style[i], zorder=2)

        s_axs[j].fill_between(xs,
                              err2[ls][i],
                              err7[ls][i],
                              color=dcmap[i], zorder=2, alpha=0.2)

        s_axs[j].set_yticks(np.arange(-0.4, 1.3, 0.2))
        s_axs[j].set_ylim(-0.6, 1.4)

for i in range(len(layer_name)):
    s_axs[i].text(0.5, 0, layer_name[i],
                  horizontalalignment='center',
                  verticalalignment='center',
                  # rotation='vertical',
                  transform=s_axs[i].transAxes,
                  fontdict={'weight': 'bold', 'size': 25}
                  )

    s_axs[i].set_xticks(np.arange(4))
    s_axs[i].set_xticklabels(['70', '60', '50', '40'])
    s_axs[i].tick_params(axis='both', which='major', labelsize=15)
    s_axs[i].axhline(y=0, c='k', lw=1.5, alpha=0.5, linestyle='dotted',
                     zorder=1)

s_axs[2].legend(prop={'size': 10},
                loc='upper right',
                bbox_to_anchor=(1, 1))

s_axs[0].text(0, 0.5, 'Ratio of changes\nto control',
              horizontalalignment='center',
              verticalalignment='center',
              rotation='vertical',
              transform=s_axs[0].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )

s_axs[1].text(0.5, 0, 'dB SPL',
              horizontalalignment='center',
              verticalalignment='center',
              # rotation='vertical',
              transform=s_axs[1].transAxes,
              fontdict={'weight': 'bold', 'size': 25}
              )


#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].set_position([0.125000, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[0].texts[0].set_position([0.500000, -0.522942])
plt.figure(0).axes[0].texts[1].set_position([-0.271555, 0.500000])
plt.figure(0).axes[1].set_position([0.398622, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[1].texts[0].set_position([0.500000, -0.522942])
plt.figure(0).axes[1].texts[1].set_position([0.500000, -0.233795])
plt.figure(0).axes[2].set_position([0.671998, 0.383202, 0.227854, 0.384952])
plt.figure(0).axes[2].texts[0].set_position([0.500340, -0.522942])
#% end: automatic generated code from pylustrator
plt.show()