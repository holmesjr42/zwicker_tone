import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
import pandas as pd

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
sets = val.extra_setup()
lvl = com.db['lv']  # SPLdB list

file_input = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5',
              '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_wn_3_1.hdf5'
              ]
# file_input = snakemake.input[0]

# stimulus conditions for this script
# nn condition: control, nn-on, nn-off; wn condition: control, nn-on, wn-off
conds = [
    [sets[-2][0], sets[-5][0], sets[-4][0]],
    [sets[-1][0], sets[-5][0], sets[-3][0]]
    ]

# coordination of cond sublist and paired test execution
k_list = [[1, 2], [2]]

# layer list
l_list = sets[2]

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]


# data frame
dataf = {
    'data': [], 'cond': [], 'layer': [], 'level': [],
    'frequecny': [], 'pvalue': [], 'stat': []
    }
c_list = list(dataf.keys())
dats = ['fps', 'fpl']
d_type = ['spk', 'lfp']

# load file
for f in range(len(file_input)):
    file = file_input[f]
    cn = conds[f]
    ks = k_list[f]

    with h5py.File(file, 'r') as dat:
        for t in range(len(dats)):
            dt1 = dats[t]
            dt2 = d_type[t]
            ds = [
                dat[dt1][cn[0]], dat[dt1][cn[1]], dat[dt1][cn[2]]
                  ]

            for l in range(len(l_list)):
                ly = l_list[l]

                for lv in lvl:
                    # list of the max/min spk/lfp frequency in nn band
                    fm = []
                    dt = ds[1][ly][lv]
                    for a in range(len(dt)):
                        fm.append(nt.freq_find(dt[a], find, type=dt2))

                    d_test = [
                        ds[0][ly][lv], ds[1][ly][lv], ds[2][ly][lv]
                        ]

                    for k in ks:

                        test = nt.fp_wilcoxon([d_test[0], d_test[k]], fm)
                        temp = [dt2, cn[k], ly, lv, 'band_max', test[1],
                                test[2]]
                        for j in range(len(c_list)):
                            dataf[c_list[j]].append(temp[j])
df = pd.DataFrame(dataf, columns=c_list)
df.to_csv(r'fp_paired_stat2.csv')
