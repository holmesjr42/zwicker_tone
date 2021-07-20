import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
from tools import csd_tool as ct
import numpy as np
from parameter import parameters as pm
import h5py
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
import quantities as pq
import neo.core
import pylustrator

sys.path.pop(1)
pylustrator.start()
'''
This is for a single data file.
CSD for nnm continuous condition. Following traditional way with dividing
with h**2 and no sigma is used. Uses rappel filter
'''

sr_lfp = 1061.5 * pq.Hz  # for convert time into data coord in the data file
comm = pm.Commonfeat
bfs = comm.bf_dic  # best frequency dictionary
b_list = comm.list_freq  # list of the 1/8 octave frequency to find index
# for bf/cf frequency
db = comm.db
lvl = db['lv']  # SPLdB list
lfp = {}  # dict of lfp: 0, ctrl; 1, nn
csds = {}  # this is dict to store csd data

val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')
ccmap = val.values()[-1]
lcmap = val2.values()[-1]

# file_input = snakemake.input[0]
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/nnm_lfp_avg/cr79_200211_lfp_avg_nnm.hdf5'

# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]
# loading data
with h5py.File(file_input, 'r') as dat:
    bf = bfs[animal]
    print(bf)
    b_ind = np.where(b_list == bf)[0][0]

    # aranging dataset
    lr = [dat['nnm_3_0'], dat['nnm_3_0_strf']]  # lfps list

    for i in lvl:
        lrg = [np.array(lr[1][i]), np.array(lr[0][i])]

        # lfp raw: 0, ctrl; 1, nn

        lfp[i] = [[] for _ in range(len(lr))]
        for k in range(len(lrg)):
            for j in range(len(lrg[k])):
                lfp[i][k].append(lrg[k][j][b_ind])

    #  csd process
    for lv in list(lfp.keys()):
        csds[lv] = []
        lfps = np.array([lfp[lv][0], lfp[lv][1]]) * pq.microvolt

        for i in range(len(lfps)):
            lfp_d = neo.core.AnalogSignal(lfps[i].T, sampling_rate=sr_lfp)

            csds[lv].append(ct.csd_calc(lfp_d, 'gaussian', (3, 1)))
