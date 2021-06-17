import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
from parameters import parameters as pm
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
find = [sets[3][1], sets[3][3]]

f_name = [sets[5][0], sets[5][2]]
# temp

#  loading data

dataf = {
    'data': [], 'layer': [], 'frequecny': [],
    'statistic': [], 'pvalue': []
    }
c_list = list(dataf.keys())
d_list = ['dfps', 'dfpl']
t_list = ['spk', 'lfp']

with h5py.File(file_input, 'r') as dat:
    fps = dat['fps']
    fpl = dat['fpl']
    base = dat['base']
    ds = [fps, fpl]
    # fps wilcoxon: fps, fpl
    for d in range(len(ds)):
        dats = ds[d]
        d_n = d_list[d]
        for ly in l_list:
            for f in range(len(find)):
                fried = {}
                for lv in lvl:
                    fried[lv] = []
                    temp = nt.diff(
                        ds[d], ly, lv, cn, cs, find[f],
                        bdata=base, types=t_list[d]
                        )
                    fried[lv] = np.append(fried[lv], temp[3])

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

                temp = [d_n, ly, find[f], test[0], test[1]]
                for j in range(len(c_list)):
                    dataf[c_list[j]].append(temp[j])

            friedc = {}

            for lv in lvl:
                friedc[lv] = []
                tempc = nt.diff(
                    ds[d], ly, lv, cn, cs, find[0],
                    bdata=base, types=t_list[d], fqtype='center'
                    )
                friedc[lv] = np.append(friedc[lv], tempc[3])

            testc = stats.friedmanchisquare(
                np.concatenate([friedc[lvl[0]][2:6],
                                friedc[lvl[0]][7:]]),
                fried[lvl[1]],
                np.concatenate([friedc[lvl[2]][2:6],
                                friedc[lvl[2]][7:]]
                               ),
                np.concatenate([friedc[lvl[3]][1:5],
                                friedc[lvl[3]][6:]]
                               )
                )
            temp = [d_n, ly, 12, test[0], test[1]]

            for j in range(len(c_list)):
                dataf[c_list[j]].append(temp[j])


    df = pd.DataFrame(dataf, columns=c_list)
    # print(df)
    df.to_csv(r'fp_diff_stat.csv')
