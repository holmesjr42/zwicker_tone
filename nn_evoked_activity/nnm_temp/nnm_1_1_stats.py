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
g_nf0 = {}  # dict of frequecny profile for nnm condition
g_nl0 = {}  # dict of lfp profile for nnm condition
g_wf0 = {}  # dict of frequecny profile for nnm condition
g_wl0 = {}  # dict of lfp profile for nnm condition
g_nf1 = {}  # dict of frequecny profile for nnm condition
g_nl1 = {}  # dict of lfp profile for nnm condition
g_wf1 = {}  # dict of frequecny profile for nnm condition
g_wl1 = {}  # dict of lfp profile for nnm condition
g_sfw = {}  # dict of frequency profile for strf condition
g_slw = {}  # dict of lfp profile for strf condition
g_sfn = {}  # dict of frequency profile for strf condition
g_sln = {}  # dict of lfp profile for strf condition

for i in lvl:
    g_nf0[i] = [[] for _ in range(16)]
    g_nl0[i] = [[] for _ in range(16)]
    g_wf0[i] = [[] for _ in range(16)]
    g_wl0[i] = [[] for _ in range(16)]
    g_nf1[i] = [[] for _ in range(16)]
    g_nl1[i] = [[] for _ in range(16)]
    g_wf1[i] = [[] for _ in range(16)]
    g_wl1[i] = [[] for _ in range(16)]
    g_sfn[i] = [[] for _ in range(16)]
    g_sln[i] = [[] for _ in range(16)]
    g_sfw[i] = [[] for _ in range(16)]
    g_slw[i] = [[] for _ in range(16)]

# dataset
file_input = glob.glob(
    "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
    "/data/dataset/nnm_spk_lfp_avg/cr*.hdf5")

# file_input = snakemake.input[0]
# getting animal cr number
animal = file_input[0].split('/')[-1].split('_')[0]

# conditions for this script
c_n = 'nnm_1_1'
c_w = 'nnm_wn_1_1'
c_s = 'nnm_1_1_strf'
# loading data

for files in file_input:
    animal = files.split('/')[-1].split('_')[0]
    if not animal in ['cr31', 'cr33', 'cr50', 'cr79', 'cr90', 'all']:
        continue
    else:
        pass

        with h5py.File(files, 'r') as dat:
            datas = dat

            if 'all' in animal:
                if '30' in list(datas['lfp'][c_s].keys()):
                    for i in ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf',
                              'lsd']:
                        datas[i][c_s].pop('30')

                else:
                    pass
                keeys = ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf',
                         'lsd']
                if '30' in list(datas['lfp'][c_n].keys()):
                    for i in keeys:
                        datas[i][c_n].pop('30')
                else:
                    pass

            else:
                pass

                # aranging dataset

            sa = [datas['fpt'][c_n], datas['fpt'][c_s], datas['fpt'][c_w]]  #
            # spk_average (f
            # profile)
            # interval

            la = [datas['fpl'][c_n], datas['fpl'][c_s], datas['fpl'][c_w]]  #
            # lfp_average (f
            # profile)
            print(animal)

            for i in lvl:
                if not np.any(sa[0]['nn'][i]):
                    continue
                else:
                    for j in range(16):
                        g_sfn[i][j].append(sa[1][i][j][12])
                        g_sln[i][j].append(la[1][i][j][12])
                        g_nf0[i][j].append(sa[0]['si'][i][j][12])
                        g_nl0[i][j].append(la[0]['si'][i][j][12])
                        g_nf1[i][j].append(sa[0]['nn'][i][j][12])
                        g_nl1[i][j].append(la[0]['nn'][i][j][12])

                if not np.any(sa[2]['nn'][i]):
                    continue
                else:
                    for j in range(16):
                        # print(la[2]['si'][i][j][12])
                        g_sfw[i][j].append(sa[1][i][j][12])
                        g_slw[i][j].append(la[1][i][j][12])
                        g_wf1[i][j].append(sa[2]['nn'][i][j][12])
                        g_wl1[i][j].append(la[2]['nn'][i][j][12])
                        g_wf0[i][j].append(sa[2]['si'][i][j][12])
                        g_wl0[i][j].append(la[2]['si'][i][j][12])

    for i in list(g_sfw.keys()):
        for j in range(16):
            print('NN-OFF fp', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sfn[i][j],
                                                                  g_nf0[i][j]))

            print('NN-OFF lf', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sln[i][j],
                                                                  g_nl0[i][j]))

            print('NN-ON fp', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sfn[i][j],
                                                                 g_nf1[i][j]))

            print('NN-ON lf', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sln[i][j],
                                                                 g_nl1[i][j]))

    for i in list(g_sfw.keys()):
        for j in range(16):
            print('WN-OFF fp', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sfw[i][j],
                                                                  g_wf0[i][j]))
            print('WN-OFF lf', 'lvl', i, 'ch:', j, stats.wilcoxon(g_slw[i][j],
                                                                  g_wl0[i][j]))
            print('WN-ON fp', 'lvl', i, 'ch:', j, stats.wilcoxon(g_sfw[i][j],
                                                                 g_wf1[i][j]))
            print('WN-ON lf', 'lvl', i, 'ch:', j, stats.wilcoxon(g_slw[i][j],
                                                                 g_wl1[i][j]))
