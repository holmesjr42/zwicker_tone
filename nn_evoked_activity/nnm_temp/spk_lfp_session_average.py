import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import h5py
import pickle
from tools import spike_tools as st
from parameters import notch_gap_params as p_tool
from parameters import parameters as pm
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

s_conds = nnc.conds + nns.conds[0:2]

# dicts
g_t = {}  # tsp session average dict
g_l = {}  # lfp session average dict
g_f = {}  # spike frequency profile dict
g_s = {}  # spike frequency profile standard deviation dict
g_cf = {}  # spike frequency profile standard error of mean dict
g_lf = {}  # lfp frequency profile dict
g_ls = {}  # lfp frequency profile standard deviation dict
g_lcf = {}  # lfp frequency profile confidence interval(95%) of mean dict
list_o = {}  # list of octave

# the average of all strf session in an animal

# g_t['a_strf'] = {'70': [], '60': [], '50': [], '40': []}
# g_l['a_strf'] = {'70': [], '60': [], '50': [], '40': []}
# g_f['a_strf'] = {'70': [], '60': [], '50': [], '40': []}
# g_lf['a_strf'] = {'70': [], '60': [], '50': [], '40': []}
# st2 = {'70': [], '60': [], '50': [], '40': []}
# sf2 = {'70': [], '60': [], '50': [], '40': []}
# sl2 = {'70': [], '60': [], '50': [], '40': []}
# slf2 = {'70': [], '60': [], '50': [], '40': []}
# data to load

# f_lfp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
#         '/data/dataset/lfp_fil/cr90_201023_lfp_fil.hdf5'
# f_tsp = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data' \
#         '/dataset/tsp/cr90_201023_tsp.hdf5'

# f_lfp = snakemake.input.lfp
# f_tsp = snakemake.input.tsp

f_ani = f_lfp.split('/')[-1].split('_')[0]  # cr# of animal

an = 0  # the index of the animal used in this script

for num_a, ani in enumerate(animals):
    if f_ani in ani:
        an = num_a
        break

print(f"{f_ani}: {an}")

if f_ani in ['cr92', 'cr93']:
    with h5py.File(snakemake.output[0], 'w') as h:
        d2 = h.create_dataset('na', data=[])
    sys.exit()


'''
strf
'''

for cond in s_conds:
    g_t[cond + '_strf'] = {}
    g_l[cond + '_strf'] = {}
    g_f[cond + '_strf'] = {}
    g_s[cond + '_strf'] = {}
    g_cf[cond + '_strf'] = {}
    g_lf[cond + '_strf'] = {}
    g_ls[cond + '_strf'] = {}
    g_lcf[cond + '_strf'] = {}
    list_o[cond + '_strf'] = {}
    for i in range(len(lv)):
        lvl = lv[i]
        g_t[cond + '_strf'][lvl] = []
        g_l[cond + '_strf'][lvl] = []
        g_f[cond + '_strf'][lvl] = []
        g_s[cond + '_strf'][lvl] = []
        g_cf[cond + '_strf'][lvl] = []
        g_lf[cond + '_strf'][lvl] = []
        g_ls[cond + '_strf'][lvl] = []
        g_lcf[cond + '_strf'][lvl] = []
        list_o[cond + '_strf'][lvl] = []

        if np.isnan(acor[cond][i][an]):
            print('hey')
            continue

        else:
            s_cord = dst[cond][an]
            bfs = bf[an]
            oct_r = p_tool.o_cut(bfs, option=cond)

            # octave range calculation
            freq_o = np.around(np.log2(freq / bfs), decimals=2)
            list_o[cond + '_strf'][lvl].extend(freq_o[oct_r[0]:oct_r[1] + 1])

            # select spk activation time window
            t_w = tw[an]

            # loading the tsp/lfp dataset
            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[s_cord][i]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
                ts = np.array(tsps[0])  # temporal spk data
                at = np.array(tsps[1])  # frequency profile
                std = np.array(tsps[2])  # std of freqency profile
                cof = np.array(tsps[3])  # conf of freqency profile
                g_t[f'{cond}_strf'][lvl].extend(
                    ts[:, oct_r[0]:oct_r[1] + 1, :]
                    )
                g_f[f'{cond}_strf'][lvl].extend(
                    at[:, oct_r[0]:oct_r[1] + 1]
                    )
                g_s[f'{cond}_strf'][lvl].extend(
                    std[:, oct_r[0]:oct_r[1] + 1]
                    )
                g_cf[f'{cond}_strf'][lvl].extend(
                    cof[:, oct_r[0]:oct_r[1] + 1]
                    )

                # st2[lvl].append(t2)
                # sf2[lvl].append(f2)
                print(f_ani, cond, lvl)
            with h5py.File(f_lfp, 'r') as l_5:
                lfp = l_5[s_cord][i]
                lfps = st.lfp_strf(p_info, lfp, tw=100, twi=t_w[0], twf=t_w[1])
                lf = np.array(lfps[0])  # temporal lfp data
                al = np.array(lfps[1])  # frequency profile
                sl = np.array(lfps[2])  # std of freqency profile
                cofl = np.array(lfps[3])  # conf of freqency profile

                g_l[f'{cond}_strf'][lvl].extend(
                    lf[:, oct_r[0]:oct_r[1] + 1, :]
                    )
                g_lf[f'{cond}_strf'][lvl].extend(
                    al[:, oct_r[0]:oct_r[1] + 1]
                    )
                g_ls[f'{cond}_strf'][lvl].extend(
                    sl[:, oct_r[0]:oct_r[1] + 1]
                    )
                g_lcf[f'{cond}_strf'][lvl].extend(
                    cofl[:, oct_r[0]:oct_r[1] + 1]
                    )
                # sl2[lvl].append(l2)
                # slf2[lvl].append(lf2)
        print(np.shape(g_l[f'{cond}_strf'][lvl]))
        print(f'{cond}_strf:{lvl} is finished')
    print(f'{cond}_strf is finished')
# for lvl in lv:
#     if not np.any(st2[lvl]):
#         continue
#     else:
#         g_t['a_strf'][lvl].extend(np.mean(st2[lvl], axis=0))
#         g_l['a_strf'][lvl].extend(np.mean(sl2[lvl], axis=0))
#         g_f['a_strf'][lvl].extend(np.mean(sf2[lvl], axis=0))
#         g_lf['a_strf'][lvl].extend(np.mean(slf2[lvl], axis=0))

'''
nnm continuous
'''

for cond in nnc.conds:
    g_t[cond] = {}
    g_l[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    g_s[cond] = {}
    g_ls[cond] = {}
    g_cf[cond] = {}
    g_lcf[cond] = {}
    list_o[cond] = {}
    for i in range(len(lv)):
        lvl = lv[i]
        g_t[cond][lvl] = []
        g_l[cond][lvl] = []
        g_f[cond][lvl] = []
        g_lf[cond][lvl] = []
        g_s[cond][lvl] = []
        g_ls[cond][lvl] = []
        g_cf[cond][lvl] = []
        g_lcf[cond][lvl] = []
        list_o[cond][lvl] = []

        if np.isnan(acor[cond][i][an]):
            print('hey')
            continue

        else:
            d_cord = datas[cond][i][an]
            bfs = bf[an]
            oct_r = p_tool.o_cut(bfs, option=cond)

            # octave range calculation
            freq_o = np.around(np.log2(freq / bfs), decimals=2)
            list_o[cond][lvl].extend(freq_o[oct_r[0]:oct_r[1] + 1])

            # select spk activation time window
            t_w = tw[an]

            # loading the tsp/lfp dataset
            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[cond][d_cord]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
                ts = np.array(tsps[0])  # temporal spk data
                at = np.array(tsps[1])  # frequency profile
                std = np.array(tsps[2])  # std of freqency profile
                cof = np.array(tsps[3])  # cof of freqency profile
                g_t[cond][lvl].extend(ts[:, oct_r[0]:oct_r[1] + 1, :])
                g_f[cond][lvl].extend(at[:, oct_r[0]:oct_r[1] + 1])
                g_s[cond][lvl].extend(std[:, oct_r[0]:oct_r[1] + 1])
                g_cf[cond][lvl].extend(cof[:, oct_r[0]:oct_r[1] + 1])
            with h5py.File(f_lfp, 'r') as l_5:
                lfp = l_5[cond][d_cord]
                lfps = st.lfp_strf(p_info, lfp, tw=100, twi=t_w[0], twf=t_w[1])
                lf = np.array(lfps[0])  # temporal spk data
                al = np.array(lfps[1])  # frequency profile
                sl = np.array(lfps[2])  # std of freqency profile
                cofl = np.array(lfps[3])  # cof of freqency profile
                g_l[cond][lvl].extend(lf[:, oct_r[0]:oct_r[1] + 1, :])
                g_lf[cond][lvl].extend(al[:, oct_r[0]:oct_r[1] + 1])
                g_ls[cond][lvl].extend(sl[:, oct_r[0]:oct_r[1] + 1])
                g_lcf[cond][lvl].extend(cofl[:, oct_r[0]:oct_r[1] + 1])
        print(f'{cond}:{lvl} is finished')
    print(f'{cond} is finished')

'''
nnm on-off
'''

for cond in nns.conds:
    g_t[cond] = {}
    g_l[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    g_s[cond] = {}
    g_ls[cond] = {}
    g_cf[cond] = {}
    g_lcf[cond] = {}
    list_o[cond] = {}

    if cond == 'nnm_3_1' or cond == 'nnm_wn_3_1':
        p_infot = p_info3
    elif cond == 'nnm_1_1' or cond == 'nnm_wn_1_1':
        p_infot = p_info1
    else:
        'read the fucking script again you shithead'
        sys.exit()
    for pt in p_type:
        g_t[cond][pt] = {}
        g_l[cond][pt] = {}
        g_f[cond][pt] = {}
        g_lf[cond][pt] = {}
        g_s[cond][pt] = {}
        g_ls[cond][pt] = {}
        g_cf[cond][pt] = {}
        g_lcf[cond][pt] = {}
        list_o[cond][pt] = {}
        p_infop = p_infot[pt]

        for i in range(len(lv)):
            lvl = lv[i]
            g_t[cond][pt][lvl] = []
            g_l[cond][pt][lvl] = []
            g_f[cond][pt][lvl] = []
            g_lf[cond][pt][lvl] = []
            g_s[cond][pt][lvl] = []
            g_ls[cond][pt][lvl] = []
            g_cf[cond][pt][lvl] = []
            g_lcf[cond][pt][lvl] = []
            list_o[cond][pt][lvl] = []
            if np.isnan(acor[cond][i][an]):
                print('hey')
                continue

            else:
                d_cord = datas[cond][i][an]
                bfs = bf[an]
                oct_r = p_tool.o_cut(bfs, option=cond)

                # octave range calculation
                freq_o = np.around(np.log2(freq / bfs), decimals=2)
                list_o[cond][pt][lvl].extend(freq_o[oct_r[0]:oct_r[1] + 1])

                # select spk activation time window
                t_w = tw[an]

                # loading the tsp/lfp dataset
                with h5py.File(f_tsp, 'r') as h_5:
                    time_snip = h_5[cond][d_cord]
                    mua = st.index_strf(time_snip)
                    tsps = st.tsp_strf(p_infop, mua, twi=t_w[0], twf=t_w[1])
                    ts = np.array(tsps[0])  # temporal spk data
                    at = np.array(tsps[1])  # frequency profile
                    std = np.array(tsps[2])  # std of freqency profile
                    cof = np.array(tsps[3])  # cof of freqency profile

                    g_t[cond][pt][lvl].extend(ts[:, oct_r[0]:oct_r[1] + 1, :])
                    g_f[cond][pt][lvl].extend(at[:, oct_r[0]:oct_r[1] + 1])
                    g_s[cond][pt][lvl].extend(std[:, oct_r[0]:oct_r[1] + 1])
                    g_cf[cond][pt][lvl].extend(cof[:, oct_r[0]:oct_r[1] + 1])

                with h5py.File(f_lfp, 'r') as l_5:
                    lfp = l_5[cond][d_cord]
                    lfps = st.lfp_strf(p_infop, lfp, tw=100, twi=t_w[0],
                                       twf=t_w[1])
                    lf = np.array(lfps[0])
                    al = np.array(lfps[1])
                    sl = np.array(lfps[2])
                    cofl = np.array(lfps[3])
                    print(np.shape(cofl), 'check')
                    g_l[cond][pt][lvl].extend(lf[:, oct_r[0]:oct_r[1] + 1, :])
                    g_lf[cond][pt][lvl].extend(al[:, oct_r[0]:oct_r[1] + 1])
                    g_ls[cond][pt][lvl].extend(sl[:, oct_r[0]:oct_r[1] + 1])
                    g_lcf[cond][pt][lvl].extend(cofl[:, oct_r[0]:oct_r[1] + 1])

                print(np.shape(g_l[cond][pt][lvl]))
            print(f'{cond}_{pt}:{lvl} is finished')
        print(f'{cond}_{pt} is finished')

groups = {'tsp': g_t, 'fpt': g_f, 'lfp': g_l, 'fpl': g_lf, 'ssd': g_s,
          'lsd': g_ls, 'scf': g_cf, 'lcf': g_lcf
          }
# s_conds = s_conds + ['a']

with h5py.File(snakemake.output[0], 'w') as h:
# with h5py.File('testing.hdf5', 'w') as h:
    for t in list(groups.keys()):
        d1 = h.create_group(t)
        for cond in s_conds:
            d2 = d1.create_group(f'{cond}_strf')
            for lvl in lv:
                d3 = d2.create_dataset(
                    lvl, data=groups[t][f'{cond}_strf'][lvl])

        for cond in nnc.conds:
            d2 = d1.create_group(cond)
            for lvl in lv:
                d3 = d2.create_dataset(lvl, data=groups[t][cond][lvl])

        for cond in nns.conds:
            d2 = d1.create_group(cond)
            for pt in p_type:
                d3 = d2.create_group(pt)
                for lvl in lv:
                    d4 = d3.create_dataset(lvl, data=groups[t][cond][pt][lvl])

