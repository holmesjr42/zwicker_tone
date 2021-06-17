import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
from parameters import parameters as pm
import seaborn as sns
import h5py
from matplotlib.colors import ListedColormap
from scipy import stats
import glob
sys.path.pop(1)

'''
this is for doing wilcoxon signed ranksum test on the evoked activity
'''
# sns.set_style("ticks")

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some adjustments for plots: channels you are going to use, wspace, hspace,
# colormap, min and max values for heatmap

# continuous nn
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
val2 = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, \
cb, ccmap = val.values()
hs += 0.05
ccl = val2.values()[-3]  # color for notch borders
# lfp spectrogram colormap
lcmap = val2.values()[-1]
# print(ccl)
condl = 'lfp'
octs = com.octaves  # octave range for plotting
lvl = com.db['lv']  # SPLdB list
g_nf = {}  # dict of frequecny profile for nnm condition
g_nl = {}  # dict of lfp profile for nnm condition
g_sf = {}  # dict of frequency profile for strf condition
g_sl = {}  # dict of lfp profile for strf condition

for i in lvl:
    g_nf[i] = [[] for _ in range(16)]
    g_nl[i] = [[] for _ in range(16)]
    g_sf[i] = [[] for _ in range(16)]
    g_sl[i] = [[] for _ in range(16)]

# dataset
file_input = glob.glob("/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
                "/data/dataset/nnm_spk_lfp_avg/cr*.hdf5")

# file_input = snakemake.input[0]
# getting animal cr number
animal = file_input[0].split('/')[-1].split('_')[0]

# conditions for this script
c_n = 'nnm_3_0_05'
c_s = 'nnm_3_0_05_strf'
# loading data

for files in file_input:
    with h5py.File(files, 'r') as dat:
        datas = dat

        if 'all' in animal:
            if '30' in list(datas['lfp'][c_s].keys()):
                for i in ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf',
                          'lsd']:
                    datas[i][c_s].pop('30')

            else:
                pass
            keeys = ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf', 'lsd']
            if '30' in list(datas['lfp'][c_n].keys()):
                for i in keeys:
                    datas[i][c_n].pop('30')
            else:
                pass

        else:
            pass

            # aranging dataset

        sa = [datas['fpt'][c_n], datas['fpt'][c_s]]  # spk_average (f profile)
        # interval

        la = [datas['fpl'][c_n], datas['fpl'][c_s]]  # lfp_average (f profile)

        for i in lvl:

            if np.any(sa[0][i]) == False:
                continue
            else:
                for j in range(16):
                    g_nf[i][j].append(sa[0][i][j][12])
                    g_nl[i][j].append(la[0][i][j][12])
                    g_sf[i][j].append(sa[1][i][j][12])
                    g_sl[i][j].append(la[1][i][j][12])


col=['red', 'blue', 'cyan', 'black']
g = {}
for k in range(len(lvl)):
    i = lvl[k]
    # g[i] = []
    g[i] = []
    for j in range(16):
        a = stats.wilcoxon(g_nf[i][j], g_sf[i][j])
        g[i].append(a[1])
        print(np.shape(g[i]))
    plt.scatter(np.arange(16), g[i], c=col[k])
plt.axhline(y=0.05)
plt.show()

# with open(snakemake.output[0], 'wb') as datas:
# with open('/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data'
#           '/dataset/wilcoxon/nnm_3_0_05_wilcoxon_l.pk', 'wb') as datas:
#     pickle.dump(g, datas, protocol=pickle.HIGHEST_PROTOCOL)
# print(g['40'])
#     print(np.shape(g))
#     plt.scatter(np.arange(16), np.transpose(g), c=col[k])
# plt.axhline(y=0.05)
# plt.show()

        # print('lvl', i, 'ch:',j , stats.wilcoxon(g_nf[i][j], g_sf[i][j]))
# for i in lvl:
#     for j in range(len(ch)):
#         chs = ch[i]
#         tspn = g_n[i][0][ch]
#         tspc = g_s[i][0][ch]
