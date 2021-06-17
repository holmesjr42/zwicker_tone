import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
import numpy as np
from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
# for bootstrap nonparametric
import pandas as pd
from scipy import stats

'''
This is a script to produce p value data set for nnm_3_0: both frequency 
profile and difference ratio.
'''
# file I'm going to use
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some features for name/condition to retrieve data from the dataset
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

# stimulus conditions for this script
cn = sets[7][0]
cs = sets[8][0]
cond = ['control', 'nn']
# layer name list and dic key list of layers
layer_name = sets[0]
l_list = sets[2]

# indice list of low edge, center, high edge, 0.5 oct above/below  of notch gap
find = [sets[3][1], sets[3][-2]]
f_name = sets[5]
# temp

#  loading data

dataf = {
    'data': [], 'layer': [], 'level': [], 'frequecny': [], 'pvalue': []
    }
c_list = list(dataf.keys())
d_list = ['fps', 'fpl', 'dfps', 'dfpl']
t_list = ['spk', 'lfp', 'spk', 'lfp']

with h5py.File(file_input, 'r') as dat:
    fps = dat['fps']
    fpl = dat['fpl']
    base = dat['base']
    ds = [fps, fpl, fps, fpl]
    # fps wilcoxon: fps, fpl
    for d in range(len(ds)):
        dats = ds[d]
        d_n = d_list[d]
        for ly in l_list:
            for f in range(len(find) - 1):
                fried = {}
                for lv in lvl:
                    fried[lv] = []
                    dn = dats[cn][ly][lv]
                    dc = dats[cs][ly][lv]
                    fm = []
                    for k in range(len(dn)):
                        fm.append(nt.freq_find(dn[k], find, type=t_list[d]))

                    if d_n == d_list[0] or d_n == d_list[1]:
                        test = nt.fp_wilcoxon([dc, dn], fm)
                        temp = [d_n, ly, lv, test[0], test[1]]
                        for j in range(len(c_list)):
                            dataf[c_list[j]].append(temp[j])
                    elif d_n == d_list[2] or d_n == d_list[3]:
                        temp = nt.diff(
                            ds[d], ly, lv, cn, cs,
                            bdata=base, types=t_list[d], fqtype='center'
                            )
                        fried[lv] = np.append(fried[lv], temp[3])
                if d_n == d_list[2] or d_n == d_list[3]:
                    test = stats.friedmanchisquare(
                        np.concatenate([fried[lvl[0]][2:6],
                                        fried[lvl[0]][7:]]),
                        fried[lvl[1]],
                        np.concatenate([fried[lvl[2]][2:6],
                                        fried[lvl[2]][7:]]
                                       ),
                        np.concatenate([fried[lvl[3]][1:5],
                                        fried[lvl[3]][6:]]
                                       )
                        )
                    temp = [d_n, ly, '-', test[0], test[1]]
                    for j in range(len(c_list)):
                        dataf[c_list[j]].append(temp[j])
    df = pd.DataFrame(dataf, columns=c_list)
    # print(df)
    df.to_csv(r'fp_stat2.csv')
