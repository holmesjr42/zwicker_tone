import os
import sys
import scipy.io as spio

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms

sys.path.pop(1)

'''
trying to check noise frequency
'''
sr_lfp = 1061.5

d = np.load(
    '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021'
    '/data/dataset/raw/cl119_210401/'
    'lfp_01-Apr-2021-17-TC_500_32000_0.125_30_10.npy', allow_pickle=True
    )

tf = 180000  # 3 min, ms
tf2 = np.int(np.round(tf * sr_lfp / 1000))

for i in range(16):
    dat = np.concatenate(d[i][0:tf2])
    t = np.linspace(0, tf, tf2, endpoint=True)
    dat2 = dat[154979:160286]
    t2 = t[154979:160286]
    # ind = [i for i, x in enumerate(t) if x > 151000 and x < 151001]
    # print(ind)
    # plt.figure()
    # plt.plot(t, dat)
    # plt.show()
    # plt.show()
    fft = np.fft.rfft(dat2)
    abs_fft = np.abs(fft)
    pspectrum = np.square(abs_fft)
    freq = np.linspace(0, sr_lfp/2, len(pspectrum))

    p_ind = np.where(pspectrum == np.max(pspectrum))

    print(i, freq[p_ind])

# dat = np.concatenate(d[12][0:tf2])
# t = np.linspace(0, tf, tf2, endpoint=True)
# dat2 = dat[154979:160286]
# t2 = t[154979:160286]
# ind = [i for i, x in enumerate(t) if x > 146000 and x < 146001]
# print(ind)
# plt.figure()
# plt.plot(t, dat)
# plt.show()

# fft = np.fft.rfft(dat2)
# abs_fft = np.abs(fft)
# pspectrum = np.square(abs_fft)
# freq = np.linspace(0, sr_lfp/2, len(pspectrum))
#
# p_ind = np.where(pspectrum == np.max(pspectrum))
# plt.plot(freq, pspectrum)
#
# plt.show()