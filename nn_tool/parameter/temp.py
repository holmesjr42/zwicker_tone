import numpy as np
import h5py
import spike_tools as st
import pickle
import notch_gap_params as p_tool
import parameters as pm
import sys
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

# data coordination of each animal
db = com.db

# for details, check data_list.ods
acor = db['animal']  # animal coordination
datas = db['datas']  # dB data set location in each animal dict

bf = {}  # best frequency list of each animal
tw = {}  # time window of activity in each animal
lv = {}  # SPLdB list
dst = db['d_strf']  # strf which corresponds to that specific nnm file
p_type = ['nn', 'si']  # corresponds to dict keys for notched noise and
for i in range(len(animals)):
    bf[animals[i]] = db['bf'][i]  # best frequency list of each animal
    tw[animals[i]] = db['tw'][i]  # time window of activity in each animal
    lv[animals[i]] = db['lv'][i]  # SPLdB list


# silence sessions.
s_conds = np.append(nnc.conds, nns.conds[0:2])

# dicts
g_t = {}
g_l = {}
g_f = {}
list_o = {}

'''
strf
'''
f_lfp = snakemake.input.lfp
f_tsp = snakemake.input.tsp
animal = f_tsp.split('/')[2][:-9]

for cond in s_conds:
    g_t[cond + '_strf'] = []
    g_l[cond + '_strf'] = []
    g_f[cond + '_strf'] = []
    list_o[cond + '_strf'] = []
    for i in range(len(f_tsp[cond])):
        a_t = []
        a_f = []
        a_l = []
        # lvl = lv[i]
        # g_t[cond + '_strf'][lvl] = {}
        # g_l[cond + '_strf'][lvl] = {}
        # g_f[cond + '_strf'][lvl] = {}
        # list_o[cond + '_strf'][lvl] = []

        bfs = bf[animal]
        oct_r = p_tool.o_cut(bfs, option=cond)
        t_w = tw[animal]
        # octave rage calculation
        freq_o = np.around(np.log2(freq / bfs), decimals=2)
        list_o[cond + '_strf'].append(freq_o[oct_r[0]:oct_r[1] + 1])

        with h5py.File(f_tsp, 'r') as h_5:
            time_snip = h_5[i]
            mua = st.index_strf(time_snip)
            tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
            ttsp = np.array(tsps[0])
            atsp = np.array(tsps[1])
            g_t[cond + '_strf'].append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
            g_f[cond + '_strf'].append(atsp[:, oct_r[0]:oct_r[1] + 1])

        with h5py.File(f_lfp, 'r') as l_5:
            # print(animal, s_cord, i)
            lfp = l_5[i]
            lfps = st.lfp_strf(p_info, lfp)
            llfp = np.array(lfps[0])
            g_l[cond + '_strf'].append(llfp[:, oct_r[0]:oct_r[1] + 1, :])


'''
continuous notched noise
'''

for cond in nnc.conds:
    g_t[cond] = []
    g_l[cond] = []
    g_f[cond] = []
    list_o[cond] = []
    for i in range(len(f_tsp[cond])):
        bfs = bf[animal]
        oct_r = p_tool.o_cut(bfs, option=cond)

        # octave rage calculation
        freq_o = np.around(np.log2(freq / oct_r[2]), decimals=2)
        list_o[cond].append(freq_o[oct_r[0]:oct_r[1] + 1])
        t_w = tw[animal]
        with h5py.File(f_tsp, 'r') as h_5:
            time_snip = h_5[cond][i]
            mua = st.index_strf(time_snip)
            tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
            ttsp = np.array(tsps[0])
            atsp = np.array(tsps[1])
            g_t[cond].append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
            g_f[cond].append(atsp[:, oct_r[0]:oct_r[1] + 1])
        with h5py.File(f_lfp, 'r') as l_5:
            # print(animal, d_cord, cond, i)
            lfp = l_5[cond][i]
            lfps = st.lfp_strf(p_info, lfp)
            llfp = np.array(lfps[0])
            g_l[cond].append(llfp[:, oct_r[0]:oct_r[1] + 1, :])


'''
notched noise with silence
'''

# timed index for multi-tone pip trigger

p_info31 = nns.p_info31

p_info11 = nns.p_info11

# single file

# animal = animals[0]
# f_tsp = f_path + animal + '/' + animal + '_tsp.hdf5'
# f_lfp = f_path + animal + '/' + animal + '_lfp.hdf5'
#
# with h5py.File(f_tsp, 'r') as h_5:
#     time_snip = h_5['nnm_3_0'][1]
#
# mua = st.index_strf(time_snip)
# k = st.tsp_strf(p_info, mua)

# with h5py.File(f_lfp, 'r') as l_5:
#     lfp = l_5['nnm_3_0'][0]
#     k = st.lfp_strf(p_info, lfp)

# file coordination
# dicts
# g_t = {}
# g_l = {}
# g_f = {}
# list_o = {}
#  nnm sti

for cond in nns.conds:
    g_t[cond] = []
    g_l[cond] = []
    g_f[cond] = []
    list_o[cond] = []
    if cond == 'nnm_3_1' or cond == 'nnm_wn_3_1':
        p_infos = p_info31
    elif cond == 'nnm_1_1' or cond == 'nnm_wn_1_1':
        p_infos = p_info11
    else:
        'read the fucking script again you shithead'
        sys.exit()
    for pt in p_type:
        g_t[cond][pt] = []
        g_l[cond][pt] = []
        g_f[cond][pt] = []
        list_o[cond][pt] = []
        p_info2 = p_infos[pt]
        for i in range(len(f_tsp[cond])):
            a_f = []
            a_t = []
            a_l = []
            lvl = lv[i]
            bfs = bf[animal]
            oct_r = p_tool.o_cut(bfs, option=cond)
            t_w = tw[animal]
            # octave rage calculation
            freq_o = np.around(np.log2(freq / oct_r[2]), decimals=2)
            list_o[cond][pt].append(freq_o[oct_r[0]:oct_r[1] + 1])

            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[cond][i]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_info2, mua, twi=t_w[0], twf=t_w[1])
                ttsp = np.array(tsps[0])
                atsp = np.array(tsps[1])
                g_t[cond][pt].append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
                g_f[cond][pt].append(atsp[:, oct_r[0]:oct_r[1] + 1])
            with h5py.File(f_lfp, 'r') as l_5:
                # print(animal, d_cord, cond, i)
                lfp = l_5[cond][i]
                lfps = st.lfp_strf(p_info2, lfp)
                llfp = np.array(lfps[0])
                g_l[cond][pt].append(llfp[:, oct_r[0]:oct_r[1] + 1, :])


names = ['_tsp', '_lfp', '_freq', '_oct']  # name of an average data file
groups = [g_t, g_l, g_f, list_o]  # data array for each average data type

for i in range(len(names)):
    na = names[i]
    gr = groups[i]

    with open(snakemake.output[0], 'wb') as dat:
        pickle.dump(gr, dat, protocol=pickle.HIGHEST_PROTOCOL)
