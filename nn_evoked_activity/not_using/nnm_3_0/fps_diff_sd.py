import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import json
from parameter import parameters as pm
import glob
import h5py
from scipy import stats

sys.path.pop(1)

'''
this is to get the SD and maybe average across the animals
'''
# sns.set_style("ticks")

# import features
com = pm.Commonfeat

lvl = com.db['lv']  # SPLdB list

# dict for sd
cfh = {}  # control, high frequency
cfc = {}  # control, center frequency
cfl = {}  # control, low frequency

nfh = {}  # notch, high frequency
nfc = {}  # notch, center frequency
nfl = {}  # notch, low frequency

d_lf = {}  # dict of sd difference for low freqeucny nnm condition
d_cf = {}  # dict of sd difference for center frequency nnm condition
d_hf = {}  # dict of sd difference for high frequency  condition

for i in lvl:

    cfl[i] = [[] for _ in range(3)]
    cfc[i] = [[] for _ in range(3)]
    cfh[i] = [[] for _ in range(3)]
    nfl[i] = [[] for _ in range(3)]
    nfc[i] = [[] for _ in range(3)]
    nfh[i] = [[] for _ in range(3)]

    d_lf[i] = [[] for _ in range(3)]
    d_cf[i] = [[] for _ in range(3)]
    d_hf[i] = [[] for _ in range(3)]

# dataset
file_input = glob.glob(
    "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
    "/data/dataset/nnm_spk_lfp_avg/cr*.hdf5")

# conditions for this script
c_n = 'nnm_3_0'
c_s = 'nnm_3_0_strf'

# channels for layer: supra, granular, infra
ch_l = [[0, 6], [6, 9], [9, 16]]
# loading data

for files in file_input:
    animal = files.split('/')[-1].split('_')[0]
    if animal in ['cr92', 'cr93']:
        continue
    else:
        with h5py.File(files, 'r') as dat:
            datas = dat

            # aranging dataset

            sa = [datas['fpt'][c_s], datas['fpt'][c_n]]  # spk_average (f
            # profile)

            for i in lvl:

                if np.any(sa[0][i]) == False:
                    continue
                else:
                    for j in range(len(ch_l)):
                        c = ch_l[j]
                        ccf = np.mean(sa[0][i][c[0]:c[1]], axis=0)[12]
                        ncf = np.mean(sa[1][i][c[0]:c[1]], axis=0)[12]

                        clf = np.mean(sa[0][i][c[0]:c[1]], axis=0)[4]
                        nlf = np.mean(sa[1][i][c[0]:c[1]], axis=0)[4]

                        chf = np.mean(sa[0][i][c[0]:c[1]], axis=0)[20]
                        nhf = np.mean(sa[1][i][c[0]:c[1]], axis=0)[20]

                        cfl[i][j].append(clf)
                        cfc[i][j].append(ccf)
                        cfh[i][j].append(chf)

                        nfl[i][j].append(nlf)
                        nfc[i][j].append(ncf)
                        nfh[i][j].append(nhf)

for i in lvl:
    for k in range(len(ch_l)):
        c_lf = np.std(cfl[i][k], axis=0)
        c_cf = np.std(cfc[i][k], axis=0)
        c_hf = np.std(cfh[i][k], axis=0)
        n_lf = np.std(nfl[i][k], axis=0)
        n_cf = np.std(nfc[i][k], axis=0)
        n_hf = np.std(nfh[i][k], axis=0)

        # c_lf = stats.sem(cfl[i][k], axis=0)
        # c_cf = stats.sem(cfc[i][k], axis=0)
        # c_hf = stats.sem(cfh[i][k], axis=0)
        # n_lf = stats.sem(nfl[i][k], axis=0)
        # n_cf = stats.sem(nfc[i][k], axis=0)
        # n_hf = stats.sem(nfh[i][k], axis=0)


        d_lf[i][k] = (n_lf - c_lf) / c_lf
        d_cf[i][k] = (n_cf - c_cf) / c_cf
        d_hf[i][k] = (n_hf - c_hf) / c_hf

g = {
    's_lf': d_lf, 's_cf': d_cf, 's_hf': d_hf,
     }

with open('/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data'
          '/dataset/nnm_spk_lfp_avg/nnm_3_0_layer_se.json', 'w') as datas:
    json.dump(g, datas)
