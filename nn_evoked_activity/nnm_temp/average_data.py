import numpy as np
import h5py
from tools import spike_tools as st
import pickle
from tools import notch_gap_params as p_tool
from parameters import parameters as pm
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
bf = db['bf']  # best frequency list of each animal
tw = db['tw']  # time window of activity in each animal
lv = db['lv']  # SPLdB list
dst = db['d_strf']  # strf which corresponds to that specific nnm file
p_type = ['nn', 'si']  # corresponds to dict keys for notched noise and

# silence sessions.

s_conds = np.append(nnc.conds, nns.conds[0:2])

# dicts
g_t = {}    # spike
g_l = {}    # lfp
g_f = {}    # frequecny profile
g_lf = {}   # lfp frequency profile
list_o = {}    # octave list

'''
strf
'''

for cond in s_conds:
    g_t[cond + '_strf'] = {}
    g_l[cond + '_strf'] = {}
    g_f[cond + '_strf'] = {}
    g_lf[cond + '_strf'] = {}
    list_o[cond + '_strf'] = {}
    for i in range(len(acor[cond])):
        # bfs = []
        # tws = []
        a_t = []
        a_f = []
        a_l = []
        a_lf = []
        lvl = lv[i]
        g_t[cond + '_strf'][lvl] = {}
        g_l[cond + '_strf'][lvl] = {}
        g_f[cond + '_strf'][lvl] = {}
        g_lf[cond + '_strf'][lvl] = {}
        list_o[cond + '_strf'][lvl] = []
        for j in acor[cond][i]:
            animal = animals[j]
            s_cord = dst[cond][j]
            bfs = bf[j]
            oct_r = p_tool.o_cut(bfs, option=cond)

            # octave range calculation
            freq_o = np.around(np.log2(freq / bfs), decimals=2)
            list_o[cond + '_strf'][lvl].append(freq_o[oct_r[0]:oct_r[1] + 1])

            # loading the tsp/lfp dataset
            f_tsp = f_path + 'tsp/' + animal + '_tsp.hdf5'
            f_lfp = f_path + 'lfp_fil/' + animal + '_lfp_fil.hdf5'
            t_w = tw[j]
            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[s_cord][i]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
                ttsp = np.array(tsps[0])
                atsp = np.array(tsps[1])
                a_t.append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
                a_f.append(atsp[:, oct_r[0]:oct_r[1] + 1])

            with h5py.File(f_lfp, 'r') as l_5:
                # print(animal, s_cord, i)
                lfp = l_5[s_cord][i]
                lfps = st.lfp_strf(p_info, lfp)
                llfp = np.array(lfps[0])
                alfp = np.array(lfps[1])
                a_l.append(llfp[:, oct_r[0]:oct_r[1] + 1, :])
                a_lf.append(alfp[:, oct_r[0]:oct_r[1] + 1])
        #
        g_t[cond + '_strf'][lvl] = np.mean(a_t, axis=0)
        g_f[cond + '_strf'][lvl] = np.mean(a_f, axis=0)
        g_l[cond + '_strf'][lvl] = np.mean(a_l, axis=0)
        g_lf[cond + '_strf'][lvl] = np.mean(a_lf, axis=0)
        print('strf ' + cond + ' ' + lv[i] + ' finished')

'''
continuous notched noise
'''


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

# average across animals

for cond in nnc.conds:
    g_t[cond] = {}
    g_l[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    list_o[cond] = {}
    for i in range(len(acor[cond])):
        a_f = []
        a_t = []
        a_l = []
        a_lf = []
        lvl = lv[i]
        g_t[cond][lvl] = {}
        g_l[cond][lvl] = {}
        g_f[cond][lvl] = {}
        g_lf[cond][lvl] = {}
        list_o[cond][lvl] = []
        for j in acor[cond][i]:
            animal = animals[j]
            d_cord = datas[cond][i][j]
            bfs = bf[j]
            oct_r = p_tool.o_cut(bfs, option=cond)

            # octave rage calculation
            freq_o = np.around(np.log2(freq / oct_r[2]), decimals=2)
            list_o[cond][lvl].append(freq_o[oct_r[0]:oct_r[1] + 1])

            # loading the tsp/lfp dataset
            f_tsp = f_path + 'tsp/' + animal + '_tsp.hdf5'
            f_lfp = f_path + 'lfp_fil/' + animal + '_lfp_fil.hdf5'
            t_w = tw[j]
            with h5py.File(f_tsp, 'r') as h_5:
                time_snip = h_5[cond][d_cord]
                mua = st.index_strf(time_snip)
                tsps = st.tsp_strf(p_info, mua, twi=t_w[0], twf=t_w[1])
                ttsp = np.array(tsps[0])
                atsp = np.array(tsps[1])
                a_t.append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
                a_f.append(atsp[:, oct_r[0]:oct_r[1] + 1])
            with h5py.File(f_lfp, 'r') as l_5:
                # print(animal, d_cord, cond, i)
                lfp = l_5[cond][d_cord]
                lfps = st.lfp_strf(p_info, lfp)
                llfp = np.array(lfps[0])
                alfp = np.array(lfps[1])
                a_l.append(llfp[:, oct_r[0]:oct_r[1] + 1, :])
                a_lf.append(alfp[:, oct_r[0]:oct_r[1] + 1])
        g_t[cond][lvl] = np.mean(a_t, axis=0)
        g_f[cond][lvl] = np.mean(a_f, axis=0)
        g_l[cond][lvl] = np.mean(a_l, axis=0)
        g_lf[cond][lvl] = np.mean(a_lf, axis=0)
        print('notch ' + cond + ' ' + lv[i] + ' finished')

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
    g_t[cond] = {}
    g_l[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    list_o[cond] = {}
    if cond == 'nnm_3_1' or cond == 'nnm_wn_3_1':
        p_infos = p_info31
    elif cond == 'nnm_1_1' or cond == 'nnm_wn_1_1':
        p_infos = p_info11
    else:
        'read the fucking script again you shithead'
        sys.exit()
    for pt in p_type:
        g_t[cond][pt] = {}
        g_l[cond][pt] = {}
        g_f[cond][pt] = {}
        g_lf[cond][pt] = {}
        list_o[cond][pt] = {}
        p_info2 = p_infos[pt]
        for i in range(len(acor[cond])):
            a_f = []
            a_t = []
            a_l = []
            a_lf = []
            lvl = lv[i]
            g_t[cond][pt][lvl] = {}
            g_l[cond][pt][lvl] = {}
            g_f[cond][pt][lvl] = {}
            g_lf[cond][pt][lvl] = {}
            list_o[cond][pt][lvl] = []
            for j in acor[cond][i]:
                animal = animals[j]
                d_cord = datas[cond][i][j]
                bfs = bf[j]
                oct_r = p_tool.o_cut(bfs, option=cond)

                # octave rage calculation
                freq_o = np.around(np.log2(freq / oct_r[2]), decimals=2)
                list_o[cond][pt][lvl].append(freq_o[oct_r[0]:oct_r[1] + 1])

                # loading the tsp/lfp dataset
                f_tsp = f_path + 'tsp/' + animal + '_tsp.hdf5'
                f_lfp = f_path + 'lfp_fil/' + animal + '_lfp_fil.hdf5'
                t_w = tw[j]
                with h5py.File(f_tsp, 'r') as h_5:
                    time_snip = h_5[cond][d_cord]
                    mua = st.index_strf(time_snip)
                    tsps = st.tsp_strf(p_info2, mua, twi=t_w[0], twf=t_w[1])
                    ttsp = np.array(tsps[0])
                    atsp = np.array(tsps[1])
                    a_t.append(ttsp[:, oct_r[0]:oct_r[1] + 1, :])
                    a_f.append(atsp[:, oct_r[0]:oct_r[1] + 1])
                with h5py.File(f_lfp, 'r') as l_5:
                    # print(animal, d_cord, cond, i)
                    lfp = l_5[cond][d_cord]
                    lfps = st.lfp_strf(p_info2, lfp)
                    llfp = np.array(lfps[0])
                    alfp = np.array(lfps[1])
                    a_l.append(llfp[:, oct_r[0]:oct_r[1] + 1, :])
                    a_lf.append(alfp[:, oct_r[0]:oct_r[1] + 1])
            g_t[cond][pt][lvl] = np.mean(a_t, axis=0)
            g_f[cond][pt][lvl] = np.mean(a_f, axis=0)
            g_l[cond][pt][lvl] = np.mean(a_l, axis=0)
            g_lf[cond][pt][lvl] = np.mean(a_lf, axis=0)
            print(
                  'notch ' + cond + ' ' + pt + ' ' + lv[i] + ' finished'
                 )

names = ['_tsp', '_lfp', '_freq', '_freq_l', '_oct']  # name of an average
# data
# file
groups = [g_t, g_l, g_f, g_lf, list_o]  # data array for each average data type

for i in range(len(names)):
    na = names[i]
    gr = groups[i]

    with open(f_path + 'average' + na + '.pk',
              'wb') as dat:
        pickle.dump(gr, dat, protocol=pickle.HIGHEST_PROTOCOL)
