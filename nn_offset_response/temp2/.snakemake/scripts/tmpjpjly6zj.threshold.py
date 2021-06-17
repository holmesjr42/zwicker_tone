
######## snakemake preamble start (automatically inserted, do not edit) ########
import sys; sys.path.extend(['/home/bhc/anaconda3/lib/python3.8/site-packages', '/home/bhc/codes/zwicker_tone/nn_offset_response/temp2']); import pickle; snakemake = pickle.loads(b'\x80\x04\x95$\x05\x00\x00\x00\x00\x00\x00\x8c\x10snakemake.script\x94\x8c\tSnakemake\x94\x93\x94)\x81\x94}\x94(\x8c\x05input\x94\x8c\x0csnakemake.io\x94\x8c\nInputFiles\x94\x93\x94)\x81\x94(\x8ca/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr92_201029_tsp.hdf5\x94\x8ca/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr93_201110_tsp.hdf5\x94\x8ca/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr94_201112_tsp.hdf5\x94e}\x94(\x8c\x06_names\x94}\x94\x8c\x12_allowed_overrides\x94]\x94(\x8c\x05index\x94\x8c\x04sort\x94eh\x12\x8c\tfunctools\x94\x8c\x07partial\x94\x93\x94h\x06\x8c\x19Namedlist._used_attribute\x94\x93\x94\x85\x94R\x94(h\x18)}\x94\x8c\x05_name\x94h\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bub\x8c\x06output\x94h\x06\x8c\x0bOutputFiles\x94\x93\x94)\x81\x94\x8ck/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/offset_data/offset_mean_std_1.hdf5\x94a}\x94(h\x0e}\x94h\x10]\x94(h\x12h\x13eh\x12h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bub\x8c\x06params\x94h\x06\x8c\x06Params\x94\x93\x94)\x81\x94}\x94(h\x0e}\x94h\x10]\x94(h\x12h\x13eh\x12h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bub\x8c\twildcards\x94h\x06\x8c\tWildcards\x94\x93\x94)\x81\x94}\x94(h\x0e}\x94h\x10]\x94(h\x12h\x13eh\x12h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bub\x8c\x07threads\x94K\x01\x8c\tresources\x94h\x06\x8c\tResources\x94\x93\x94)\x81\x94(K\x01K\x01e}\x94(h\x0e}\x94(\x8c\x06_cores\x94K\x00N\x86\x94\x8c\x06_nodes\x94K\x01N\x86\x94uh\x10]\x94(h\x12h\x13eh\x12h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bhWK\x01hYK\x01ub\x8c\x03log\x94h\x06\x8c\x03Log\x94\x93\x94)\x81\x94}\x94(h\x0e}\x94h\x10]\x94(h\x12h\x13eh\x12h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x12sNt\x94bh\x13h\x16h\x18\x85\x94R\x94(h\x18)}\x94h\x1ch\x13sNt\x94bub\x8c\x06config\x94}\x94\x8c\x04rule\x94\x8c\x0bthreshold_1\x94\x8c\x0fbench_iteration\x94N\x8c\tscriptdir\x94\x8c5/home/bhc/codes/zwicker_tone/nn_offset_response/temp2\x94ub.'); from snakemake.logging import logger; logger.printshellcmds = False; __real_file__ = __file__; __file__ = '/home/bhc/codes/zwicker_tone/nn_offset_response/temp2/threshold.py';
######## snakemake preamble end #########
import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nnm_plot as nnp
from tools import nn_tool as nt
from parameter import parameters as pm
# import pylustrator
import matplotlib.pyplot as plt
# pylustrator.start()
sys.path.pop(1)

# file_spk = 'D:/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr79_200211_tsp.hdf5'
file_spk = snakemake.input
# file_lfp = 'D:/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr79_200211_lfp_fil.hdf5'

# condition setups
cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
ind = [pm.Nn.nn_i['nn31'], pm.Nn.nn_i['nn11']]  # indices for each condition sessions
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
trf = [150, 50]  # time points to calculate reference session range

group = {}


for file_input in file_spk:
    s_ref = [[] for _ in range(len(cond))]
    l_ref = [[] for _ in range(len(cond))]
    animal = nnp.animal_name(file_input)
    with h5py.File(file_input, 'r') as dat:
        for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
            if animal == 'cr103' and 'nn_1_1' in cond[j]:
                s_ref[j] = np.zeros([16, 2])
            else:
                ti = ind[j][0]
                tf = ind[j][1]
                t_off = offset[j]
                print('hate')
                for ch in range(16):  # channels
                    ths = []
                    print('waiting')
                    for k in range(len(cond[j])):  # choosing between notch and white noise
                        print('for')
                        for i in range(len(ti)):  # collecting offset-kinda reference session
                            print('result', animal, cond[j][k], ch, i)
                            data = dat[cond[j][k]][0]
                            mua = nt.index_spike(data)
                            t_i = ti[i] + t_off + trf[0]
                            t_f = tf[i] - trf[1]
                            ths.extend(mua[ch][t_i:t_f])

                    std = np.std(ths)
                    mean = np.mean(ths)
                    base = [mean, std]
                    s_ref[j].append(base)

        group[animal] = s_ref
# with h5py.File(file_lfp, 'r') as dat:
#     for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
#         ti = ind[j][0]
#         tf = ind[j][1]
#         t_off = offset[j]
#         print('why')
#         for ch in range(16):  # channels
#             ths = []
#             print('you')
#             for k in range(len(cond[j])):  # choosing between notch and white noise
#                 print('do')
#                 for i in range(len(ti)):  # collecting offset-kinda reference session
#                     print('this', i)
#                     data = dat[cond[j][k]][0][ch]
#                     t_i = nt.lfp_index(ti[i] + t_off + trf[0])\
#
#                     t_f = nt.lfp_index(tf[i] - trf[1])
#                     ths.extend(data[t_i:t_f])

            # l_ref[j].append(ths)

with h5py.File(snakemake.output[0], 'w') as h:
    for t in list(group.keys()):
        d1 = h.create_dataset(t, data=group[t])
