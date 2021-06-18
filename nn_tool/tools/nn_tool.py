import os
import sys

sys.path.insert(1, os.getcwd())

import scipy.signal as scig
import numpy as np
# import spike_tools as st
from parameter import parameters as pm
import sys
import quantities as pq
from scipy import stats
import statsmodels.stats.weightstats as sms
from tools import icsd
import neo.core
sys.path.pop(1)

# time index for notched noise. in[0] is the lower boundary and in[1] is
# the higher boundary.

in31 = pm.Nn.nn_i['nn31']
in11 = pm.Nn.nn_i['nn11']
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
crl = val.values()[7]
sets = val.extra_setup()
finx = [sets[3][1], sets[3][3]]
sr_lfp = 1061.5 * pq.Hz  # lfp sampling rate

# smoothing filter using hanning window
filt = np.hanning(5)


def index_spike(tsp):
    """
    :param tsp: just raw spk data from tsp file
    :return: spike train
    """
    mua = []

    for i in range(16):
        mua.append(np.zeros(181 * 1000 + 1))
        for k in range(np.size(tsp[i])):
            k1 = int(np.round(1000 * tsp[i][k]))
            if k1 > 181 * 1000:
                break
            elif k1 != 0:
                mua[i][k1] = 1
    return mua

def threshold_collect(data, ti, tf, t_off):
    """
    :param data: data of noise condition spikes with either 3/1 or 1/1 condition
    :param ti: t_i list for a session
    :param tf: tf list for a session
    :param t_off: offset phase start point for each subsession
    :return: mean and std of baseline to calculate threshold
    """
    ths = []
    data = np.array(data)
    trf = [150, 50]  # time points to calculate reference session range

    for i in range(len(ti)):
        t_i = ti[i] + t_off + trf[0]
        t_f = tf[i] - trf[1]
        ths.append(data[:, t_i:t_f])
    base = np.concatenate(ths, axis=1)
    return base


def psth(mua, indt):
    """
    :param mua: spike train from index_spike
    :param indt: type of index. depending on 3s/1s or 1s/1s on-off condition.
    :return: n_raster: data array you can use for raster plot. each channel
    has 4 s spike train with certain repetition ( 3s/1s # 45, 1s/1s # 90)
             n_psth: data array for psth. It's the sum of all repetition.
             s_psth: filtered data. Used convolution moving average, hanning
                     window for smoothing and averaged with repetition number.
             t_n: time array for generating plot.
    """
    n_raster = [[] for _ in range(16)]
    n_psth = []
    s_psth = []

    if indt in ['nn_3_1', 'nn_wn_3_1', 'nn_3_1_nt', 'nn_wn_3_1_nt']:
        ind = in31
        t_n = np.arange(0, 4001)

    elif indt in ['nn_1_1', 'nn_wn_1_1', 'nn_1_1_nt', 'nn_wn_1_1_nt']:
        ind = in11
        t_n = np.arange(0, 2001)

    else:
        print('somthing is wrong. check if you choose the right index type '
              'for nn condition.')
        sys.exit()

    rep = np.size(ind[0])

    for i in range(16):
        n_raster[i] = []

        for j in range(rep):
            # session of nn/wn  file with 4000/2000 ms/session
            n_raster[i].append(mua[i][ind[0][j]:ind[1][j] + 1])

        sums = np.sum(n_raster[i], axis=0) / rep
        n_psth.append(sums)
        s_psth.append(np.convolve(filt / filt.sum(), n_psth[i],
                                  mode='same'))

    n_psth = n_psth * pq.ms ** (-1)
    n_psth.units = pq.s ** (-1)

    s_psth = s_psth * pq.ms ** (-1)
    s_psth.units = pq.s ** (-1)

    return n_raster, n_psth, s_psth, t_n


def lfp_seg(lfp, indt):
    l_seg = [[] for _ in range(16)]
    rep = 0

    if indt in ['nn_3_1', 'nn_wn_3_1', 'nn_3_1_nt', 'nn_wn_3_1_nt']:
        ind = in31

    elif indt in ['nn_1_1', 'nn_wn_1_1', 'nn_1_1_nt', 'nn_wn_1_1_nt']:
        ind = in11
    else:
        print('something is wrong with choosing time index.')
        sys.exit()

    rep = np.size(ind[0])
    ind_l = ind[0] * (sr_lfp / 1000)
    ind_h = (ind[1] + 101) * (sr_lfp / 1000)
    for i in range(16):  # number of channels
        d_lfp = lfp[i] * pq.microvolt
        d_lfp.units = pq.mV
        for j in range(rep):
            l_seg[i].append(d_lfp[np.int(ind_l[j]): np.int(ind_h[j])])
    return l_seg


def lfp_index(t):
    inds = np.int(np.round(t * (sr_lfp / 1000)))
    return inds

def lfp_index_nnm(t1, t2=0, types=0):
    sr = sr_lfp / pq.Hz
    if types == 0:

        inds = np.int(np.round(t1 * (sr / 1000)))
    elif types == 1:

        inds = int(np.round(
            t1 * (sr / 1000) + int((t2 * sr / 1000))
            ))
    else:
        print("you didn't choose the right types")
        raise
    return inds

def m_spectro(l_seg):
    """

    :param l_seg: data array from lfp_seg
    :return: f: frequency array from spectrogram
             t: time array from spectrogram
             sx_mean: mean value of spectrogram intensity
             sx_m_log: mean value of spectrogram log intensity
    """

    sx_mean = []
    f = []
    t = []
    sx_m_log = []
    for i in range(len(l_seg)):
        sx_a = []
        sx_l = []
        rep = len(l_seg[i])
        for j in range(rep):
            f1, t1, sxr = scig.spectrogram(l_seg[i][j], sr_lfp,
                                           window=scig.hann(172), nperseg=172)
            sx = (sxr - np.min(sxr)) / (np.max(sxr) - np.min(sxr))  # scaling
            sxl = (np.log10(sxr + 1) - np.min(np.log10(sxr + 1))) / \
                  (np.max(np.log10(sxr + 1)) - np.min(np.log10(sxr + 1)))
            # scaling log
            sx_a.append(sx)
            sx_l.append(sxl)
            if j == rep - 1:
                f.append(f1)
                t.append(t1)

        sx_mean.append(np.mean(sx_a, axis=0))
        sx_m_log.append(np.mean(sx_l, axis=0))
    return f, t, sx_mean, sx_m_log


def spect_plot(ax, t, f, sig, images, xticks, yticks):
    im = ax.pcolormesh(t, f, sig,
                       cmap='rainbow',
                       edgecolors='none', shading='flat')
    images.append(im)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.set_yticks(yticks)
    ax.set_xticks(xticks[0])
    # ax.set_yticks(yticks[1], minor=True)
    ax.set_xticks(xticks[1], minor=True)
    ax.tick_params(axis='both', which='major', labelsize=8, length=2.5,
                   width=0.5)
    ax.tick_params(axis='both', which='minor', labelsize=8, length=0.9,
                   width=0.25)


def psth_plot(ax, t, spikes, xticks, yticks, c_type):
    """

    :param ax: axis of a plot/subplo
    :param t: time array
    :param spikes: spike number array
    :param xticks: array for the xtick
    :param yticks: array for the ytick
    :param s_max: maximum value of the spike number in all 16 channels
    :param c_type: 'nn' or 'wn' to choose the line color
    :return:
    """

    if c_type == 'nn_3_1' or c_type == 'nn_1_1':
        c_line = crl[0]
    elif c_type == 'nn_wn_3_1' or c_type == 'nn_wn_1_1':
        c_line = crl[1]
    else:
        print('something is wrong with psth_plot in nn_tools')
        sys.exit()

    ax.plot(t / 1000, spikes, lw=1, color=c_line, alpha=0.8)
    ax.set_yticks(yticks)
    ax.set_xticks(xticks)


def lfp_plot(ax, t, lfp, conf, xticks, yticks, c_type):
    """
    :param ax: axis of a plot/subplo
    :param t: time array
    :param lfp: averaged lfp
    :param conf: confidence interval of lfp
    :param xticks: array for the xtick
    :param yticks: array for the ytick
    :param c_type: 'nn' or 'wn' to choose the line color
    :return:
    """

    if c_type == 'nn_3_1' or c_type == 'nn_1_1':
        c_line = crl[0]
    elif c_type == 'nn_wn_3_1' or c_type == 'nn_wn_1_1':
        c_line = crl[1]
    else:
        print('something is wrong with lfp_plot nn_tools')
        sys.exit()
    lfp = lfp
    conf1 = np.transpose(conf)

    ax.plot(t / 1000, lfp, lw=1, color=c_line, alpha=0.8)
    ax.fill_between(
        t / 1000,
        conf1[0],
        conf1[1],
        alpha=.2
        )
    ax.set_yticks(yticks)
    ax.set_xticks(xticks)


def setups(cond):
    if cond == 'nn_3_1':
        names = ['nn_3_1', 'nn_wn_3_1']
        tmax = 4100
        nn_title = 'NN On 3 s/ Off 1 s'
        wn_title = 'WN On 3 s/ Off 1 s'

    elif cond == 'nn_1_1':
        names = ['nn_1_1', 'nn_wn_1_1']
        tmax = 2100
        nn_title = 'NN On 1 s/ Off 1 s'
        wn_title = 'WN On 1 s/ Off 1 s'
    else:
        print('something is wrong. check nn31/11_psth_lfp_plot.py')
        sys.exit()
    return names, tmax, nn_title, wn_title


def freq_find(data, find, type='spk'):
    """

    :param data: frequency profile type data
    :param find: index for edges of notch frequencies
    :param type: spk/lfp
    :return: max activity freq index within notch
    """
    fi = find[0]
    ff = find[1] + 1

    if type == 'spk':
        d_max = np.max(data[fi:ff])
        ind = [i for i, x in enumerate(data) if x == d_max and fi <= i < ff][0]

    elif type == 'lfp':
        d_min = np.min(data[fi:ff])
        ind = [i for i, x in enumerate(data) if x == d_min and fi <= i < ff][0]

    else:
        print("you did not choose the data type. Choose either 'spk' or "
              "'lfp'.")
        raise ValueError

    return ind


def layer_mean(data, layer, type='spk', cond='3_1'):
    """
    Actually, this returns quartile and median of input data.

    :param data: data of each condition. e.g. nn_3_1 data
    :param layer: specific layer name you want to choose e.g. supr, gran,
    infr for supragranular, granular, and infragranular layer
    :param type: the data type you are processing: 'spk' or 'lfp'
    :return: the list contains quartile values ([lower, upper]), max peak
    value, the index of the max peak value
    """
    """
    I changed np.where to np.argwhere. check if this works ok
    """
    med = np.median(data[layer], axis=0)  # average spk/lfp
    quar2 = np.percentile(data[layer], 25, axis=0)
    quar7 = np.percentile(data[layer], 75, axis=0)

    """
    offset peaks appear within 100 ms from start of offset phase. So I 
    choose between 3000 - 3100 ms window to find the max peak

    """
    ti = 0
    tf = 0
    p_ind = 0
    peak = 0

    if cond == '3_1':
        if type == 'spk':
            ti = 3000
            tf = 3101
            peak = np.max(med[ti:tf])  # peak value
            p_ind = [x for x in np.argwhere(med == peak) if 3000 < x <
                     3101][0]

        elif type == 'lfp':
            ti = lfp_index(3000)
            tf = lfp_index(3101)
            p_min = np.min(med[ti:tf])  # peak value
            p_max = np.max(med[ti:tf])  # baseline value
            peak = np.abs(p_max - p_min)  # peak to peak

            p_ind = [x for x in np.argwhere(med == p_min) if ti < x < tf][0]

        else:
            print("you forgot to add a type of your data")
        # p_ind, ind of offset peak: for finding quartile value at max peak time
        # point.
    elif cond == '1_1':
        if type == 'spk':
            ti = 1000
            tf = 1101
            peak = np.max(med[ti:tf])  # peak value
            p_ind = [x for x in np.argwhere(med == peak) if 3000 < x < 3101][0]

        elif type == 'lfp':
            ti = lfp_index(1000)
            tf = lfp_index(1101)
            p_min = np.min(med[ti:tf])  # peak value
            p_max = np.max(med[ti:tf])  # baseline value
            peak = np.abs(p_max - p_min)  # peak to peak

            p_ind = [x for x in np.argwhere(med == p_min) if ti < x < tf][0]

        else:
            print("you forgot to add a type of your data")
        # p_ind, ind of offset peak: for finding quartile value at max peak time
        # point.

    return [quar2[p_ind], quar7[p_ind]], peak, p_ind


def p_to_p(ctrl, nn, cbase, nbase, ind):
    """
    :param ctrl: data array of congrol
    :param nn:  data array of notched noise
    :return: difference ratio to ctrl
    """
    pc = np.abs(ctrl[ind] - cbase[ind])
    pn = np.abs(nn[ind] - nbase[ind])

    diff = (pn - pc) / pc
    # if ctrl[ind] != np.max(ctrl):
    #     pc = np.abs(ctrl[ind] - np.max(ctrl))
    # elif ctrl[ind] == np.max(ctrl):
    #     pc = np.abs(ctrl[ind] - ctrl[ind - 1])
    #
    # if nn[ind] != np.max(nn):
    #     pn = np.abs(nn[ind] - np.max(nn))
    # elif nn[ind] == np.max(nn):
    #     pn = np.abs(nn[ind] - nn[ind - 1])

    return diff


def diff(data, layer, lv, cn, cs, ind=None, bdata=None, types='spk',
         fqtype='center'):
    """

    :param data: frequency profile data
    :param bdata: baseline data for lfp frequency profile
    :param layer: layer name (string)
    :param lv: lv name (string)
    :param cn: name of nnm condition
    :param cs: name ofstrf for nnm condition
    :param ind: index of the frequency you want to calculate
    :param types: type of the data: 'spk', 'lfp'
    :param fqtype: type of the frequency of interest: 'edge', 'center'
    :return: median value of that specific layer, level, frequecny
    """
    global tempm, tempe2, tempe7
    tempc = data[cs][layer][lv]
    tempn = data[cn][layer][lv]

    tempr = []
    meann = []
    if fqtype == 'edge':
        for ani in range(len(tempn)):
            if types == 'spk':
                tempr.append(
                    (tempn[ani][ind] - tempc[ani][ind]) / tempc[ani][ind])
            elif types == 'lfp':
                tembc = bdata[cs][layer][lv]
                tembn = bdata[cn][layer][lv]
                tempr.append(
                    p_to_p(tempc[ani], tempn[ani], tembc[ani], tembn[ani], ind)
                    )
            else:
                print("you forgot to indicate which kind of data it is")
                raise ValueError

        tempm = np.median(np.array(tempr), axis=0)  # temp for
        # median

        tempe2 = np.percentile(np.array(tempr), 25, axis=0)  # temp for
        # quartile, 0.25
        tempe7 = np.percentile(np.array(tempr), 75, axis=0)  # temp for
        # quartile, 0.75
        return tempm, tempe2, tempe7, tempr

    elif fqtype == 'center':
        find = finx
        fm = []
        if types == 'spk':
            for ani in range(len(tempn)):
                fm.append(freq_find(tempn[ani], find))

            for ani in range(len(tempn)):
                tempr.append(
                    (tempn[ani][fm[ani]] - tempc[ani][fm[ani]])
                    / tempc[ani][fm[ani]]
                    )

        elif types == 'lfp':
            for ani in range(len(tempn)):
                fm.append(freq_find(tempn[ani], find, type='lfp'))

            for ani in range(len(tempn)):
                tembc = bdata[cs][layer][lv]
                tembn = bdata[cn][layer][lv]
                tempr.append(
                    p_to_p(tempc[ani], tempn[ani], tembc[ani],
                           tembn[ani], fm[ani])
                    )
        else:
            print("you forgot to indicate which kind of data it is")
            raise ValueError

        tempm = np.median(np.array(tempr), axis=0)  # temp for
        # median

        tempe2 = np.percentile(np.array(tempr), 25, axis=0)  # temp for
        # quartile, 0.25
        tempe7 = np.percentile(np.array(tempr), 75, axis=0)  # temp for
        # quartile, 0.75
        return tempm, tempe2, tempe7, tempr


def diff_on_off(data, layer, lv, cn, cs, cnon, bdata=None, types='spk'):
    """

    :param data: frequency profile data
    :param bdata: baseline data for lfp frequency profile
    :param layer: layer name (string)
    :param lv: lv name (string)
    :param cn: name of nnm condition
    :param cs: name of control for nnm condition
    :param cnon: name of nn-on to find max/min freq ind
    :param types: type of the data: 'spk', 'lfp'
    :return: median value of that specific layer, level, frequecny
    """
    global tempm, tempe2, tempe7
    tempc = data[cs][layer][lv]
    tempn = data[cn][layer][lv]
    dnon = data[cnon][layer][lv]
    tempr = []
    meann = []

    find = finx
    fm = []
    if types == 'spk':
        for ani in range(len(dnon)):
            fm.append(freq_find(dnon[ani], find))

        for ani in range(len(tempn)):
            tempr.append(
                (tempn[ani][fm[ani]] - tempc[ani][fm[ani]])
                / tempc[ani][fm[ani]]
                )
    elif types == 'lfp':
        for ani in range(len(dnon)):
            fm.append(freq_find(dnon[ani], find, type='lfp'))

        for ani in range(len(tempn)):
            tembc = bdata[cs][layer][lv]
            tembn = bdata[cn][layer][lv]
            tempr.append(
                p_to_p(tempc[ani], tempn[ani], tembc[ani],
                       tembn[ani], fm[ani])
                )
    else:
        print("you forgot to indicate which kind of data it is")
        raise ValueError

    tempm = np.median(np.array(tempr), axis=0)  # temp for
    # median

    tempe2 = np.percentile(np.array(tempr), 25, axis=0)  # temp for
    # quartile, 0.25
    tempe7 = np.percentile(np.array(tempr), 75, axis=0)  # temp for
    # quartile, 0.75
    temci = sms.DescrStatsW(np.array(tempr)).tconfint_mean()

    return tempm, tempe2, tempe7, temci, tempr


def layer_average(data, layer_number):
    """
    :param data: data you want to process to have layer-wise average
    :param layer_number: start-end point list of each layer
    :return: layer-wise averaged list
    """
    layer = [
        data[layer_number[0][0]:layer_number[0][1]],
        data[layer_number[1][0]:layer_number[1][1]],
        data[layer_number[2][0]:layer_number[2][1]]
        ]
    l_average = [
        np.mean(layer[0], axis=0),
        np.mean(layer[1], axis=0),
        np.mean(layer[2], axis=0)]

    return l_average


def fp_wilcoxon(data, find, type='center'):
    if type == 'edge':
        dat = [np.transpose(data[0])[find], np.transpose(data[1])[find]]
        test = stats.wilcoxon(dat[0], dat[1])
        return [find, test[1]]

    elif type == 'center':
        datc = []
        datn = []

        for i in range(len(find)):
            f = find[i]
            datc.append(data[0][i][f])
            datn.append(data[1][i][f])
        test = stats.wilcoxon(datc, datn)

        return [12, test[1], test[0]]


def fp_friedman(data, find):
    datc = []
    datnn = []
    datnf = []
    datwf = []

    for i in range(len(find)):
        f = find[i]
        datc.append(data[0][i][f])
        datnn.append(data[1][i][f])
        datnf.append(data[2][i][f])
        datwf.append(data[3][i][f])
    test = stats.friedmanchisquare(datc, datnn, datnf, datwf)

    return [12, test[1]]


def dat_unit(data, types='lfp'):
    if types == 'lfp':
        data = data * pq.microvolt
        data.units = pq.mV
    elif types == 'spk':
        data = data * pq.ms ** (-1)
        data.units = pq.s ** (-1)
    elif types == 'csd':
        data = data * pq.mV / (pq.mm ** 2)
    else:
        print('You did not choose a type of data')
        raise ValueError

    return data


def nn_threshold(data, t_ind, ratio, types):
    m = np.mean(data[t_ind[0]:t_ind[1] + 1])
    sd = np.std(data[t_ind[0]:t_ind[1] + 1])

    if types == 'spk':
        thr = m + ratio * sd
    elif types == 'lfp':
        thr = m - ratio * sd
    else:
        print('there is something wrong. you may not choose types of the data')
        raise ValueError

    return thr


def noise_sep(data, time_on, time_off, types):
    if types == 'lfp':
        t_on = [lfp_index(time_on[0]), lfp_index(time_on[1])]
        t_off = [lfp_index(time_off[0]), lfp_index(time_off[1])]
    elif types == 'spk':
        t_on = time_on
        t_off = time_off
    else:
        print('something is wrong with -on_off_seperate-')
        raise ValueError

    g_on = []
    g_off = []
    for i in range(len(data)):
        g_on.append(data[i][t_on[0]:t_on[1]])
        g_off.append(data[i][t_off[0]:t_off[1]])

    return g_on, g_off


def nn_csd(data):
    coord = np.arange(0, 1501, 100) * pq.micrometer
    sigma = 1 / (100 * pq.micrometer)
    data = data * pq.mV
    lfp_data = neo.core.AnalogSignal(data.T, sampling_rate=sr_lfp)

    lfp_input = {
        'lfp': lfp_data,
        'coord_electrode': coord,
        'sigma': sigma,
        'f_type': 'gaussian',
        'f_order': (3, 1)
        }

    fil_csd = icsd.estimate_csd(**lfp_input)[1]
    csd = np.transpose(fil_csd / fil_csd.units) * fil_csd.units
    csd.units = pq.mV / (pq.mm ** 2)

    return csd