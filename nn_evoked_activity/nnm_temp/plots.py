import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
import parameters as pm

# matplotlib.use('Agg')

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# data setup
# load file
dat = pm.Datas
nnmt = dat.nnm_t
nnml = dat.nnm_l
nnmf = dat.nnm_f
nnmlf = dat.nnm_lf

# some adjustments for plots: channels you are going to use, wspace, hspace,
# colormap, min and max values for heatmap

# continuous nn
val = pm.Setup(cond='nnm_3_0_05', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, ws, hs, ccmap, cct = val.values()
ccl = '#4e69ab'
condl = 'lfp'
octs = com.octaves
lvlc = list(nnmt[nnc.lists[condc][0]].keys())

# nn and silence
valn = pm.Setup(cond='nnm_1_1', cond2='tsp', yl=0.15)
yln = valn.values()[1]
condn = valn.values()[2]
lvln = list(nnmt[nns.lists[condn][0]]['nn'].keys())[0:4]

# ch = [5,6,7,8,9]
# depth = ['0', '100', '200', '300', '400']


# function for plotting

def plott(aax, dats, imag):
    aax.tick_params(axis='both', which='major', labelsize=4, length=0.9,
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
    imag.append(aax.imshow(dats, cmap=ccmap, aspect='auto',
                           interpolation='gaussian'))
    # plt.subplots_adjust(wspace=.001)
    aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
    aax.set_yticklabels([-1.5, -1., -0.5, 0., 0.5, 1., 1.5])
    aax.label_outer()


# plot setup
'''
nn continuous
'''

#  heatmap

c1_fig = plt.figure(0, figsize=(10, 5), dpi=200)
c1_fig.patch.set_facecolor(cct)

c1_axs1 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.07, right=0.226,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))

c1_axs2 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.256, right=0.412,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
c1_axs3 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.442, right=0.598,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
c1_axs4 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.628,
                                                       right=0.784,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
c1_axs5 = c1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.814, right=0.97,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
# axs1[0][0].set_title('hey''70')
c1_axs = [c1_axs1, c1_axs2, c1_axs3, c1_axs4, c1_axs5]

# fig.suptitle('Multiple images')


imaget1 = []

for j in range(len(lvlc)):
    for i in range(len(ch)):
        nn = nnc.lists[condc][0]
        ct = nnc.lists[condc][1]
        tspn = nnmt[nn][lvlc[j]]
        tspc = nnmt[ct][lvlc[j]]
        aaxn = c1_axs[j][i, 0]
        aaxc = c1_axs[j][i, 1]
        # print('hey', tspc[i])
        plott(aaxn, tspn[ch[i]], imaget1)
        plott(aaxc, tspc[ch[i]], imaget1)

        # lines for the gap
        for axes in [aaxn, aaxc]:
            if condc == 'nnm_3_0_05':
                for p in [10, 14]:
                    axes.axhline(y=p, color=cct, linestyle='-.', lw=0.5)
            else:
                for p in [8, 16]:
                    axes.axhline(y=p, color=cct, linestyle='-.', lw=0.5)
                # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == 0:
            if i == 2:
                aaxn.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' + '\n\nOctave', fontsize=8)
            else:
                aaxn.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                                fontsize=8)
        else:
            pass

        # x label
        if i == 4:
            aaxn.set_xlabel('t (ms)', fontsize=8)
            aaxc.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)

        # subplot title
        if i == 0:
            aaxn.title.set_text('NN')
            aaxc.title.set_text('STRF')

# heatmap normalization
vmint1 = np.around(min(image.get_array().min() for image in imaget1),
                   decimals=2)
vmaxt1 = np.around(max(image.get_array().max() for image in imaget1),
                   decimals=2)
print(vmint1, vmaxt1)

normt1 = colors.Normalize(vmin=vmint1, vmax=vmaxt1)

for im in imaget1:
    im.set_norm(normt1)

for k in range(len(lvlc)):
    cbart1 = c1_fig.colorbar(imaget1[k], ax=c1_axs[k],
                             orientation='horizontal',
                             fraction=.03)
    cbart1.ax.tick_params(labelsize=5)
    cbart1.locator = ticker.MaxNLocator(nbins=nb)
    cbart1.update_ticks()
print(np.shape(imaget1))
# if mode == 0:
#     plt.show()
# elif mode == 1:
#     plt.savefig(cond + '_' + cond2 + '.png', dpi=300)

# lfp heatmap

l1_fig = plt.figure(1, figsize=(10, 5), dpi=200)
l1_fig.patch.set_facecolor(cct)

l1_axs1 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.07, right=0.226,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))

l1_axs2 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.256, right=0.412,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
l1_axs3 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.442, right=0.598,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
l1_axs4 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.628, right=0.784,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
l1_axs5 = l1_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.814, right=0.97,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
# axs1[0][0].set_title('hey''70')
l1_axs = [l1_axs1, l1_axs2, l1_axs3, l1_axs4, l1_axs5]

# fig.suptitle('Multiple images')


imagel1 = []

for j in range(len(lvlc)):
    for i in range(len(ch)):
        nn = nnc.lists[condc][0]
        ct = nnc.lists[condc][1]
        tspn = nnml[nn][lvlc[j]]
        tspc = nnml[ct][lvlc[j]]
        aaxn = l1_axs[j][i, 0]
        aaxc = l1_axs[j][i, 1]
        # print('hey', tspc[i])
        plott(aaxn, tspn[ch[i]], imagel1)
        plott(aaxc, tspc[ch[i]], imagel1)

        # lines for the gap
        for axes in [aaxn, aaxc]:
            if condc == 'nnm_3_0_05':
                for p in [10, 14]:
                    axes.axhline(y=p, color=ccl, linestyle='-.', lw=0.5)
            else:
                for p in [8, 16]:
                    axes.axhline(y=p, color=ccl, linestyle='-.', lw=0.5)
                # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == 0:
            if i == 2:
                aaxn.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' + '\n\nOctave', fontsize=8)
            else:
                aaxn.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                                fontsize=8)
        else:
            pass

        # x label
        if i == 4:
            aaxn.set_xlabel('t (ms)', fontsize=8)
            aaxc.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)

        # subplot title
        if i == 0:
            aaxn.title.set_text('NN')
            aaxc.title.set_text('STRF')

# heatmap normalization
vminl = np.around(min(image.get_array().min() for image in imagel1),
                  decimals=2)
vmaxl = np.around(max(image.get_array().max() for image in imagel1),
                  decimals=2)
print(vminl, vmaxl)
norml1 = colors.Normalize(vmin=vminl, vmax=vmaxl)

for im in imagel1:
    im.set_norm(norml1)

for k in range(len(lvlc)):
    cbarl = l1_fig.colorbar(imagel1[k], ax=l1_axs[k],
                            orientation='horizontal',
                            fraction=.03)
    cbarl.ax.tick_params(labelsize=5)
    cbarl.locator = ticker.MaxNLocator(nbins=nb)
    cbarl.update_ticks()

# frequency profile

f1_fig = plt.figure(2, figsize=(10, 5), dpi=200)
f1_fig.patch.set_facecolor(cct)
f1_axs = f1_fig.subplots(len(ch), 5, gridspec_kw=dict(wspace=0.5, hspace=0.3))

# k = np.mean(p, axis=2)

for j in range(len(lvlc)):
    for i in range(len(ch)):
        fa = f1_axs[i, j]
        nn = nnc.lists[condc][0]
        ct = nnc.lists[condc][1]
        tspn = nnmf[nn][lvlc[j]]
        tspc = nnmf[ct][lvlc[j]]

        fa.plot(octs, tspn[ch[i]], label='NN', lw=1)
        fa.plot(octs, tspc[ch[i]], label='strf', lw=1)
        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_yticks([0.000, 0.025, 0.050, 0.075, 0.100])
        fa.set_ylim(top=ylc)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 4})
        fa.tick_params(axis='both', which='major', labelsize=4.5, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)
        if condc == 'nnm_3_0_05':
            for p in [-0.25, 0.25]:
                fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)
        else:
            for p in [-0.5, 0.5]:
                fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == 0:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                          fontsize=8)

# frequency profile-lfp

fl1_fig = plt.figure(2, figsize=(10, 5), dpi=200)
fl1_fig.patch.set_facecolor(cct)
fl1_axs = fl1_fig.subplots(len(ch), 5, gridspec_kw=dict(wspace=0.5,
                                                        hspace=0.3))

# k = np.mean(p, axis=2)

for j in range(len(lvlc)):
    for i in range(len(ch)):
        fb = fl1_axs[i, j]
        nn = nnc.lists[condc][0]
        ct = nnc.lists[condc][1]
        tspn = nnmlf[nn][lvlc[j]]
        tspc = nnmlf[ct][lvlc[j]]

        fb.plot(octs, tspn[ch[i]], label='NN', lw=1)
        fb.plot(octs, tspc[ch[i]], label='strf', lw=1)
        fb.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        # fa.set_yticks([0.000, 0.025, 0.050, 0.075, 0.100])
        fb.set_ylim(top=30, bottom=-200)
        fb.set_xlim(left=-1.5, right=1.5)
        fb.legend(prop={'size': 4})
        fb.tick_params(axis='both', which='major', labelsize=4.5, length=0.9,
                       width=0.5)
        fb.grid(True, alpha=0.6, lw=0.5)
        if condc == 'nnm_3_0_05':
            for p in [-0.25, 0.25]:
                fb.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)
        else:
            for p in [-0.5, 0.5]:
                fb.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == 0:
            fb.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                          fontsize=8)

if mode == 0:
    plt.show()
elif mode == 1:
    f_fig.savefig(condc + '_freq' + '.png', dpi=300)

'''
nn with silence
'''

# heatmap

c2_fig = plt.figure(3, figsize=(10, 5), dpi=200)
c2_fig.patch.set_facecolor('#e6e6e6')

c2_axs1 = c2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.07, right=0.270,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))

c2_axs2 = c2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.3, right=0.50,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
c2_axs3 = c2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.53, right=0.730,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
c2_axs4 = c2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.760, right=0.960,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
# c2_axs5 = c2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.814, right=0.97,
#                                                        top=0.90, bottom=0.1,
#                                                        wspace=ws, hspace=hs))
c2_axs = [c2_axs1, c2_axs2, c2_axs3, c2_axs4]

imaget2 = []

for j in range(len(lvln)):
    for i in range(len(ch)):
        nn = nns.lists[condn][0]
        ct = nns.lists[condn][1]
        tspn = nnmt[nn]['nn'][lvln[j]]
        tsps = nnmt[nn]['si'][lvln[j]]
        tspc = nnmt[ct][lvln[j]]
        aaxn = c2_axs[j][i, 0]
        aaxc = c2_axs[j][i, 1]
        aaxs = c2_axs[j][i, 2]
        gtsp = [tspn, tsps, tspc]
        axs = [aaxn, aaxs, aaxc]
        a_lab = ['NN-ON', 'STRF', 'NN-OFF']
        for a in range(len(gtsp)):
            plott(axs[a], gtsp[a][ch[i]], imaget2)
            for p in [8, 16]:
                axs[a].axhline(y=p, color=cct, linestyle='-.', lw=0.5)
                # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')
        if j == 0:
            if i == 2:
                aaxn.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' + '\n\nOctave', fontsize=8)
            else:
                aaxn.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                                fontsize=8)
        else:
            pass
        if i == 4:
            aaxc.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)
        elif i == 0:
            for a in range(len(gtsp)):
                axs[a].set_title(a_lab[a], fontdict=dict(fontweight='bold',
                                                         fontsize=7))

vmint2 = np.around(min(image.get_array().min() for image in imaget2),
                   decimals=2)
# vmin = 0
vmaxt2 = np.around(max(image.get_array().max() for image in imaget2),
                   decimals=2)
print(vmint2, vmaxt2)

normt2 = colors.Normalize(vmin=vmint2, vmax=vmaxt2)
for im in imaget2:
    im.set_norm(normt2)

for k in range(len(lvln)):
    cbart2 = c2_fig.colorbar(imaget2[k], ax=c2_axs[k],
                             orientation='horizontal',
                             fraction=.03)
    cbart2.ax.tick_params(labelsize=5)
    cbart2.locator = ticker.MaxNLocator(nbins=nb)
    cbart2.update_ticks()

# lfp heatmap

l2_fig = plt.figure(4, figsize=(10, 5), dpi=200)
l2_fig.patch.set_facecolor(cct)

l2_axs1 = l2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.07, right=0.270,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))

l2_axs2 = l2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.3, right=0.50,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
l2_axs3 = l2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.53, right=0.730,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
l2_axs4 = l2_fig.subplots(len(ch), 3, gridspec_kw=dict(left=0.760, right=0.960,
                                                       top=0.90, bottom=0.1,
                                                       wspace=ws, hspace=hs))
# l2_axs5 = l2_fig.subplots(len(ch), 2, gridspec_kw=dict(left=0.814, right=0.97,
#                                                        top=0.90, bottom=0.1,
#                                                        wspace=ws, hspace=hs))
# axs1[0][0].set_title('hey''70')
l2_axs = [l2_axs1, l2_axs2, l2_axs3, l2_axs4]

# fig.suptitle('Multiple images')


imagel2 = []

for j in range(len(lvln)):
    for i in range(len(ch)):
        nn = nns.lists[condn][0]
        ct = nns.lists[condn][1]
        tspn = nnml[nn]['nn'][lvln[j]]
        tsps = nnml[nn]['si'][lvln[j]]
        tspc = nnml[ct][lvln[j]]
        aaxn = l2_axs[j][i, 0]
        aaxc = l2_axs[j][i, 1]
        aaxs = l2_axs[j][i, 2]
        gtsp = [tspn, tsps, tspc]
        axs = [aaxn, aaxs, aaxc]
        a_lab = ['NN-ON', 'STRF', 'NN-OFF']
        # print('hey', tspc[i])
        plott(aaxn, tspn[ch[i]], imagel2)
        plott(aaxc, tspc[ch[i]], imagel2)

        # lines for the gap
        for a in range(len(gtsp)):
            plott(axs[a], gtsp[a][ch[i]], imagel2)
            for p in [8, 16]:
                axs[a].axhline(y=p, color=ccl, linestyle='-.', lw=0.5)
                # aaxc.axvline(0/home/bhc/codes/spikes_classics.2, 0, 1, label='pyplot vertical line')
        if j == 0:
            if i == 2:
                aaxn.set_ylabel(
                    depth[i] + r'$\mu$' + 'm' + '\n\nOctave', fontsize=8)
            else:
                aaxn.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                                fontsize=8)
        else:
            pass
        if i == 4:
            aaxc.set_xlabel('t (ms)', fontsize=8)
            # aaxn.xaxis.set_label_coords(1.05, -0.4)
        elif i == 0:
            for a in range(len(gtsp)):
                axs[a].set_title(a_lab[a], fontdict=dict(fontweight='bold',
                                                         fontsize=7))
# heatmap normalization
vminl2 = np.around(min(image.get_array().min() for image in imagel2),
                   decimals=2)
vmaxl2 = np.around(max(image.get_array().max() for image in imagel2),
                   decimals=2)
print(vminl, vmaxl)
norml2 = colors.Normalize(vmin=vminl2, vmax=vmaxl2)

for im in imagel2:
    im.set_norm(norml2)

for k in range(len(lvln)):
    cbarl2 = c2_fig.colorbar(imagel2[k], ax=l2_axs[k],
                             orientation='horizontal',
                             fraction=.03)
    cbarl2.ax.tick_params(labelsize=5)
    cbarl2.locator = ticker.MaxNLocator(nbins=nb)
    cbarl2.update_ticks()

# frequency profile
f2_fig = plt.figure(5, figsize=(10, 5), dpi=200)
f2_fig.patch.set_facecolor(cct)
f2_axs = f2_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.5, hspace=0.3))

# k = np.mean(p, axis=2)


for j in range(len(lvln)):
    for i in range(len(ch)):
        fa = f2_axs[i, j]
        nn = nns.lists[condn][0]
        ct = nns.lists[condn][1]
        wn = nns.lists[condn][2]
        tspn = nnmf[nn]['nn'][lvln[j]]
        tsps = nnmf[nn]['si'][lvln[j]]
        tspc = nnmf[ct][lvln[j]]
        tswn = nnmf[wn]['nn'][lvln[j]]
        tsws = nnmf[wn]['si'][lvln[j]]
        gtsp = [tspn, tsps, tspc, tswn, tsws]
        g_lab = ['NN-ON', 'NN-OFF', 'STRF', 'WN-ON', 'WN-OFF']
        for g in range(len(gtsp)):
            fa.plot(octs, gtsp[g][ch[i]], label=g_lab[g], lw=1)

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_ylim(top=yln)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 3}, bbox_to_anchor=(1.3, 1.05))

        fa.tick_params(axis='both', which='major', labelsize=4.5, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == 0:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                          fontsize=8)

# frequency profile-lfp

fl2_fig = plt.figure(5, figsize=(10, 5), dpi=200)
fl2_fig.patch.set_facecolor(cct)
fl2_axs = fl2_fig.subplots(len(ch), 4, gridspec_kw=dict(wspace=0.5,
                                                        hspace=0.3))

# k = np.mean(p, axis=2)

for j in range(len(lvln)):
    for i in range(len(ch)):
        fa = fl2_axs[i, j]
        nn = nns.lists[condn][0]
        ct = nns.lists[condn][1]
        wn = nns.lists[condn][2]
        tspn = nnmf[nn]['nn'][lvln[j]]
        tsps = nnmf[nn]['si'][lvln[j]]
        tspc = nnmf[ct][lvln[j]]
        tswn = nnmf[wn]['nn'][lvln[j]]
        tsws = nnmf[wn]['si'][lvln[j]]
        gtsp = [tspn, tsps, tspc, tswn, tsws]
        g_lab = ['NN-ON', 'NN-OFF', 'STRF', 'WN-ON', 'WN-OFF']
        for g in range(len(gtsp)):
            fa.plot(octs, gtsp[g][ch[i]], label=g_lab[g], lw=1)

        fa.set_xticks([-1.5, -1., -0.5, 0, 0.5, 1., 1.5])
        fa.set_ylim(top=30, bottom=-200)
        fa.set_xlim(left=-1.5, right=1.5)
        fa.legend(prop={'size': 3}, bbox_to_anchor=(1.3, 1.05))

        fa.tick_params(axis='both', which='major', labelsize=4.5, length=0.9,
                       width=0.5)
        fa.grid(True, alpha=0.6, lw=0.5)

        for p in [-0.5, 0.5]:
            fa.axvline(x=p, color=ccl, linestyle='-.', lw=0.5)

        if j == 0:
            fa.set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n ',
                          fontsize=8)

figures1 = [c1_fig, l1_fig, f1_fig, fl1_fig]
figures2 = [c2_fig, l2_fig, f2_fig, fl2_fig]
# figures1 = [f1_fig]
# figures2 = [f2_fig]
names = ['hmap', 'lfp', 'freq', 'freq_lfp']
# names = ['freq_lfp']
save_f = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/image' \
         '/data/average/averages/'
if mode == 0:
    plt.show()
elif mode == 1:
    for i in range(len(names)):
        figures1[i].savefig(save_f + condc + '_' + names[i] + '.png', dpi=200)
        figures2[i].savefig(save_f + condn + '_' + names[i] + '.png', dpi=200)
