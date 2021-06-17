import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import json
import matplotlib.pyplot as plt
from parameters import parameters as pm
import h5py
from tools import nn_tool as nt
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
val = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cnon = 'nnm_3_1_on'
cnoff = 'nnm_3_1_off'
cwoff = 'nnm_wn_3_1_off'
cc = 'nnm_3_1_strf'
cw = 'nnm_wn_3_1_strf'

layer_name = ['Supragranular\nLayer', 'Granular\nLayer',
              'Infragranular\nLayer']

l_list = ['supr', 'gran', 'infr']


# index of low edge, center, high edge, 0.5 oct above/below  of notch gap
mid = 12
lef = 4
hef = 20
hbe = 8
hab = 16
finx = [lef, mid, hef]
paradigm = ['NN-ON', 'NN-OFF', 'WN-OFF']
l_style = ['dashdot', '-', 'dashed']
rationon = {}
rationof = {}
ratiowof = {}
err2 = {}
err7 = {}
# load file
with h5py.File(file_input, 'r') as dat:
    ind = mid
    sk = dat['fps']  #
    for layer in l_list:
        rationon[layer] = []
        rationof[layer] = []
        ratiowof[layer] = []

        temp_rnon = []  # temporary list for nn-on ratio
        temp_rnoff = []  # temporary list for nn-off ratio
        temp_rwoff = []  # temporary list for wn-on ratio

        for lv in lvl:
            teempnon = nt.diff(sk, layer, lv, cnon, cc, ind, type='lfp')
            teempnof = nt.diff(sk, layer, lv, cnoff, cc, ind, type='lfp')
            teempwof = nt.diff(sk, layer, lv, cwoff, cw, ind, type='lfp')

            temp_rnon.append(teempnon[3])

            temp_rnoff.append(teempnof[3])

            temp_rwoff.append(teempwof[3])

        rationon[layer].append(temp_rnon)
        rationof[layer].append(temp_rnoff)
        ratiowof[layer].append(temp_rwoff)

    stat_r = [rationon, rationof, ratiowof]

    # stat
    for s in range(len(stat_r)):
        for ly in l_list:
            s2 = stat_r[s][ly][0]
            name = paradigm[s]
            sts = stats.friedmanchisquare(s2[0], s2[1], s2[2], s2[3])

            print(name, ly, sts)
