import numpy as np
# from scipy import stats
import statsmodels.stats.api as sms
from tools import nn_tool as nt
import scipy.signal as ss
# import scipy.fftpack as ft

'''
spike train

 - making binary spike train array
 - time_snip is Tsp in mat file
'''


def index_strf(time_snip):
    mua = []
    for i in range(16):
        mua.append(np.zeros(181 * 1000 + 1))
        for k in range(np.size(time_snip[i])):
            k1 = int(np.round(1000 * time_snip[i][k]))
            if k1 > 181 * 1000:
                break
            elif k1 > 0:
                mua[i][k1] = 1
    return mua

def smooth(data, f_order, f_type='hanning'):
    """

    :param data: the input signal
    :param f_order: dimension of the sliding window
    :param f_type: window type
    :return: the smoothed signal
    """
    if data.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays")

    if f_type == 'gaussian':
        f_dim = len(f_order)
    else:
        f_dim = f_order

    if len(data) < f_dim:
        raise ValueError("Input vector needs to be bigger than window size")
    if f_dim < 3:
        print("No smoothing working with window size less than 3")
        return data
    if not f_type in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window should be one of 'flat', 'hanning', "
                         "'hamming', 'barlett', or 'blackman'")

    if f_type == 'boxcar':
        num = ss.boxcar(f_order)
        denom = np.array([num.sum()])
    elif f_type == 'hamming':
        num = ss.hamming(f_order)
        denom = np.array([num.sum()])
    elif f_type == 'hanning':
        num = ss.hanning(f_order)
        denom = np.array([num.sum()])
    elif f_type == 'triangular':
        num = ss.triang(f_order)
        denom = np.array([num.sum()])
    elif f_type == 'gaussian':
        num = ss.gaussian(f_order[0], f_order[1])
        denom = np.array([num.sum()])
    elif f_type == 'identity':
        num = np.array([1.])
        denom = np.array([1.])
    elif f_type == 'flat':
        num = np.ones(f_order, 'd')
        denom = np.array([num.sum()])
    else:
        print('%s Wrong filter type!' % f_type)
        raise

    procd = ss.convolve(data, num / denom.sum(), 'same')

    return procd

'''
tsp

averaging the number of spikes
 - p_info = parameter_info = time_index; mua, spike train binary arrays from
 - index_strf; twi, ms, initial point of time window for activated area in
 - 100 ms
 - window from a stimulus trigger point; twf, ms, final point of time window
 - from twi; tsp_m, spks,  average of each frequency activity in 100 ms time
 - window;,
 - avg, spike density function, average of each frequency activity through 
   activation time window
'''


# def tsp_strf(p_info, mua, twi=19, twf=50):
#     tsp_m = [[] for _ in range(16)]
#     tsp_f = [[] for _ in range(16)]
#     avg = [[] for _ in range(16)]
#     std = [[] for _ in range(16)]  # standard deviation for frequency profile
#     conf = [[] for _ in range(16)]  # confidence interval for frequency profile
#     for i in range(16):
#         tsp_m[i] = [[] for _ in range(49)]
#         tsp_f[i] = [[] for _ in range(49)]
#         for j in range(49):
#             for k in range(len(p_info[j]) - 1):
#                 tsp_f[i][j].append(mua[i][(int(np.floor(p_info[j][k]))):(int(
#                     np.floor(p_info[j][k])) + 101)])
#
#             tsp_m[i][j] = np.append(tsp_m[i][j], np.mean(tsp_f[i][j], axis=0))
#             avg[i] = np.append(avg[i], np.mean(tsp_m[i][j][twi:twf + 1]))
#             std[i] = np.append(
#                                std[i],
#                                np.std(tsp_m[i][j][twi:twf + 1], ddof=1)
#                               )
#             conf[i].append(
#                 np.array(
#                     sms.DescrStatsW(tsp_m[i][j][twi:twf + 1]).tconfint_mean()
#                     )
#                 )
#     return [tsp_m, avg, std, conf]

def tsp_strf(p_info, mua, twi=19, twf=50, tmi=10, tmf=40):
    """

    :param p_info: tone pip time onset information
    :param mua: mua data array
    :param twi: time window initial for frequency profile average
    :param twf: time window final for frequency profile average
    :param tmi: time window initial for frequency profile average with max val
    :param tmf: time window final for frequency profile average with max val
    :return: ave spike, frequency profile, standard deviation, confidence
    interval, frequency profile with max val
    """
    tsp_m = [[] for _ in range(16)]  # temporal spike data
    avg = [[] for _ in range(16)]  # using mean for frequency profile
    std = [[] for _ in range(16)]  # standard deviation for frequency profile
    conf = [[] for _ in range(16)]  # confidence interval for frequency profile
    avg_2 = [[] for _ in range(16)]  # using max for frequency profile

    for i in range(16):
        tsp_m[i] = []
        for j in range(49):
            tsp_f = []
            for k in range(len(p_info[j]) - 1):
                tsp_f.append(
                    mua[i][(int(np.floor(p_info[j][k]))):
                           (int(np.floor(p_info[j][k])) + 101)]
                    )

            tsp_m[i].append(np.mean(tsp_f, axis=0))
            avg[i].append(np.mean(tsp_m[i][j][twi:twf + 1]))

            std[i].append(np.std(tsp_m[i][j][twi:twf + 1], ddof=1))
            conf[i].append(
                np.array(
                    sms.DescrStatsW(tsp_m[i][j][twi:twf + 1]).tconfint_mean()
                    )
                )

            # another frequency profile
            tsp_s = smooth(tsp_m[i][j], f_order=3, f_type='hamming')
            avg_2[i] = np.append(avg_2[i], np.max(tsp_s[tmi:tmf + 1]))

    return [tsp_m, avg, std, conf, avg_2]


'''
lfp

 - averaging lfp
 - p_info = parameter_info = time_index; mua, spike train binary arrays from
 - index_strf; twi, ms, initial point of time window for activated area in
 - 100 ms
 - window from a stimulus trigger point; twf, ms, final point of time window
 - from twi; tsp_m, mV,  average of each frequency voltage in 100 ms time
 - window;,
 - avg, mV/ms, average of each frequency activity through activation time 
   window. What do I call them? Voltage density function?
'''


# def lfp_strf(p_info, lfp, tw=100, twi=19, twf=50):
#     sr_lfp = 1061.5  # sampling rate
#     lfp_m = [[] for _ in range(16)]  # temporal lfp data
#     lfp_f = [[] for _ in range(16)]
#     avg = [[] for _ in range(16)]  # frequency profile
#     std = [[] for _ in range(16)]  # standard deviation for frequency profile
#     conf = [[] for _ in range(16)]  # confidence interval for frequency profile
#     twi = int(twi * sr_lfp / 1000)
#     twf = int(twf * sr_lfp / 1000)
#     for i in range(16):
#         lfp_m[i] = [[] for _ in range(49)]
#         lfp_f[i] = [[] for _ in range(49)]
#         for j in range(49):
#             for k in range(len(p_info[j]) - 1):
#                 cut_l = int(np.round(p_info[j][k] * (sr_lfp / 1000)))
#                 cut_h = int(np.round((p_info[j][k]) * (sr_lfp / 1000) +
#                                      int(tw * sr_lfp / 1000)))
#
#                 lfp_f[i][j].append(lfp[i][cut_l:cut_h + 1])
#
#             lfp_m[i][j] = np.append(lfp_m[i][j], np.mean(lfp_f[i][j], axis=0))
#             avg[i] = np.append(avg[i], np.mean(lfp_m[i][j][twi:twf + 1]))
#             std[i] = np.append(
#                 std[i],
#                 np.std(lfp_m[i][j][twi:twf + 1], ddof=1)
#                 )
#             conf[i].append(
#                 np.array(
#                     sms.DescrStatsW(
#                         lfp_m[i][j][twi:twf + 1]
#                         ).tconfint_mean()
#                     )
#                 )
#     return [lfp_m, avg, std, conf]

def lfp_strf(
        p_info, lfp, tw=100, twi=19, twf=50, tmi=10, tmf=40, tbi=0, tbf=10
        ):
    """

    :param p_info: tone pip time onset information
    :param lfp: lfp data array
    :param tw: time window length for onset response
    :param twi: time window initial for frequency profile average
    :param twf: time window final for frequency profile average
    :param tmi: time window initial for frequency profile average with min val
    :param tmf: time window final for frequency profile average with min val
    :param tbi: time window initial for baseline
    :param tbf: time window final for baseline
    :return: ave spike, frequency profile, standard deviation, confidence
    interval, frequency profile with min val, baseline value for peak to peak
    """
    sr_lfp = 1061.5  # sampling rate
    lfp_m = [[] for _ in range(16)]  # temporal lfp data
    avg = [[] for _ in range(16)]  # frequency profile
    std = [[] for _ in range(16)]  # standard deviation for frequency profile
    conf = [[] for _ in range(16)]  # confidence interval for frequency profile
    avg_2 = [[] for _ in range(16)]  # using max for frequency profile
    base = [[] for _ in range(16)]  # baseline value to calculate peak to peak
    twi = nt.lfp_index(twi)
    twf = nt.lfp_index(twf)
    tmi = nt.lfp_index(tmi)
    tmf = nt.lfp_index(tmf)
    tbi = nt.lfp_index(tbi)
    tbf = nt.lfp_index(tbf)

    for i in range(16):
        lfp_m[i] = []
        for j in range(49):
            lfp_f = []
            for k in range(len(p_info[j]) - 1):
                cut_l = nt.lfp_index(p_info[j][k])
                cut_h = nt.lfp_index_nnm(p_info[j][k], t2=tw, types=1)

                lfp_f.append(lfp[i][cut_l:cut_h + 1])

            lfp_m[i].append(np.mean(lfp_f, axis=0))
            avg[i].append(np.mean(lfp_m[i][j][twi:twf + 1]))
            std[i].append(np.std(lfp_m[i][j][twi:twf + 1], ddof=1))
            conf[i].append(np.array(
                sms.DescrStatsW(lfp_m[i][j][twi:twf + 1]).tconfint_mean()
                    )
                )

            # another frequency profile
            tsp_s = smooth(lfp_m[i][j], f_order=3, f_type='hamming')
            avg_2[i] = np.append(avg_2[i], np.min(tsp_s[tmi:tmf + 1]))
            base[i] = np.append(base[i], np.max(tsp_s[tbi:tbf + 1]))

    return [lfp_m, avg, std, conf, avg_2, base]
