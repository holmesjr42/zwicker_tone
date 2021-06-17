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
val = pm.Setup(cond='nnm_3_0_05', cond2='tsp', mode=1, ratio=0.7)
val2 = pm.Setup(cond='nnm_3_0', cond2='lfp', mode=1, ccmap='lfp')
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, \
cb, ccmap = val.values()
ccl = val2.values()[-3]  # color for notch borders
# lfp spectrogram colormap
lcmap = val2.values()[-1]
condl = 'lfp'
octs = com.octaves  # octave range for plotting
lvl = com.db['lv']  # SPLdB list
g_n = {}  # dict of lfp for nnm condition
g_s = {}  # dict of lfp for strf condition
# dataset
# file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
#              '/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm.hdf5'
file_input = snakemake.input[0]
# getting animal cr number
animal = file_input.split('/')[-1].split('_')[0]

if not animal in ['cr29', 'cr31', 'cr33', 'cr50', 'cr79', 'all']:
    for i in snakemake.output:
        plt.figure()
        plt.savefig(i, dpi=150)
    sys.exit()
else:
    pass

# conditions for this script
c_n = 'nnm_3_0_05'
c_s = 'nnm_3_0_05_strf'
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

    sk = [datas['tsp'][c_n], datas['tsp'][c_s]]  # spk
    lp = [datas['lfp'][c_n], datas['lfp'][c_s]]  # lfp

    sa = [datas['fpt'][c_n], datas['fpt'][c_s]]  # spk_average
    sd = [datas['ssd'][c_n], datas['ssd'][c_s]]  # spk_average_std
    sc = [datas['scf'][c_n], datas['scf'][c_s]]  # spk_average confidence

    la = [datas['fpl'][c_n], datas['fpl'][c_s]]  # lfp_average
    ld = [datas['lsd'][c_n], datas['lsd'][c_s]]  # lfp_average_std
    lc = [datas['lcf'][c_n], datas['lcf'][c_s]]  # lfp_average confidence

    for i in lvl:
        g_n[i] = [np.array(sk[0][i]), np.array(lp[0][i]),
                  np.array(sa[0][i]), np.array(la[0][i]),
                  np.array(sd[0][i]), np.array(ld[0][i]),
                  np.array(sc[0][i]), np.array(lc[0][i])
                  ]
        g_s[i] = [np.array(sk[1][i]), np.array(lp[1][i]),
                  np.array(sa[1][i]), np.array(la[1][i]),
                  np.array(sd[1][i]), np.array(ld[1][i]),
                  np.array(sc[1][i]), np.array(lc[1][i])
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
    aax.set_xticks(np.linspace(0, 100, 3, endpoint=True))
    # aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
    aax.set_yticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5], minor=True)
    aax.set_yticks([-1., -0.25, 0., 0.25, 1.])

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
nn continuous
'''

#  heatmap
# setup
c_img = []
# cx_ind = []
# # axinc = []
lvp = []  # spl list which actually has data
for i in range(len(lvl)):
    if not np.any(g_n[lvl[i]][0]):
        continue
    else:
        lvp.append(lvl[i])

lv_off = [x for x in lvl if x not in lvp]

c1_fig = plt.figure(0, figsize=(16, 9), dpi=300)
# c1_fig.patch.set_facecolor(cct)

c1_axs1 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.12, right=0.286,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))

c1_axs2 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.316, right=0.471,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))
c1_axs3 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.501, right=0.657,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))
c1_axs4 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.687,
                                                       right=0.843,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))

c1_axs = {'70': c1_axs1, '60': c1_axs2, '50': c1_axs3, '40': c1_axs4}

# fig.suptitle('Multiple images')

for j in lvp:
    for i in range(len(ch)):
        tspn = g_n[j][0]
        tspc = g_s[j][0]
        aaxn = c1_axs[j][i, 1]
        aaxc = c1_axs[j][i, 0]
        # print('hey', tspc[i])
        plott(aaxn, tspn[ch[i]], c_img)
        plott(aaxc, tspc[ch[i]], c_img)
        # axinc.append(axin_s)

        # lines for the gap
        for axes in [aaxn, aaxc]:
            for p in [-0.25, 0.25]:
                axes.axhline(y=p, color='white', linestyle='-.', lw=0.6)
            # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n\n ',
                            fontsize=10)
        else:
            pass

        # x label
        if i == len(ch) - 1:
            aaxc.text(1, -0.4, 'time (ms)',
                      horizontalalignment='center',
                      verticalalignment='center',
                      # rotation='vertical',
                      transform=aaxc.transAxes,
                      fontdict={'weight': 'bold', 'size': 11}
                      )

        # subplot title
        if i == 0:
            aaxn.title.set_text('NN')
            aaxc.title.set_text('Control')

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

    c1_axs[lvp[i]][0, 0].text(1.3, 1.5, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              transform=c1_axs[lvp[i]][0, 0].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

c1_axs[lvp[0]][2, 0].text(-1.1, 0.5, 'Depth\n\n\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          transform=c1_axs['70'][2, 0].transAxes,
                          fontdict={'weight': 'bold', 'size': 11}
                          )

plt.savefig(snakemake.output[0], dpi=300)
# plt.savefig('test0.png', dpi=300)
# plt.show()
c1_fig.clf()
# lfp heatmap
cl_img = []
cl_ind = []

l1_fig = plt.figure(0, figsize=(16, 9), dpi=300)
# c1_fig.patch.set_facecolor(cct)

l1_axs1 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.12, right=0.286,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))

l1_axs2 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.316, right=0.471,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))
l1_axs3 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.501, right=0.657,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))
l1_axs4 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.687,
                                                       right=0.843,
                                                       top=0.90, bottom=0.07,
                                                       wspace=ws, hspace=hs))
# axs1[0][0].set_title('hey''70')
l1_axs = {'70': l1_axs1, '60': l1_axs2, '50': l1_axs3, '40': l1_axs4}

for j in lvp:
    for i in range(len(ch)):
        tspn = g_n[j][1]
        tspc = g_s[j][1]
        aaxn = l1_axs[j][i, 1]
        aaxc = l1_axs[j][i, 0]
        # print('hey', tspc[i])
        plott(aaxn, tspn[ch[i]], cl_img, cm=lcmap)
        plott(aaxc, tspc[ch[i]], cl_img, cm=lcmap)
        # axinc.append(axin_s)

        # lines for the gap
        for axes in [aaxn, aaxc]:
            for p in [-0.25, 0.25]:
                axes.axhline(y=p, color=ccl, linestyle='-.', lw=0.5)
            # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            aaxc.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n\n ',
                            fontsize=10)
        else:
            pass

        # x label
        if i == len(ch) - 1:
            aaxc.text(1, -0.4, 'time (ms)',
                      horizontalalignment='center',
                      verticalalignment='center',
                      # rotation='vertical',
                      transform=aaxc.transAxes,
                      fontdict={'weight': 'bold', 'size': 11}
                      )

        # subplot title
        if i == 0:
            aaxn.title.set_text('NN')
            aaxc.title.set_text('Control')

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

    l1_axs[lvp[i]][0, 0].text(1, 1.6, f'{lvp[i]} SPL dB',
                              horizontalalignment='center',
                              verticalalignment='center',
                              # rotation='vertical',
                              transform=l1_axs[lvp[i]][0, 0].transAxes,
                              fontdict={'weight': 'bold', 'size': 11}
                              )

l1_axs[lvp[0]][2, 0].text(-1.1, 0.5, 'Depth\n\n\n\n\n\n\nOctave',
                          horizontalalignment='center',
                          verticalalignment='center',
                          rotation='vertical',
                          transform=l1_axs['70'][2, 0].transAxes,
                          fontdict={'weight': 'bold', 'size': 11}
                          )

plt.savefig(snakemake.output[1], dpi=300)
# plt.savefig('test1.png', dpi=300)
plt.clf()

# frequency profile
f1_fig = plt.figure(figsize=(16, 9), dpi=300)
f1_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)
f1_axs = f1_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))

f_max = []
fmd = 0

for j in range(len(lvp)):
    pi = lvl.index(lvp[j])
    for i in range(len(ch)):
        tspn = g_n[lvp[j]][2][ch[i]]
        tspc = g_s[lvp[j]][2][ch[i]]
        tvn = g_n[lvp[j]][6][ch[i]]
        tvc = g_s[lvp[j]][6][ch[i]]

        f_max.append([np.max(tvn), np.max(tvc)])

ym = np.around(np.max(f_max) * 1.3, decimals=2)

'''
This is to get the maximum of the y axis in case you are going to use
standard deviation instead of confidence interval
# fmx = np.max(f_max)
#
# for j in range(len(lvp)):
#     pi = lvl.index(lvp[j])
#     for i in range(len(ch)):
#         tspn = g_n[lvp[j]][2][ch[i]]
#         tspc = g_s[lvp[j]][2][ch[i]]
#         tsdn = g_n[lvp[j]][6][ch[i]]
#         tsdc = g_s[lvp[j]][6][ch[i]]
#
#         if fmx in tspn:
#             dind, = np.where(tspn == fmx)[0]
#             fmd = tsdn[dind]
#         elif fmx in tspc:
#             dind, = np.where(tspn == fmx)[0]
#             fmd = tsdc[dind]
#         else:
#             continue
#
# ym = np.around((fmx + fmd) * 1.4, decimals=2)
'''

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f1_axs[i, pi]
        tspn = g_n[j][2]
        tspc = g_s[j][2]
        tvn = g_n[j][6]
        tvc = g_s[j][6]

        p_dat = [tspc, tspn]
        p_var = [tvc, tvn]
        labelz = ['Control', 'NN']
        ltype = ['-', '--']

        for k in range(2):
            fa.plot(octs, p_dat[k][ch[i]],
                    label=labelz[k], lw=1,
                    color=dcmap[k], linestyle=ltype[k]
                    )
            fa.fill_between(
                octs,
                p_var[k][ch[i]][:, 0],
                p_var[k][ch[i]][:, 1],
                alpha=.2
                )
        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_yticks(np.linspace(0, ym, 3, endpoint=True))
        fa.set_ylim(top=ym)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 6}, bbox_to_anchor=(1.3, 1.05))
        fa.tick_params(axis='both', which='major', labelsize=8, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.25, 0.25]:
            fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                          fontsize=8)
        else:
            pass

        # tick lable off
        if i != len(ch) - 1:
            fa.tick_params(labelbottom=False)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
                          fontsize=10)
        else:
            fa.tick_params(labelleft=False)

        # legend box
        if j == lvp[3] and i == 0:
            fa.legend(prop={'size': 7.5}, bbox_to_anchor=(1, 1))
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
                    fontdict={'size': 8}
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

# plt.savefig('test2.png', dpi=300)
plt.savefig(snakemake.output[2], dpi=300)
plt.clf()

# frequency profile lfp

f2_fig = plt.figure(figsize=(16, 9), dpi=300)
f2_axs = f2_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.15, hspace=0.2))
f2_fig.subplots_adjust(left=0.12, right=0.92, top=0.9, bottom=0.1)

f_max = []
f_min = []

for j in range(len(lvp)):
    pi = lvl.index(lvp[j])
    for i in range(len(ch)):
        tspn = g_n[lvp[j]][3][ch[i]]
        tspc = g_s[lvp[j]][3][ch[i]]
        tvn = g_s[lvp[j]][7][ch[i]]
        tvc = g_s[lvp[j]][7][ch[i]]

        f_max.append([np.max(tvn), np.max(tvc)])
        f_min.append([np.min(tvn), np.min(tvc)])

ymx = np.around(np.max(f_max) * 1.3, decimals=-1)
ymn = np.around(np.min(f_min) * 1.3, decimals=-1)

for j in lvp:
    pi = lvl.index(j)
    for i in range(len(ch)):
        fa = f2_axs[i, pi]
        tspn = g_n[j][3]
        tspc = g_s[j][3]
        tvn = g_n[j][7]
        tvc = g_s[j][7]

        p_dat = [tspc, tspn]
        p_var = [tvc, tvn]
        labelz = ['Control', 'NN']
        ltype = ['-', '--']

        for k in range(len(p_dat)):
            fa.plot(octs, p_dat[k][ch[i]],
                    label=labelz[k], lw=1,
                    color=dcmap[k], linestyle=ltype[k]
                    )

            fa.fill_between(octs,
                            p_var[k][ch[i]][:, 0],
                            p_var[k][ch[i]][:, 1], alpha=.2
                            )

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_yticks([ymn, 0, ymx])
        fa.set_ylim(top=ymx, bottom=ymn)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.tick_params(axis='both', which='major', labelsize=8, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.25, 0.25]:
            fa.axvline(x=p, color='#363b50', linestyle='-.', lw=0.7)

        # tick lable off
        if i != len(ch) - 1:
            fa.tick_params(labelbottom=False)

        if j == lvp[0]:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n',
                          fontsize=10)
        else:
            fa.tick_params(labelleft=False)

        if j == lvp[3] and i == len(ch) - 1:
            fa.legend(prop={'size': 7.5}, bbox_to_anchor=(1, 0.4))
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

# plt.savefig('test3.png', dpi=300)
plt.savefig(snakemake.output[3], dpi=300)
