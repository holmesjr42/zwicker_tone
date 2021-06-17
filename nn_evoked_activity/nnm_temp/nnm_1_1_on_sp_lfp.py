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
val = pm.Setup(cond='nnm_1_1', cond2='tsp', mode=1, ratio=0.7)
val2 = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, \
cb, ccmap = val.values()
lst = ['solid', 'dashed', 'dashdot', 'dashed', 'dashdot']
ccl = val2.values()[-3]  # color for notch borders
# lfp spectrogram colormap
lcmap = val2.values()[-1]
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

if not animal in ['cr31', 'cr33', 'cr50', 'cr79', 'cr90', 'cr94',
                  'all'
                  ]:
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
            for i in ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf', 'lsd']:
                datas[i][c_s].pop('30')

        else:
            pass

        if '30' in list(datas['lfp'][c_n].keys()):
            for i in ['tsp', 'lfp', 'fpt', 'fpl', 'scf', 'ssd', 'lcf', 'lsd']:
                datas[i][c_n].pop('30')
        else:
            pass

    else:
        pass

    # aranging dataset
    sk = [datas['tsp'][c_n], datas['tsp'][c_s], datas['tsp'][c_w]]  # spk
    lp = [datas['lfp'][c_n], datas['lfp'][c_s], datas['lfp'][c_w]]  # lfp

    sa = [datas['fpt'][c_n], datas['fpt'][c_s],
          datas['fpt'][c_w]]  # spk_mean
    sd = [datas['ssd'][c_n], datas['ssd'][c_s], datas['ssd'][c_w]]
    # spk_average_std

    sc = [datas['scf'][c_n], datas['scf'][c_s], datas['scf'][c_w]]
    # spk_average confidence

    la = [datas['fpl'][c_n], datas['fpl'][c_s],
          datas['fpl'][c_w]]  # lfp_mean
    ld = [datas['lsd'][c_n], datas['lsd'][c_s], datas['lsd'][c_w]]
    # lfp_average_std

    lc = [datas['lcf'][c_n], datas['lcf'][c_s], datas['lcf'][c_w]]
    # lfp_average confidence

    if 'cr' in animal:
        for i in lvl:
            g_s[i] = [np.array(sk[1][i]), np.array(lp[1][i]),
                      np.array(sa[1][i]), np.array(la[1][i]),
                      np.array(sd[1][i]), np.array(ld[1][i]),
                      np.array(sc[1][i]), np.array(lc[1][i])
                      ]

            g_n1[i] = [np.array(sk[0]['nn'][i]), np.array(lp[0]['nn'][i]),
                       np.array(sa[0]['nn'][i]), np.array(la[0]['nn'][i]),
                       np.array(sd[0]['nn'][i]), np.array(ld[0]['nn'][i]),
                       np.array(sc[0]['nn'][i]), np.array(lc[0]['nn'][i])
                       ]

            g_w1[i] = [np.array(sk[2]['nn'][i]), np.array(lp[2]['nn'][i]),
                       np.array(sa[2]['nn'][i]), np.array(la[2]['nn'][i]),
                       np.array(sd[2]['nn'][i]), np.array(ld[2]['nn'][i]),
                       np.array(sc[2]['nn'][i]), np.array(lc[2]['nn'][i])
                       ]

    elif 'all' in animal:
        for i in lvl:
            g_s[i] = [np.array(sk[1][i]), np.array(lp[1][i]),
                      np.array(sa[1][i]), np.array(la[1][i]),
                      np.array(sd[1][i]), np.array(ld[1][i]),
                      np.array(sc[1][i]), np.array(lc[1][i])
                      ]

            g_n1[i] = [np.array(sk[0][i][0]), np.array(lp[0][i][0]),
                       np.array(sa[0][i][0]), np.array(la[0][i][0]),
                       np.array(sd[0][i][0]), np.array(ld[0][i][0]),
                       np.array(sc[0][i][0]), np.array(lc[0][i][0])
                       ]

            g_w1[i] = [np.array(sk[2][i][0]), np.array(lp[2][i][0]),
                       np.array(sa[2][i][0]), np.array(la[2][i][0]),
                       np.array(sd[2][i][0]), np.array(ld[2][i][0]),
                       np.array(sc[2][i][0]), np.array(lc[2][i][0])
                       ]


# function for plotting

def plott(aax, dats, imag, cm=ccmap):
    aax.tick_params(axis='both', which='major', labelsize=8, length=3,
                    width=0.7)
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
    aax.set_xticks(np.linspace(0, 50, 2, endpoint=True))
    # aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
    aax.set_yticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5], minor=True)
    aax.set_yticks([-1., 0., 1.])

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


def norm_color(img, types, ratio=rt):
    if types == 'lfp':
        vmin = min(ims.get_array().min() for ims in img) * ratio
        vmax = -1 * vmin
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
    elif types == 'tsp':
        vmin = 0
        vmax = max(ims.get_array().max() for ims in img) * ratio
        norm = colors.Normalize(vmin=vmin, vmax=vmax)
    else:
        print('there is a problem with norm_color. check it')
        sys.exit()

    for ims in img:
        ims.set_norm(norm)


# plot setup
'''
nn/wn off
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
        tspn = g_n1[j][0]
        tspw = g_w1[j][0]
        aaxc = c1_axs[j][i, 0]
        aaxn = c1_axs[j][i, 1]
        aaxw = c1_axs[j][i, 2]

        if not np.any(tspw):
            tspw = np.zeros([16, 25, 101])

        else:
            pass

        p_dat = [tspc, tspn, tspw]
        axs = [aaxc, aaxn, aaxw]
        a_lab = ['Control', 'NN-ON', 'WN-ON']
        for a in range(len(p_dat)):

            plott(axs[a], p_dat[a][ch[i]], c_img)
            # lines for the gap
            for p in [-0.5, 0.5]:
                axs[a].axhline(y=p, color='white', linestyle='-.', lw=0.6)
                # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                            fontsize=8)

        else:
            pass

        # x label
        if i == len(ch) - 1:
            aaxn.text(0.5, -0.4, 't (ms)',
                      horizontalalignment='center',
                      verticalalignment='center',
                      # rotation='vertical',
                      transform=aaxn.transAxes,
                      fontdict={'weight': 'bold', 'size': 10}
                      )
        elif i == 0:
            for a in range(len(p_dat)):
                axs[a].title.set_text(a_lab[a])

for i in lv_off:
    for j in range(len(ch)):
        c1_axs[i][j, 0].set_axis_off()
        c1_axs[i][j, 1].set_axis_off()

# heatmap normalization
norm_color(c_img, 'tsp')

cmx = max(ims.get_array().max() for ims in c_img) * rt  # max value of the
# tsp data for colorbar tick

# colorbar
for i in range(len(lvp)):
    cbart1 = c1_fig.colorbar(
        c_img[i], ax=c1_axs[lvp[i]],
        orientation='horizontal',
        format='%.2f',
        fraction=.017,
        ticks=np.linspace(0, cmx, 3, endpoint=True)
        )
    cbart1.ax.tick_params(labelsize=10)
    cbart1.ax.set_title('Firing rate (spk/s)', fontdict={'fontsize': 11})
    cbart1.update_ticks()

    # if axinc[i] in axinc[-5:0]:
    #     cbar_t(cbart1, 'tsp')
    # else:
    #     axinc[i].remove()
    c1_axs[lvp[i]][0, 1].text(0.5, 1.5, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              transform=c1_axs[lvp[i]][0, 1].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

c1_axs[lvp[0]][2, 0].text(-.7, 0.5, 'Depth\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          transform=c1_axs[lvp[0]][2, 0].transAxes,
                          fontdict={'weight': 'bold', 'size': 9}
                          )

plt.savefig(snakemake.output[0], dpi=300)
# plt.savefig('test0.png', dpi=300)
c1_fig.clf()

# lfp heatmap
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
        tspn = g_n1[j][1]
        tspw = g_w1[j][1]
        aaxc = l1_axs[j][i, 0]
        aaxn = l1_axs[j][i, 1]
        aaxw = l1_axs[j][i, 2]

        if not np.any(tspw):
            tspw = np.zeros([16, 25, 101])

        else:
            pass

        p_dat = [tspc, tspn, tspw]
        axs = [aaxc, aaxn, aaxw]
        a_lab = ['Control', 'NN-ON', 'WN-ON']
        for a in range(len(p_dat)):
            plott(axs[a], p_dat[a][ch[i]]/1000, cl_img, cm=lcmap)

            # lines for the gap
            for p in [-0.5, 0.5]:
                axs[a].axhline(y=p, color='white', linestyle='-.', lw=0.5)
            # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n ',
                            fontsize=8)
        else:
            pass

        # x label
        if i == len(ch) - 1:
            aaxn.text(0.5, -0.4, 't (ms)',
                      horizontalalignment='center',
                      verticalalignment='center',
                      # rotation='vertical',
                      transform=aaxn.transAxes,
                      fontdict={'weight': 'bold', 'size': 10}
                      )
            # aaxn.xaxis.set_label_coords(1.05, -0.4)
        elif i == 0:
            for a in range(len(p_dat)):
                axs[a].title.set_text(a_lab[a])
        else:
            pass

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
                             ticks=ticker.MaxNLocator(3))
    lbart1.ax.tick_params(labelsize=10)
    lbart1.ax.set_title('Amplitude ' + r'(mV)', fontdict={
        'fontsize': 11
        }
                        )

    lbart1.update_ticks()

    l1_axs[lvp[i]][0, 1].text(0.5, 1.5, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              transform=l1_axs[lvp[i]][0, 1].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

l1_axs[lvp[0]][2, 0].text(-.7, 0.5, 'Depth\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          transform=l1_axs[lvp[0]][2, 0].transAxes,
                          fontdict={'weight': 'bold', 'size': 9}
                          )

plt.savefig(snakemake.output[1], dpi=300)
# plt.savefig('test1.png', dpi=300)
plt.clf()

# frequency profile
f1_fig = plt.figure(figsize=(16, 9), dpi=300)
f1_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)
f1_axs = f1_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))

f_max = []

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        tspc = g_s[j][2][ch[i]]
        tspn = g_n1[j][2][ch[i]]
        tsws = g_w1[j][2]
        tvc = g_s[j][6][ch[i]]
        tvn = g_n1[j][6][ch[i]]
        tvws = g_w1[j][6]

        if not np.any(tsws):
            tspw = np.zeros([25, 2])
            tvw = np.zeros(25)
        else:
            tspw = tsws[ch[i]]
            tvw = tvws[ch[i]]

        if 'all' in animal:
            f_max = np.append(f_max, np.max([np.max(tspc),
                                             np.max(tspn),
                                             np.max(tspw)
                                             ]))

        elif 'cr' in animal:
            f_max = np.append(f_max, np.max([np.max(tvn),
                                             np.max(tvc),
                                             np.max(tvw)
                                             ]))

# ym = np.around(np.max(f_max) * 1.3, decimals=2)

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f1_axs[i, pi]
        tspc = g_s[j][2]
        tspn = g_n1[j][2]
        tspw = g_w1[j][2]
        tvc = g_s[j][6]
        tvn = g_n1[j][6]
        tvw = g_w1[j][6]

        if not np.any(tspw):
            tspw = np.zeros([16, 25])
            tvw = np.zeros([16, 25, 2])
        else:
            pass

        p_dat = [tspc, tspn, tspw]
        p_var = [tvc, tvn, tvw]
        lb = ['Control', 'NN-ON', 'WN-ON']

        for ti in range(len(p_dat)):
            fa.plot(octs, p_dat[ti][ch[i]], label=lb[ti], lw=1, color=dcmap[
                ti], linestyle=lst[ti])

            if 'all' in animal:
                pass
            elif 'cr' in animal:
                fa.fill_between(
                    octs,
                    p_var[ti][ch[i]][:, 0],
                    p_var[ti][ch[i]][:, 1],
                    alpha=.2
                    )

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        # fa.set_yticks(np.linspace(0, ym, 3, endpoint=True))
        fa.set_ylim(bottom=0)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.tick_params(axis='both', which='major', labelsize=8, length=3,
                       width=1)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)

        # tick lable off
        if i != len(ch) - 1:
            fa.tick_params(labelbottom=False)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
                          fontsize=10)
        else:
            fa.legend().set_visible(False)
        #     fa.tick_params(labelleft=False)

        # legend box
        if j == lvp[len(lvp) - 1] and i == 0:
            fa.legend(prop={'size': 7},
                      loc='upper right',
                      bbox_to_anchor=(1, 1))
        else:
            pass

        if i == 0:
            fa.text(0.5, 1.5, f'{j} SPL dB',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )
        elif i == len(ch) - 1:
            fa.text(0.5, -0.3, f'Octave',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )

f1_axs[1, 0].text(-0.4, -0.7, 'Depth\n\n\n\n\n\nFiring rate (spk/s)',
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='vertical',
                  transform=f1_axs[1, 0].transAxes,
                  fontdict={'weight': 'bold', 'size': 11}
                  )

for j in lv_off:
    o_i = lvl.index(j)
    for i in range(len(ch)):
        f1_axs[i, o_i].set_axis_off()

plt.savefig(snakemake.output[2], dpi=300)
# plt.savefig('test2.png', dpi=300)
plt.clf()

# frequency profile lfp

f2_fig = plt.figure(figsize=(16, 9), dpi=300)
f2_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)
f2_axs = f2_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))

f_max = []
f_min = []

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        tspc = g_s[j][3][ch[i]]
        tspn = g_n1[j][3][ch[i]]
        tsws = g_w1[j][3]
        tvc = g_s[j][7][ch[i]]
        tvn = g_n1[j][7][ch[i]]
        tvws = g_w1[j][7]

        if not np.any(tsws):
            tspw = np.zeros(25)
            tvw = np.zeros([25, 2])
        else:
            tspw = tsws[ch[i]]
            tvw = tvws[ch[i]]

        if 'all' in animal:
            f_max = np.append(f_max, np.max([np.max(tspc),
                                             np.max(tspn),
                                             np.max(tspw)
                                             ]))/1000

            f_min = np.append(f_min, np.min([np.min(tspc),
                                             np.min(tspn),
                                             np.min(tspw)
                                             ]))/1000

        elif 'cr' in animal:
            f_max = np.append(f_max, np.max([np.max(tvc),
                                             np.max(tvn),
                                             np.max(tvw)
                                             ]))/1000

            f_min = np.append(f_min, np.min([np.min(tvc),
                                             np.min(tvn),
                                             np.min(tvw)
                                             ]))/1000

# ymx = np.around(np.max(f_max) * 1.2, decimals=2)
# ymn = np.around(np.min(f_min) * 1.2, decimals=2)

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f2_axs[i, pi]
        tspc = g_s[j][3]
        tspn = g_n1[j][3]
        tspw = g_w1[j][3]
        tvc = g_s[j][7]
        tvn = g_n1[j][7]
        tvw = g_w1[j][7]

        if not np.any(tspw):
            tspw = np.zeros([16, 25])
            tvw = np.zeros([16, 25, 2])
        else:
            pass

        p_dat = [tspc, tspn, tspw]
        p_var = [tvc, tvn, tvw]
        lb = ['Control', 'NN-ON', 'WN-ON']

        for ti in range(len(p_dat)):
            fa.plot(octs, p_dat[ti][ch[i]]/1000, label=lb[ti], lw=1, color=dcmap[
                ti], linestyle=lst[ti])

            if 'all' in animal:
                pass
            elif 'cr' in animal:
                fa.fill_between(
                    octs,
                    p_var[ti][ch[i]][:, 0]/1000,
                    p_var[ti][ch[i]][:, 1]/1000,
                    alpha=.2
                    )

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        # fa.set_yticks([ymn, 0, ymx])
        # fa.set_ylim(top=ymx, bottom=ymn)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.tick_params(axis='both', which='major', labelsize=8, length=3,
                       width=1)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)

        # tick lable off
        if i != len(ch) - 1:
            fa.tick_params(labelbottom=False)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
                          fontsize=10)
        else:
            fa.legend().set_visible(False)
        #     fa.tick_params(labelleft=False)

        # legend box
        if j == lvp[len(lvp) - 1] and i == 0:
            fa.legend(prop={'size': 7},
                      loc='lower right',
                      bbox_to_anchor=(1, 0))
        else:
            pass

        if i == 0:
            fa.text(0.5, 1.5, f'{j} SPL dB',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )
        elif i == len(ch) - 1:
            fa.text(0.5, -0.3, f'Octave',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 9}
                    )

f2_axs[1, 0].text(-0.4, -0.7, 'Depth\n\n\n\n\n\nAmplitude ' + r'(mV)',
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='vertical',
                  transform=f2_axs[1, 0].transAxes,
                  fontdict={'weight': 'bold', 'size': 11}
                  )

for j in lv_off:
    o_i = lvl.index(j)
    for i in range(len(ch)):
        f2_axs[i, o_i].set_axis_off()

plt.savefig(snakemake.output[3], dpi=300)
# plt.savefig('test3.png', dpi=300)
plt.clf()

# frequency profile: difference between control and notch conditions
f3_fig = plt.figure(figsize=(16, 9), dpi=300)
f3_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)
f3_axs = f3_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))

f_m = []

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        chs = ch[i]
        tspc = g_s[j][2][chs]
        tspn = g_n1[j][2][chs]
        tsws = g_w1[j][2]

        if not np.any(tsws):
            tspw = np.zeros(25)
        else:
            tspw = tsws[chs]

        # tspc1 = [1E-3 if i == 0 else i for i in tspc]
        per = [(tspn - tspc) / tspc, (tspw - tspc) / tspc]

        for ki in range(len(per)):
            per[ki] = [np.nan if infs == np.inf else infs for infs in per[ki]]
        f_m.append(per)

# ymax = np.around(np.nanmax(f_m) * 1.3, decimals=1)
# ymin = np.around(np.nanmin(f_m) * 1.3, decimals=1)


# if ymin == 0:
#     ymin = -0.5
# if ymax == 0:
#     ymax = 0.5


for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        chs = ch[i]
        fa = f3_axs[i, pi]
        tspc = g_s[j][2][chs]
        tspn = g_n1[j][2][chs]
        tsws = g_w1[j][2]

        if not np.any(tsws):
            tspw = np.zeros(25)

        else:
            tspw = tsws[chs]
            pass

        p_datn = (tspn - tspc) / tspc
        p_datw = (tspw - tspc) / tspc
        p_datn = [np.nan if infs == np.inf else infs for infs in p_datn]
        p_datw = [np.nan if infs == np.inf else infs for infs in p_datw]

        p_dat = [p_datn, p_datw]
        lb = ['NN-Ctrl', 'WN-Ctrl']

        for ti in range(len(p_dat)):
            fa.plot(octs, p_dat[ti], label=lb[ti], lw=1, color=dcmap[
                ti], linestyle=lst[ti])

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        # fa.set_yticks([ymin, 0, ymax/2, ymax])
        # fa.set_yticks(np.linspace(0, ym, 3, endpoint=True))
        # fa.set_ylim(top=ymax, bottom=ymin)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.tick_params(axis='both', which='major', labelsize=8, length=3,
                       width=1)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)

        # tick lable off
        if i != len(ch) - 1:
            fa.tick_params(labelbottom=False)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
                          fontsize=10)
        else:
            fa.legend().set_visible(False)
        #     fa.tick_params(labelleft=False)

        # legend box
        if j == lvp[len(lvp) - 1] and i == 0:
            fa.legend(prop={'size': 7},
                      loc='lower right',
                      bbox_to_anchor=(1, 0))
        else:
            pass

        if i == 0:
            fa.text(0.5, 1.5, f'{j} SPL dB',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )
        elif i == len(ch) - 1:
            fa.text(0.5, -0.3, f'Octave',
                    horizontalalignment='center',
                    verticalalignment='center',
                    # rotation='vertical',
                    transform=fa.transAxes,
                    fontdict={'weight': 'bold', 'size': 11}
                    )

f3_axs[1, 0].text(-0.4, -0.7, 'Depth\n\n\n\n\n\n'
                  + r'$\Delta$' + 'Firing rate',
                  horizontalalignment='center',
                  verticalalignment='center',
                  rotation='vertical',
                  transform=f3_axs[1, 0].transAxes,
                  fontdict={'weight': 'bold', 'size': 11}
                  )
for j in lv_off:
    o_i = lvl.index(j)
    for i in range(len(ch)):
        f3_axs[i, o_i].set_axis_off()

plt.savefig(snakemake.output[4], dpi=300)
# plt.savefig('test4.png', dpi=300)
plt.clf()

# # frequency profile lfp: difference between control and notch conditions
# f4_fig = plt.figure(figsize=(16, 9), dpi=300)
# f4_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)
# f4_axs = f4_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))
#
# f_m = []
#
# for j in lvp:
#     pi = lvl.index(j)
#     for i in range(len(ch)):
#         chs = ch[i]
#         tspc = g_s[j][3][chs]
#         tspn = g_n1[j][3][chs]
#         tsws = g_w1[j][3]
#
#         if not np.any(tsws):
#             tspw = np.zeros(25)
#         else:
#             tspw = tsws[chs]
#
#         f_m.append([(tspn - tspc), (tspw - tspc)])
#
# ymax = np.around(np.max(f_m) * 1.3, decimals=0)
# ymin = np.around(np.min(f_m) * 1.3, decimals=1)
#
# for j in lvp:
#     pi = lvl.index(j)
#     for i in range(len(ch)):
#         chs = ch[i]
#         fa = f4_axs[i, pi]
#         tspc = g_s[j][3][chs]
#         tspn = g_n1[j][3][chs]
#         tsws = g_w1[j][3]
#
#         if not np.any(tsws):
#             tspw = np.zeros(25)
#
#         else:
#             tspw = tsws[chs]
#             pass
#
#         p_datn = (tspn - tspc) #/ tspc
#         p_datw = (tspw - tspc) #/ tspc
#
#         p_datn = [np.nan if infs == np.inf else infs for infs in p_datn]
#         p_datw = [np.nan if infs == np.inf else infs for infs in p_datw]
#
#         p_dat = [p_datn, p_datw]
#         lb = ['NN-Ctrl', 'WN-Ctrl']
#
#         for ti in range(len(p_dat)):
#             fa.plot(octs, p_dat[ti], label=lb[ti], lw=1, color=dcmap[
#                 ti], linestyle=lst[ti])
#
#         fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
#         ytic = np.linspace(ymin, ymax, 3)
#         ytic = np.append(ytic, 0)
#         fa.set_yticks(ytic)
#         # fa.set_yticks(np.linspace(0, ym, 3, endpoint=True))
#         # fa.set_ylim(top=ymax, bottom=ymin)
#         fa.set_xlim(left=-1.5, right=1.5)
#         fa.tick_params(axis='both', which='major', labelsize=8, length=3,
#                        width=1)
#         fa.grid(True, alpha=0.6, lw=0.5)
#
#         for p in [-0.5, 0.5]:
#             fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)
#
#         # tick lable off
#         if i != len(ch) - 1:
#             fa.tick_params(labelbottom=False)
#
#         if j == lvp[0]:
#             fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
#                           fontsize=10)
#         # else:
#         #     fa.tick_params(labelleft=False)
#
#         # legend box
#         if j == lvp[len(lvp) - 1] and i == 0:
#             fa.legend(prop={'size': 7},
#                       loc='lower right',
#                       bbox_to_anchor=(1, 0))
#         else:
#             pass
#
#         if i == 0:
#             fa.text(0.5, 1.5, f'{j} SPL dB',
#                     horizontalalignment='center',
#                     verticalalignment='center',
#                     # rotation='vertical',
#                     transform=fa.transAxes,
#                     fontdict={'weight': 'bold', 'size': 11}
#                     )
#         elif i == len(ch) - 1:
#             fa.text(0.5, -0.3, f'Octave',
#                     horizontalalignment='center',
#                     verticalalignment='center',
#                     # rotation='vertical',
#                     transform=fa.transAxes,
#                     fontdict={'weight': 'bold', 'size': 11}
#                     )
#
# f4_axs[1, 0].text(-0.4, -0.7, 'Depth\n\n\n\n\n\n'
#                   + r'$\Delta$' + 'Amplitude ' + r'(mV)',
#                   horizontalalignment='center',
#                   verticalalignment='center',
#                   rotation='vertical',
#                   transform=f4_axs[1, 0].transAxes,
#                   fontdict={'weight': 'bold', 'size': 11}
#                   )
# for j in lv_off:
#     o_i = lvl.index(j)
#     for i in range(len(ch)):
#         f4_axs[i, o_i].set_axis_off()
#
# plt.savefig(snakemake.output[5], dpi=300)
# # plt.savefig('test5.png', dpi=300)

