import os
import sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
import numpy as np
import h5py
import pickle
from tools import spike_tools as st
from parameter import notch_gap_params as p_tool
from parameter import parameters as pm
import sys
sys.path.pop(1)

'''
This is creating average of all the animal data. 
std and confidence interval (0.95) is between time window used for generate 
frequency profile
recording session.
'''

'''
setup
'''
# classes
com = pm.Commonfeat  # common features
nnc = pm.Nnmcontfeat  # continuous notched noise features
nns = pm.Nnsifeat  # notch on-off features


# frequency list turned from octave to Hz
freq = com.list_freq

# any other variables are included in spike_tools
f_path = com.f_path

# animal/data folder name
animals = com.animals

# time index for strf
p_info = com.p_info
p_info1 = nns.p_info11
p_info3 = nns.p_info31

# data coordination of each animal
db = com.db

# for details, check data_list.ods
acor = db['animal']  # animal coordination
datas = db['datas']  # dB data set location in each animal dict
bf = db['bf']  # best frequency list of each animal
tw = db['tw']  # time window of activity in each animal
lv = db['lv']  # SPLdB list
dst = db['d_strf']  # strf which corresponds to that specific nnm file
p_type = ['nn', 'si']  # corresponds to dict keys for notched noise and

# silence sessions.

s_conds = ['strf_1']

# dicts
g_t = {}  # tsp, tsp session average dict
g_l = {}  # lfp, lfp session average dict
g_f = {}  # fpt, spike frequency profile dict
g_mf = {}  # fpt, spike frequency profile dict with max value
g_s = {}  # ssd, spike frequency profile standard deviation dict
g_cf = {}  # scf, spike frequency profile confidence interval(95%) dict
g_lf = {}  # fpl, lfp frequency profile dict
g_mlf = {}  # fpl, lfp frequency profile dict with min value
g_mlb = {}  # baseline for lfp frequency profile
g_ls = {}  # lsd, lfp frequency profile standard deviation dict
g_lcf = {}  # lcf, lfp frequency profile confidence interval(95%) of mean dict
list_o = {}  # list of octave

# data to load

f_lfp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data' \
        '/dataset/lfp_fil/cr122b_210604_lfp_fil.hdf5'
f_tsp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data' \
        '/dataset/tsp/cr122b_210604_tsp.hdf5'


f_ani = f_lfp.split('/')[-1].split('_')[0] + '_' +\
        f_lfp.split('/')[-1].split('_')[1]  # animal number
#
# an = 0  # the index of the animal used in this script
#
# for num_a, ani in enumerate(animals):
#     if f_ani in ani:
#         an = num_a
#         break
#
# print(f"{f_ani}: {an}")

'''
strf
'''
for cond in s_conds:
    g_t[cond] = {}
    g_l[cond] = {}
    for i in range(len(lv)):
        lvl = lv[i]
        g_t[cond][lvl] = []
        g_l[cond][lvl] = []
        # loading the tsp/lfp dataset
        with h5py.File(f_tsp, 'r') as h_5:
            time_snip = h_5[s_conds[0]][i]
            mua = st.index_strf(time_snip)
            tsps = st.tsp_strf(p_info, mua)
            ts = np.array(tsps[0])  # temporal spk data
            # at = np.array(tsps[1])  # frequency profile
            # mt = np.array(tsps[4])  # frequency profile with max value
            # std = np.array(tsps[2])  # std of freqency profile
            # cof = np.array(tsps[3])  # conf of freqency profile

            g_t[cond][lvl].extend(ts)
            # g_f[f'{cond}_strf'][lvl].extend(
            #     at
            #     )
            # g_mf[f'{cond}_strf'][lvl].extend(
            #     mt
            #     )
            # g_s[f'{cond}_strf'][lvl].extend(
            #     std
            #     )
            # g_cf[f'{cond}_strf'][lvl].extend(
            #     cof
            #     )
            print(f'{cond}: {lvl} for spike finished')
        with h5py.File(f_lfp, 'r') as l_5:
            lfp = l_5[s_conds[0]][i]
            lfps = st.lfp_strf(p_info, lfp)
            lf = np.array(lfps[0])  # temporal lfp data
            # al = np.array(lfps[1])  # frequency profile
            # ml = np.array(lfps[4])  # frequency profile with min val
            # sl = np.array(lfps[2])  # std of freqency profile
            # cofl = np.array(lfps[3])  # conf of freqency profile
            # base = np.array(lfps[5])

            g_l[f'{cond}'][lvl].extend(lf)
            # g_lf[f'{cond}_strf'][lvl].extend(
            #     al
            #     )
            # g_mlf[f'{cond}_strf'][lvl].extend(
            #     ml
            #     )
            # g_mlb[f'{cond}_strf'][lvl].extend(
            #     base
            #     )
            # g_ls[f'{cond}_strf'][lvl].extend(
            #     sl
            #     )
            # g_lcf[f'{cond}_strf'][lvl].extend(
            #     cofl
            #     )
            print(f'{cond}: {lvl} for lfp finished')



'''
nnm on-off
'''
n_conds = ['nnm_3_1']
for cond in n_conds:
    g_t[cond] = {}
    g_l[cond] = {}
    if cond == 'nnm_3_1' or cond == 'nnm_wn_3_1':
        p_infot = p_info3
    elif cond == 'nnm_1_1' or cond == 'nnm_wn_1_1':
        p_infot = p_info1
    else:
        'read the fucking script again you shithead'
        raise ValueError
    for pt in p_type:
        g_t[cond][pt] = {}
        g_l[cond][pt] = {}
        p_infop = p_infot[pt]

        for i in range(len(lv)):
            lvl = lv[i]
            g_t[cond][pt][lvl] = []
            g_l[cond][pt][lvl] = []

            # loading the tsp/lfp dataset
            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[cond][i]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_infop, mua)
                ts = np.array(tsps[0])  # temporal spk data
                # at = np.array(tsps[1])  # frequency profile
                # mt = np.array(tsps[4])  # frequency profile with max value
                # std = np.array(tsps[2])  # std of freqency profile
                # cof = np.array(tsps[3])  # cof of freqency profile

                g_t[cond][pt][lvl].extend(ts)
                # g_f[cond][pt][lvl].extend(at[:, oct_r[0]:oct_r[1] + 1])
                # g_mf[cond][pt][lvl].extend(mt[:, oct_r[0]:oct_r[1] + 1])
                # g_s[cond][pt][lvl].extend(std[:, oct_r[0]:oct_r[1] + 1])
                # g_cf[cond][pt][lvl].extend(cof[:, oct_r[0]:oct_r[1] + 1])

            with h5py.File(f_lfp, 'r') as l_5:
                lfp = l_5[cond][i]
                lfps = st.lfp_strf(p_infop, lfp, tw=100)
                lf = np.array(lfps[0])
                # al = np.array(lfps[1])
                # ml = np.array(lfps[4])  # frequency profile with min val
                # sl = np.array(lfps[2])
                # cofl = np.array(lfps[3])
                # base = np.array(lfps[5])
                g_l[cond][pt][lvl].extend(lf)
                # g_lf[cond][pt][lvl].extend(al[:, oct_r[0]:oct_r[1] + 1])
                # g_mlf[cond][pt][lvl].extend(ml[:, oct_r[0]:oct_r[1] + 1])
                # g_mlb[cond][pt][lvl].extend(base[:, oct_r[0]:oct_r[1] + 1])
                # g_ls[cond][pt][lvl].extend(sl[:, oct_r[0]:oct_r[1] + 1])
                # g_lcf[cond][pt][lvl].extend(cofl[:, oct_r[0]:oct_r[1] + 1])
                print(f'{cond}: {lvl}, {pt} finished')


groups = {'spk': g_t, 'lfp': g_l}

with h5py.File(f_ani + '_spk_lfp_avg_nnm.hdf5', 'w') as h:
    for t in list(groups.keys()):
        d1 = h.create_group(t)
        for cond in s_conds:
            d2 = d1.create_group(cond)
            for lvl in lv:
                d3 = d2.create_dataset(
                    lvl, data=groups[t][cond][lvl])


        for cond in n_conds:
            d2 = d1.create_group(cond)
            for pt in p_type:
                d3 = d2.create_group(pt)
                for lvl in lv:
                    d4 = d3.create_dataset(lvl, data=groups[t][cond][pt][lvl])
