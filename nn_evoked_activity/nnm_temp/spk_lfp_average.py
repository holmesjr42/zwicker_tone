import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import h5py
from parameters import parameters as pm
import statsmodels.stats.api as sms
import quantities as pq
import neo.core
from tools import icsd
sys.path.pop(1)

'''
This is creating average of all the animal data. 
std and confidence interval (0.95) is between animals.
'''

'''
setup
'''
file_input = snakemake.input
# file_input = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
#               ".hdf5"]
# classes
com = pm.Commonfeat  # common features
nnc = pm.Nnmcontfeat  # continuous notched noise features
nns = pm.Nnsifeat  # notch on-off features

# frequency list turned from octave to Hz
freq = com.list_freq

# any other variables are included in spike_tools
f_path = com.f_path

# animal/data folder name
animals = []
for i in range(len(file_input)):
    animals = np.append(animals, file_input[i].split('/')[-1].split('_')[0])

# time index for strf
p_info = com.p_info
p_info1 = nns.p_info11
p_info3 = nns.p_info31

# data coordination of each animal
db = com.db

# for details, check data_list.ods
acor = db['animal']  # animal coordination
lv = db['lv']  # SPLdB list

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
g_lcf = {}  # lfp frequency profile standard error of mean dict


'''
strf
'''
print(s_conds)
for cond in s_conds:
    cond_s = f'{cond}_strf'
    g_l[cond_s] = {}
    g_t[cond_s] = {}
    g_f[cond_s] = {}
    g_lf[cond_s] = {}
    g_s[cond_s] = {}
    g_cf[cond_s] = {}
    g_ls[cond_s] = {}
    g_lcf[cond_s] = {}
    for i in range(len(lv)):
        a_l = []
        a_t = []
        a_lf = []
        a_f = []
        a_cf = [[] for _ in range(16)]
        a_lcf = [[] for _ in range(16)]

        lvl = lv[i]
        g_l[cond_s][lvl] = {}
        g_t[cond_s][lvl] = {}
        g_f[cond_s][lvl] = {}
        g_lf[cond_s][lvl] = {}
        g_s[cond_s][lvl] = {}
        g_ls[cond_s][lvl] = {}
        g_cf[cond_s][lvl] = {}
        g_lcf[cond_s][lvl] = {}
        for j in acor[cond][i]:
            if np.isnan(j):
                continue
            else:
                with h5py.File(file_input[j], 'r') as dat:
                    print(file_input[j], dat['lfp'].keys())
                    datas = dat
                    dats = [
                            np.array(datas['lfp'][cond_s][lvl]),
                            np.array(datas['tsp'][cond_s][lvl]),
                            np.array(datas['fpl'][cond_s][lvl]),
                            np.array(datas['fpt'][cond_s][lvl])
                           ]
                    print(cond_s, lvl, np.shape(dats[0]))
                    a_l.append(dats[0])
                    a_t.append(dats[1])
                    a_lf.append(dats[2])
                    a_f.append(dats[3])
        a_f2 = np.transpose(a_f)
        a_lf2 = np.transpose(a_lf)

        g_l[cond_s][lvl] = np.mean(a_l, axis=0)
        g_t[cond_s][lvl] = np.mean(a_t, axis=0)
        g_f[cond_s][lvl] = np.mean(a_f, axis=0)
        g_lf[cond_s][lvl] = np.mean(a_lf, axis=0)
        g_s[cond_s][lvl] = np.std(a_f, axis=0)
        g_ls[cond_s][lvl] = np.std(a_lf, axis=0)

        for p in range(len(a_f2)):
            for q in range(len(a_f2[p])):
                a_cf[q].append(
                    np.array(sms.DescrStatsW(a_f2[p][q]).tconfint_mean())
                    )
                a_lcf[q].append(
                    np.array(sms.DescrStatsW(a_lf2[p][q]).tconfint_mean())
                    )
        g_cf[cond_s][lvl] = a_cf
        g_lcf[cond_s][lvl] = a_lcf
        print(f'strf {cond}: {lvl} is finished')
    print(f'strf {cond} is finished')

# # strf average
#
# g_l['a_strf'] = {}
# g_t['a_strf'] = {}
# g_f['a_strf'] = {}
# g_lf['a_strf'] = {}
#
# for i in range(len(lv)):
#     a_l = []
#     a_t = []
#     a_lf = []
#     a_f = []
#     lvl = lv[i]
#     g_l['a_strf'][lvl] = {}
#     g_t['a_strf'][lvl] = {}
#     g_f['a_strf'][lvl] = {}
#     g_lf['a_strf'][lvl] = {}
#
#     for j in file_input:
#
#         with h5py.File(j, 'r') as dat:
#             datas = dat
#             if not np.any(datas['tsp']['a_strf'][lvl]):
#                 print('skip')
#                 continue
#             else:
#                 dats = [
#                         np.array(datas['lfp']['a_strf'][lvl]),
#                         np.array(datas['tsp']['a_strf'][lvl]),
#                         np.array(datas['fpl']['a_strf'][lvl]),
#                         np.array(datas['fpt']['a_strf'][lvl])
#                        ]
#                 a_l.append(dats[0])
#                 a_t.append(dats[1])
#                 a_lf.append(dats[2])
#                 a_f.append(dats[3])
#
#     g_l['a_strf'][lvl] = np.mean(a_l, axis=0)
#     g_t['a_strf'][lvl] = np.mean(a_t, axis=0)
#     g_f['a_strf'][lvl] = np.mean(a_f, axis=0)
#     g_lf['a_strf'][lvl] = np.mean(a_lf, axis=0)
#     print(f'a_strf :{lvl} is finished')
# print(f'a_strf is finished')

'''
NN continuous
'''

for cond in nnc.conds:
    g_l[cond] = {}
    g_t[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    g_s[cond] = {}
    g_cf[cond] = {}
    g_ls[cond] = {}
    g_lcf[cond] = {}
    for i in range(len(lv)):
        a_l = []
        a_t = []
        a_lf = []
        a_f = []
        a_cf = [[] for _ in range(16)]
        a_lcf = [[] for _ in range(16)]

        lvl = lv[i]
        g_l[cond][lvl] = {}
        g_t[cond][lvl] = {}
        g_f[cond][lvl] = {}
        g_lf[cond][lvl] = {}
        g_s[cond][lvl] = {}
        g_ls[cond][lvl] = {}
        g_cf[cond][lvl] = {}
        g_lcf[cond][lvl] = {}
        for j in acor[cond][i]:
            if np.isnan(j):
                continue
            else:
                with h5py.File(file_input[j], 'r') as dat:
                    datas = dat
                    dats = [
                        np.array(datas['lfp'][cond][lvl]),
                        np.array(datas['tsp'][cond][lvl]),
                        np.array(datas['fpl'][cond][lvl]),
                        np.array(datas['fpt'][cond][lvl])
                        ]
                    a_l.append(dats[0])
                    a_t.append(dats[1])
                    a_lf.append(dats[2])
                    a_f.append(dats[3])
        a_f2 = np.transpose(a_f)
        a_lf2 = np.transpose(a_lf)

        g_l[cond][lvl] = np.mean(a_l, axis=0)
        g_t[cond][lvl] = np.mean(a_t, axis=0)
        g_f[cond][lvl] = np.mean(a_f, axis=0)
        g_lf[cond][lvl] = np.mean(a_lf, axis=0)
        g_s[cond][lvl] = np.std(a_f, axis=0)
        g_ls[cond][lvl] = np.std(a_lf, axis=0)

        for p in range(len(a_f2)):
            for q in range(len(a_f2[p])):
                a_cf[q].append(
                    np.array(sms.DescrStatsW(a_f2[p][q]).tconfint_mean())
                    )
                a_lcf[q].append(
                    np.array(sms.DescrStatsW(a_lf2[p][q]).tconfint_mean())
                    )
        g_cf[cond][lvl] = a_cf
        g_lcf[cond][lvl] = a_lcf

        print(f'{cond}: {lvl} is finished')
    print(f'{cond} is finished')


'''
NN on-off
'''

for cond in nns.conds:
    g_l[cond] = {}
    g_t[cond] = {}
    g_f[cond] = {}
    g_lf[cond] = {}
    g_s[cond] = {}
    g_cf[cond] = {}
    g_ls[cond] = {}
    g_lcf[cond] = {}
    for i in range(len(lv)):
        # notch on
        a_ln = []
        a_tn = []
        a_lfn = []
        a_fn = []
        a_cfn = [[] for _ in range(16)]
        a_lcfn = [[] for _ in range(16)]
        # notch off
        a_ls = []
        a_ts = []
        a_lfs = []
        a_fs = []
        a_cfs = [[] for _ in range(16)]
        a_lcfs = [[] for _ in range(16)]

        lvl = lv[i]
        g_l[cond][lvl] = {}
        g_t[cond][lvl] = {}
        g_f[cond][lvl] = {}
        g_lf[cond][lvl] = {}
        g_s[cond][lvl] = {}
        g_ls[cond][lvl] = {}
        g_cf[cond][lvl] = {}
        g_lcf[cond][lvl] = {}
        for j in acor[cond][i]:
            if np.isnan(j):
                continue
            else:
                with h5py.File(file_input[j], 'r') as dat:
                    datas = dat
                    datn = [
                        np.array(datas['lfp'][cond]['nn'][lvl]),
                        np.array(datas['tsp'][cond]['nn'][lvl]),
                        np.array(datas['fpl'][cond]['nn'][lvl]),
                        np.array(datas['fpt'][cond]['nn'][lvl])
                        ]

                    dats = [
                        np.array(datas['lfp'][cond]['si'][lvl]),
                        np.array(datas['tsp'][cond]['si'][lvl]),
                        np.array(datas['fpl'][cond]['si'][lvl]),
                        np.array(datas['fpt'][cond]['si'][lvl])
                        ]

                    a_ln.append(datn[0])
                    a_tn.append(datn[1])
                    a_lfn.append(datn[2])
                    a_fn.append(datn[3])

                    a_ls.append(dats[0])
                    a_ts.append(dats[1])
                    a_lfs.append(dats[2])
                    a_fs.append(dats[3])

        a_fn2 = np.transpose(a_fn)
        a_lfn2 = np.transpose(a_lfn)
        a_fs2 = np.transpose(a_fs)
        a_lfs2 = np.transpose(a_lfs)

        g_l[cond][lvl] = [np.mean(a_ln, axis=0), np.mean(a_ls, axis=0)]
        g_t[cond][lvl] = [np.mean(a_tn, axis=0), np.mean(a_ts, axis=0)]
        g_f[cond][lvl] = [np.mean(a_fn, axis=0), np.mean(a_fs, axis=0)]
        g_lf[cond][lvl] = [np.mean(a_lfn, axis=0), np.mean(a_lfs, axis=0)]
        g_s[cond][lvl] = [np.std(a_fn, axis=0), np.std(a_fs, axis=0)]
        g_ls[cond][lvl] =[np.std(a_lfn, axis=0), np.std(a_lfs, axis=0)]

        for p in range(len(a_fn2)):
            for q in range(len(a_fn2[p])):
                a_cfn[q].append(
                    np.array(sms.DescrStatsW(a_fn2[p][q]).tconfint_mean())
                    )
                a_lcfn[q].append(
                    np.array(sms.DescrStatsW(a_lfn2[p][q]).tconfint_mean())
                    )
                a_cfs[q].append(
                    np.array(sms.DescrStatsW(a_fs2[p][q]).tconfint_mean())
                    )
                a_lcfs[q].append(
                    np.array(sms.DescrStatsW(a_lfs2[p][q]).tconfint_mean())
                    )
        g_cf[cond][lvl] = [a_cfn, a_cfs]
        g_lcf[cond][lvl] = [a_lcfn, a_lcfs]

        print(f'{cond}: {lvl} is finished')
    print(f'{cond} is finished')

groups = {'tsp': g_t, 'fpt': g_f, 'lfp': g_l, 'fpl': g_lf, 'ssd': g_s,
          'lsd': g_ls, 'scf': g_cf, 'lcf': g_lcf
          }

# with h5py.File(snakemake.output[0], 'w') as h:
#     for t in list(groups.keys()):
#         d1 = h.create_group(t)
#         for cond in s_conds:
#             d2 = d1.create_group(f'{cond}_strf')
#             for lvl in lv:
#                 d3 = d2.create_dataset(
#                     lvl, data=groups[t][f'{cond}_strf'][lvl])
#
#         for cond in nnc.conds:
#             d2 = d1.create_group(cond)
#             for lvl in lv:
#                 d3 = d2.create_dataset(
#                     lvl, data=groups[t][cond][lvl])
#
#         for cond in nns.conds:
#             d2 = d1.create_group(cond)
#             for lvl in lv:
#                 d3 = d2.create_dataset(
#                     lvl, data=groups[t][cond][lvl])
