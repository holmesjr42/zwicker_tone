
######## Snakemake header ########
import sys; sys.path.extend(['/home/bhc/anaconda3/lib/python3.7/site-packages', '/home/bhc/codes/spike_snakemake/nnm_spike_lfp']); import pickle; snakemake = pickle.loads(b'\x80\x03csnakemake.script\nSnakemake\nq\x00)\x81q\x01}q\x02(X\x05\x00\x00\x00inputq\x03csnakemake.io\nInputFiles\nq\x04)\x81q\x05Xy\x00\x00\x00/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/nnm_spk_lfp_avg/cr33_190321_spk_lfp_avg_nnm.hdf5q\x06a}q\x07X\x06\x00\x00\x00_namesq\x08}q\tsbX\x06\x00\x00\x00outputq\ncsnakemake.io\nOutputFiles\nq\x0b)\x81q\x0c(Xy\x00\x00\x00/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/image/nnm_sp_lfp/spk/cr33_190321_nnm_1_1_spk.pngq\rXy\x00\x00\x00/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/image/nnm_sp_lfp/lfp/cr33_190321_nnm_1_1_lfp.pngq\x0eXy\x00\x00\x00/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/image/nnm_sp_lfp/fps/cr33_190321_nnm_1_1_fps.pngq\x0fXy\x00\x00\x00/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/image/nnm_sp_lfp/fpl/cr33_190321_nnm_1_1_fpl.pngq\x10e}q\x11h\x08}q\x12sbX\x06\x00\x00\x00paramsq\x13csnakemake.io\nParams\nq\x14)\x81q\x15}q\x16h\x08}q\x17sbX\t\x00\x00\x00wildcardsq\x18csnakemake.io\nWildcards\nq\x19)\x81q\x1aX\x0b\x00\x00\x00cr33_190321q\x1ba}q\x1c(h\x08}q\x1dX\x04\x00\x00\x00nameq\x1eK\x00N\x86q\x1fsX\x04\x00\x00\x00nameq h\x1bubX\x07\x00\x00\x00threadsq!K\x01X\t\x00\x00\x00resourcesq"csnakemake.io\nResources\nq#)\x81q$(K\x01K\x01e}q%(h\x08}q&(X\x06\x00\x00\x00_coresq\'K\x00N\x86q(X\x06\x00\x00\x00_nodesq)K\x01N\x86q*uh\'K\x01h)K\x01ubX\x03\x00\x00\x00logq+csnakemake.io\nLog\nq,)\x81q-}q.h\x08}q/sbX\x06\x00\x00\x00configq0}q1X\x04\x00\x00\x00ruleq2X\x0e\x00\x00\x00nnm_1_1_sp_lfpq3X\x0f\x00\x00\x00bench_iterationq4NX\t\x00\x00\x00scriptdirq5X-\x00\x00\x00/home/bhc/codes/spike_snakemake/nnm_spike_lfpq6ub.'); from snakemake.logging import logger; logger.printshellcmds = False; __real_file__ = __file__; __file__ = '/nnm_spike_lfp/nnm_1_1_off_sp_lfp.py';
######## Original script #########
import os
import sys

print(os.path.dirname(os.getcwd()))
sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
from parameters import parameters as pm
import seaborn as sns
import h5py

sys.path.pop(1)

'''
this is to process and generate a single data file for spikes and lfp 
data
'''
# sns.set_style("ticks")

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some adjustments for plots: channels you are going to use, wspace, hspace,
# colormap, min and max values for heatmap

# continuous nn
val = pm.Setup(cond='nnm_1_1', cond2='tsp', mode=1)
val2 = pm.Setup(cond='nnm_1_1', cond2='lfp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, ws, hs, ccmap, cct, cb = val.values()
ccl = val2.values()[10]  # color for notch borders
condl = 'lfp'
octs = com.octaves  # octave range for plotting
lvl = com.db['lv']  # SPLdB list
g_n1 = {}  # dict of lfp for nn-on condition
g_n0 = {}  # dict of lfp for nn-off condition
g_w1 = {}  # dict of lfp for wn-on condition
g_w0 = {}  # dict of lfp for wn-off condition
g_s = {}  # dict of lfp for strf condition
# dataset
# file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
#              '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
file_input = snakemake.input[0]
# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]

if animal == 'cr29' or animal == 'cr30':
    for i in snakemake.output:
        plt.figure()
        plt.savefig(i, dpi=150)
    sys.exit()
else:
    pass

# conditions for this script
c_n = 'nnm_1_1'
c_w = 'nnm_wn_1_1'
c_s = 'nnm_1_1_strf'
# loading data
with h5py.File(file_input, 'r') as dat:
    datas = dat

    if 'all' in animal:
        if '30' in list(datas['lfp'][c_s].keys()):
            for i in ['tsp', 'lfp', 'fpt', 'fpl']:
                datas[i][c_s].pop('30')

        else:
            pass

        if '30' in list(datas['lfp'][c_n].keys()):
            for i in ['tsp', 'lfp', 'fpt', 'fpl']:
                datas[i][c_n].pop('30')
        else:
            pass

    else:
        pass

        # aranging dataset
    sk = [datas['tsp'][c_n], datas['tsp'][c_s], datas['tsp'][c_w]]  # spk
    lp = [datas['lfp'][c_n], datas['lfp'][c_s], datas['lfp'][c_w]]  # lfp
    sa = [datas['fpt'][c_n], datas['fpt'][c_s], datas['fpt'][c_w]]  # spk_mean
    la = [datas['fpl'][c_n], datas['fpl'][c_s], datas['fpl'][c_w]]  # lfp_mean

    if 'cr' in animal:
        for i in lvl:
            g_s[i] = [np.array(sk[1][i]), np.array(lp[1][i]),
                      np.array(sa[1][i]), np.array(la[1][i])]
            g_n1[i] = [np.array(sk[0]['nn'][i]), np.array(lp[0]['nn'][i]),
                       np.array(sa[0]['nn'][i]), np.array(la[0]['nn'][i])]
            g_n0[i] = [np.array(sk[0]['si'][i]), np.array(lp[0]['si'][i]),
                       np.array(sa[0]['si'][i]), np.array(la[0]['si'][i])]
            g_w1[i] = [np.array(sk[2]['nn'][i]), np.array(lp[2]['nn'][i]),
                       np.array(sa[2]['nn'][i]), np.array(la[2]['nn'][i])]
            g_w0[i] = [np.array(sk[2]['si'][i]), np.array(lp[2]['si'][i]),
                       np.array(sa[2]['si'][i]), np.array(la[2]['si'][i])]

    elif 'all' in animal:
        for i in lvl:
            g_s[i] = [np.array(sk[1][i]), np.array(lp[1][i]),
                      np.array(sa[1][i]), np.array(la[1][i])]
            g_n1[i] = [np.array(sk[0][i][0]), np.array(lp[0][i][0]),
                       np.array(sa[0][i][0]), np.array(la[0][i][0])]
            g_n0[i] = [np.array(sk[0][i][1]), np.array(lp[0][i][1]),
                       np.array(sa[0][i][1]), np.array(la[0][i][1])]
            g_w1[i] = [np.array(sk[2][i][0]), np.array(lp[2][i][0]),
                       np.array(sa[2][i][0]), np.array(la[2][i][0])]
            g_w0[i] = [np.array(sk[2][i][1]), np.array(lp[2][i][1]),
                       np.array(sa[2][i][1]), np.array(la[2][i][1])]


# function for plotting

def plott(aax, dats, imag, cm=ccmap):
    aax.tick_params(axis='both', which='major', labelsize=6, length=0.9,
                    width=0.5)
    # aax.tick_params(axis='both', length=0.9, width=0.5)
    aax.spines['top'].set_visible(False)
    aax.spines['right'].set_visible(False)
    aax.spines['left'].set_visible(False)
    aax.spines['bottom'].set_visible(False)
    # aax.spines['bottom'].set_linewidth(0.5)
    # aax.spines['left'].set_linewidth(0.5)
    for tick in aax.get_xticklabels():
        tick.set_fontname('sans-serif')
    for tick in aax.get_yticklabels():
        tick.set_fontname('sans-serif')
    img = aax.imshow(
        dats, cmap=cm, aspect=100 / 3,
        extent=[0, 100, 1.5, -1.5], interpolation='gaussian')
    imag.append(img)
    # plt.subplots_adjust(wspace=.001)
    aax.set_xticks(np.linspace(0, 100, 5, endpoint=True), minor=True)
    aax.set_xticks(np.linspace(0, 100, 3, endpoint=True))
    # aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
    aax.set_yticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5])

    # axins = inset_axes(aax,
    #                    width="5%",  # width = 5% of parent_bbox width
    #                    height="100%",  # height : 50%
    #                    loc='lower left',
    #                    bbox_to_anchor=(20, 0., 1, 1),
    #                    bbox_transform=aax.transAxes,
    #                    borderpad=0,
    #                    )
    aax.label_outer()
    # return aax, axins


def cbar_t(cbar, type):
    cbar.ax.tick_params(labelsize=7)
    if type == 'lfp':
        cbar.set_label(
            r'mV',
            labelpad=15, size=9
            )

    elif type == 'tsp':
        cbar.set_label(
            'spk' + r's',
            labelpad=15, size=9
            )


def norm_color(img, type, ratio=0.7):
    if type == 'lfp' or type == 'tsp':
        vmin = min(ims.get_array().min() for ims in img) * ratio
        vmax = max(ims.get_array().max() for ims in img) * ratio
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        print('there is a problem with norm_color. check it')
        sys.exit()

    for ims in img:
        ims.set_norm(norm)


# plot setup
'''
nn on-off
'''

#  heatmap
# setup
c_img = []
# cx_ind = []
# # axinc = []
lvp = []  # spl list which actually has data
for i in range(len(lvl)):
    if not np.any(g_n1[lvl[i]][0]):
        continue
    else:
        lvp.append(lvl[i])

lv_off = [x for x in lvl if x not in lvp]

c1_fig = plt.figure(0, figsize=(16, 9), dpi=300)
# c1_fig.patch.set_facecolor(cct)

c1_axs1 = c1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.07, right=0.270,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))

c1_axs2 = c1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.3, right=0.50,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))
c1_axs3 = c1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.53, right=0.73,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))
c1_axs4 = c1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.76, right=0.96,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))

# axs1[0][0].set_title('hey''70')
c1_axs = {'70': c1_axs1, '60': c1_axs2, '50': c1_axs3, '40': c1_axs4}

# fig.suptitle('Multiple images')

for j in lvp:
    for i in range(len(ch)):
        tspc = g_s[j][0]
        tspn1 = g_n1[j][0]
        tspn0 = g_n0[j][0]
        aaxc = c1_axs[j][i, 0]
        aaxn1 = c1_axs[j][i, 1]
        aaxn0 = c1_axs[j][i, 2]
        gtsp = [tspc, tspn1, tspn0, ]
        axs = [aaxc, aaxn1, aaxn0]
        a_lab = ['Control', 'NN-ON', 'NN-OFF']
        for a in range(len(gtsp)):
            plott(axs[a], gtsp[a][ch[i]], c_img)
            # lines for the gap
            for p in [-0.5, 0.5]:
                axs[a].axhline(y=p, color=cct, linestyle='-.', lw=0.5)
                # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            if i == 2:
                aaxc.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' +
                    '\n\n\n', fontsize=8)
            else:
                aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                                fontsize=8)
        else:
            pass

        # x label
        if i == 5:
            aaxn1.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)
        elif i == 0:
            for a in range(len(gtsp)):
                axs[a].set_title(a_lab[a], fontdict=dict(fontweight='bold',
                                                         fontsize=7))

for i in lv_off:
    for j in range(len(ch)):
        c1_axs[i][j, 0].set_axis_off()
        c1_axs[i][j, 1].set_axis_off()

# heatmap normalization
norm_color(c_img, 'tsp')

# colorbar
for i in range(len(lvp)):
    cbart1 = c1_fig.colorbar(c_img[i], ax=c1_axs[lvp[i]],
                             orientation='horizontal',
                             format='%.2f',
                             fraction=.03,
                             ticks=ticker.MaxNLocator(6))
    cbart1.ax.tick_params(labelsize=6)
    cbart1.ax.set_title('Amplitude ' + r'(mV)', fontdict={'fontsize': 8})
    cbart1.update_ticks()

    # if axinc[i] in axinc[-5:0]:
    #     cbar_t(cbart1, 'tsp')
    # else:
    #     axinc[i].remove()
    c1_axs[lvp[i]][0, 1].text(50, 3, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              # transform=st_axes[0, 0].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

c1_axs[lvp[0]][2, 0].text(-80, -1.5, 'Depth\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          # transform=st_axes[0, 0].transAxes,
                          fontdict={'size': 8}
                          )

plt.savefig(snakemake.output[0], dpi=300)
c1_fig.clf()
# # lfp heatmap
cl_img = []
cl_ind = []

l1_fig = plt.figure(0, figsize=(16, 9), dpi=300)
# c1_fig.patch.set_facecolor(cct)

l1_axs1 = l1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.07, right=0.270,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))

l1_axs2 = l1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.3, right=0.50,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))
l1_axs3 = l1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.53, right=0.73,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))
l1_axs4 = l1_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.76, right=0.96,
                                                       top=0.90, bottom=0.06,
                                                       wspace=ws, hspace=hs))

# axs1[0][0].set_title('hey''70')
l1_axs = {'70': l1_axs1, '60': l1_axs2, '50': l1_axs3, '40': l1_axs4}

for j in lvp:
    for i in range(len(ch)):
        tspc = g_s[j][1]
        tspn1 = g_n1[j][1]
        tspn0 = g_n0[j][1]
        aaxc = l1_axs[j][i, 0]
        aaxn1 = l1_axs[j][i, 1]
        aaxn0 = l1_axs[j][i, 2]
        gtsp = [tspc, tspn1, tspn0, ]
        axs = [aaxc, aaxn1, aaxn0]
        a_lab = ['Control', 'NN-ON', 'NN-OFF']
        for a in range(len(gtsp)):
            plott(axs[a], gtsp[a][ch[i]], cl_img)

            # lines for the gap
            for p in [-0.5, 0.5]:
                axs[a].axhline(y=p, color=cct, linestyle='-.', lw=0.5)
            # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            if i == 2:
                aaxc.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' +
                    '\n\n\n', fontsize=8)
            else:
                aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                                fontsize=8)
        else:
            pass

        # x label
        if i == 5:
            aaxn1.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)
        elif i == 0:
            for a in range(len(gtsp)):
                axs[a].set_title(a_lab[a], fontdict=dict(fontweight='bold',
                                                         fontsize=7))

lv_off = [x for x in lvl if x not in lvp]

for i in lv_off:
    for j in range(len(ch)):
        l1_axs[i][j, 0].set_axis_off()
        l1_axs[i][j, 1].set_axis_off()

# heatmap normalization
norm_color(cl_img, 'lfp')

# colorbar
for i in range(len(lvp)):
    lbart1 = l1_fig.colorbar(cl_img[i], ax=l1_axs[lvp[i]],
                             orientation='horizontal',
                             format='%.2f',
                             fraction=.017,
                             ticks=ticker.MaxNLocator(6))
    lbart1.ax.tick_params(labelsize=6)
    lbart1.ax.set_title('Amplitude ' + r'(mV)', fontdict={'fontsize': 8})
    lbart1.update_ticks()

    # if axinc[i] in axinc[-5:0]:
    #     cbar_t(cbart1, 'tsp')
    # else:
    #     axinc[i].remove()
    l1_axs[lvp[i]][0, 1].text(50, 3, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              # transform=st_axes[0, 0].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

l1_axs[lvp[0]][2, 0].text(-80, -1.5, 'Depth\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          # transform=st_axes[0, 0].transAxes,
                          fontdict={'size': 8}
                          )

plt.savefig(snakemake.output[1], dpi=300)
plt.clf()

# frequency profile
f1_fig = plt.figure(figsize=(16, 9), dpi=300)
f1_axs = f1_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.5, hspace=0.3))
f_max = []
f_min = []

for j in lvp:
    pi = lvl.index(j)

    tspc = g_s[j][2]
    tspn1 = g_n1[j][2]
    tspn0 = g_n0[j][2]
    tspw1 = g_w1[j][2]
    tspw0 = g_w0[j][2]

    if not np.any(tspw1):
        tspw1 = np.zeros([16, 25])
        tspw0 = np.zeros([16, 25])
    else:
        pass

    f_max = np.append(f_max, np.max([np.max(tspn1),
                                     np.max(tspn0),
                                     np.max(tspw1),
                                     np.max(tspw0),
                                     np.max(tspc)]))

ym = np.around(np.max(f_max), decimals=1) + 0.1

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f1_axs[i, pi]
        tspc = g_s[j][2]
        tspn1 = g_n1[j][2]
        tspn0 = g_n0[j][2]
        tspw1 = g_w1[j][2]
        tspw0 = g_w0[j][2]

        if not np.any(tspw1):
            tspw1 = np.zeros([16, 25])
            tspw0 = np.zeros([16, 25])
        else:
            pass

        gtsp = [tspc, tspn1, tspw1, tspn0, tspw0]
        lb = ['Control', 'NN-ON', 'WN-ON', 'NN-OFF', 'WN-OFF']
        for ti in range(len(gtsp)):
            fa.plot(octs, gtsp[ti][ch[i]], label=lb[ti], lw=1)
        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_yticks(np.linspace(0, ym, 5, endpoint=True))
        fa.set_ylim(top=ym)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 4}, bbox_to_anchor=(1.23, 1.05))
        fa.tick_params(axis='both', which='major', labelsize=6, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                          fontsize=8)
        else:
            pass

        if i == 0:
            fa.text(0, 0.7, f'{j} SPL dB',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    # transform=st_axes[0, 0].transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )
        elif i == len(ch) - 1:
            fa.text(0, -0.15, f'Octave',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    # transform=st_axes[0, 0].transAxes,
                    fontdict={'size': 8}
                    )

f1_axs[2, 0].text(-2.6, -0.06, 'Depth\n\n\n\n\nspk/s',
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='vertical',
                  # transform=st_axes[0, 0].transAxes,
                  fontdict={'size': 8}
                  )
for j in lv_off:
    o_i = lvl.index(j)
    for i in range(len(ch)):
        f1_axs[i, o_i].set_axis_off()

plt.savefig(snakemake.output[2], dpi=300)
plt.clf()

# frequency profile lfp

f2_fig = plt.figure(figsize=(16, 9), dpi=300)
f2_axs = f2_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.5, hspace=0.3))
f_max = []
f_min = []

for j in lvp:
    pi = lvl.index(j)

    tspc = g_s[j][3]
    tspn1 = g_n1[j][3]
    tspn0 = g_n0[j][3]
    tspw1 = g_w1[j][3]
    tspw0 = g_w0[j][3]

    if not np.any(tspw1):
        tspw1 = np.zeros([16, 25])
        tspw0 = np.zeros([16, 25])
    else:
        pass

    f_max = np.append(f_max, np.max([np.max(tspn1),
                                     np.max(tspn0),
                                     np.max(tspw1),
                                     np.max(tspw0),
                                     np.max(tspc)]))

    f_min = np.append(f_min, np.min([np.min(tspn1),
                                     np.min(tspn0),
                                     np.min(tspw1),
                                     np.min(tspw0),
                                     np.min(tspc)]))

ymx = np.around(np.max(f_max), decimals=-1) + 50
ymn = np.around(np.max(f_min), decimals=-1) - 50

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f2_axs[i, pi]
        tspc = g_s[j][3]
        tspn1 = g_n1[j][3]
        tspn0 = g_n0[j][3]
        tspw1 = g_w1[j][3]
        tspw0 = g_w0[j][3]

        if not np.any(tspw1):
            tspw1 = np.zeros([16, 25])
            tspw0 = np.zeros([16, 25])
        else:
            pass

        gtsp = [tspc, tspn1, tspw1, tspn0, tspw0]
        lb = ['Control', 'NN-ON', 'WN-ON', 'NN-OFF', 'WN-OFF']

        for ti in range(len(gtsp)):
            fa.plot(octs, gtsp[ti][ch[i]], label=lb[ti], lw=1)
        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_yticks([ymn, 0, ymx])
        fa.set_ylim(top=ymx, bottom=ymn)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 4}, bbox_to_anchor=(1.23, 1.05))
        fa.tick_params(axis='both', which='major', labelsize=6, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                          fontsize=8)
        else:
            pass

        if i == 0:
            fa.text(0, 120, f'{j} SPL dB',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    # transform=st_axes[0, 0].transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )
        elif i == len(ch) - 1:
            fa.text(0, -140, f'Octave',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    # transform=st_axes[0, 0].transAxes,
                    fontdict={'size': 8}
                    )

f2_axs[2, 0].text(-2.5, -110, 'Depth\n\n\n\n\n\nAmplitude ' + r'(mV)',
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='vertical',
                  # transform=st_axes[0, 0].transAxes,
                  fontdict={'size': 8}
                  )
for j in lv_off:
    o_i = lvl.index(j)
    for i in range(len(ch)):
        f2_axs[i, o_i].set_axis_off()
plt.savefig(snakemake.output[3], dpi=300)
