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

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
# nn condition: control, nn-on, nn-off; wn condition: control, nn-on, wn-off
cn = [sets[8][0], sets[7][0]]

# layer list
l_list = sets[2]

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]

# data frame
dataf = {
    'data': [], 'layer': [], 'level': [], 'frequecny': [], 'pvalue': []
    }
c_list = list(dataf.keys())
dats = ['fps', 'fpl']
d_type = ['spk', 'lfp']

# load file
for d in range(len(dats)):
    dt1 = dats[d]
    dt2 = d_type[d]
    with h5py.File(file_input, 'r') as dat:
        ds = [dat[dt1][cn[0]], dat[dt1][cn[1]]]

        for l in range(len(l_list)):
            ly = l_list[l]

            for lv in lvl:
                # list of the max/min spk/lfp frequency in nn band
                fm = []
                dt = ds[1][ly][lv]
                for a in range(len(dt)):
                    fm.append(nt.freq_find(dt[a], find, type=dt2))

                d_test = [ds[0][ly][lv], ds[1][ly][lv]]

                test = nt.fp_wilcoxon([d_test[0], d_test[1]], fm)
                temp = [dt2, ly, lv, 'band_max', test[1]]
                for j in range(len(c_list)):
                    dataf[c_list[j]].append(temp[j])
df = pd.DataFrame(dataf, columns=c_list)
df.to_csv(r'fp_paired_stat.csv')
