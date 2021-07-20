import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
from parameter import parameters as pm
import seaborn as sns
import h5py
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import quantities as pq
from tools import icsd

sys.path.pop(1)

com = pm.Commonfeat
db = com.db
sr_lfp = 1061.5 * pq.Hz
coord = np.arange(0, 1501, 100) * pq.micrometer
sigma = 1 / (100 * pq.micrometer)

val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')

ccmap = val.values()[-1]
lcmap = val2.values()[-1]

def animal_name(file_input):
    name = file_input.split('/')[-1].split('_')[0]
    return name


def pop_lvl(animal, data, cond):
    cat = list(data.keys())
    if 'all' in animal:
        for i in cat:
            for j in cond:
                if '30' in list(data[cat[0]].keys()):
                    data[cat[i]][j].pop('30')

                else:
                    pass

    else:
        print('nothing to pop')
        pass

    return data


def db_lv(data):
    """
    :param data: the data which contains the SPL dB dict
    :return: The SPL dB actually included in the data
    """
    lv_list = []
    lvl = com.db['lv']  # SPLdB list
    for i in range(len(lvl)):
        if not np.any(data[lvl[i]][0]):
            continue
        else:
            lv_list.append(lvl[i])
    return lv_list


# function for nnm plotting
# function for nnm plotting
def nnm_plot(aax, dats, imag, cm, type='octave', cf=0):

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

    if type == 'octave':
        aax.tick_params(axis='both', which='major', labelsize=18, length=6,
                        width=1.5)
        aax.tick_params(axis='both', which='minor', labelsize=10, length=4,
                        width=1)
        img = aax.imshow(
            dats, cmap=cm, aspect=100 / 3,
            extent=[0, 100, 1.5, -1.5], interpolation='gaussian')
        imag.append(img)

        # notch line
        for p in [-0.5, 0.5]:
            aax.axhline(y=p, color='white', linestyle='-.', lw=1)
        # plt.subplots_adjust(wspace=.001)
        aax.set_xticks(np.linspace(0, 100, 5, endpoint=True), minor=True)
        aax.set_xticks(np.linspace(0, 100, 3, endpoint=True))
        # aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
        aax.set_yticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5], minor=True)
        aax.set_yticks([-1., 0., 1.])

    elif type == 'frequency':
        aax.tick_params(axis='both', which='major', labelsize=15, length=6,
                        width=1.5)
        aax.tick_params(axis='both', which='minor', labelsize=10, length=4,
                        width=1)
        img = aax.imshow(
            dats, cmap=cm, aspect=100 / 48,
            extent=[0, 100, 48, 0], interpolation='gaussian')
        imag.append(img)

        # notch line
        l_e1 = cf * 2 ** (-0.5)
        h_e1 = cf * 2 ** 0.5

        l_e = int(np.round(8 * np.log2(l_e1 / 500)))
        h_e = int(np.round(8 * np.log2(h_e1 / 500)))

        for p in [l_e, h_e]:
            aax.axhline(y=p, color='white', linestyle='-.', lw=1)
        # plt.subplots_adjust(wspace=.001)
        aax.set_xticks(np.linspace(0, 100, 5, endpoint=True), minor=True)
        aax.set_xticks(np.linspace(0, 100, 3, endpoint=True))
        aax.set_yticks(np.arange(0, 49, 8))
        aax.set_yticklabels([0.5, 1, 2, 4, 8, 16, 32])
        # aax.set_yticks([-1., 0., 1.])

def csd_plot(zz, ax, image, cm):
    zz = zz / zz.units
    sig = zz
    t_ticks = np.linspace(0, 200, 9, endpoint=True)
    t_ticks2 = np.linspace(0, 200, 5, endpoint=True)
    img = ax.imshow(
        sig, cmap=cm, aspect=213 / 1500,
        extent=[0, 200, 1500, 0], interpolation='gaussian')
    # aspect: the number of elements in x-axis
    image.append(img)
    yticks = np.arange(0, 1501, 100)
    yticks2 = np.array([0, 400, 600, 800, 1000, 1200])
    ax.set_yticks(yticks2)
    ax.set_yticks(yticks, minor=True)
    ax.set_xticks(t_ticks, minor=True)
    ax.set_xticks(t_ticks2)
    axins = inset_axes(ax,
                       width="5%",  # width = 5% of parent_bbox width
                       height="100%",  # height : 50%
                       loc='lower left',
                       bbox_to_anchor=(1.1, 0., 1, 1),
                       bbox_transform=ax.transAxes,
                       borderpad=0,
                       )

    ax.tick_params(axis='x', which='major', labelsize=9)
    ax.tick_params(axis='y', which='major', labelsize=9)

# axins = inset_axes(aax,
#                    width="5%",  # width = 5% of parent_bbox width
#                    height="100%",  # height : 50%
#                    loc='lower left',
#                    bbox_to_anchor=(20, 0., 1, 1),
#                    bbox_transform=aax.transAxes,
#                    borderpad=0,
#                    )
# aax.label_outer()
# return aax, axins


# function for frequency profile heatmap
def fph_plot(aax, dats, imag, cm):
    aax.tick_params(axis='both', which='major', labelsize=18, length=6,
                    width=1.5)
    aax.tick_params(axis='both', which='minor', labelsize=10, length=4,
                    width=1)
    # l_depth = [0, 400, 600, 800, 1000, 1200]  # depth point of different layers
    l_depth = [0, 400, 700]  # depth point of supra/gran/infra
    tick_d = np.arange(0, 1501, 300)  # depth point for ticks
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
        dats, cmap=cm, aspect=3 / 1500,
        extent=[-1.5, 1.5, 1500, 0], interpolation='gaussian')
    imag.append(img)

    # notch line
    for p in [-0.5, 0.5]:
        aax.axvline(x=p, color='white', linestyle='-.', lw=1)
    for d in l_depth:
        aax.axhline(y=d, color='white', linestyle='--', lw=1)
    # plt.subplots_adjust(wspace=.001)
    aax.set_yticks(np.linspace(0, 1500, 16, endpoint=True), minor=True)
    aax.set_yticks(tick_d)
    # aax.set_yticks([0, 4, 8, 12, 16, 20, 24])
    aax.set_xticks([-1.5, -1., -0.5, 0., 0.5, 1., 1.5], minor=True)
    aax.set_xticks([-1., 0., 1.])

    # axins = inset_axes(aax,
    #                    width="5%",  # width = 5% of parent_bbox width
    #                    height="100%",  # height : 50%
    #                    loc='lower left',
    #                    bbox_to_anchor=(20, 0., 1, 1),
    #                    bbox_transform=aax.transAxes,
    #                    borderpad=0,
    #                    )
    # aax.label_outer()
    # return aax, axins

# function for time depth with a specific frequency heatmap
def tdh_plot(aax, dats, imag, cm, hc='white'):
    aax.tick_params(axis='both', which='major', labelsize=16, length=6,
                    width=1.5)
    aax.tick_params(axis='both', which='minor', labelsize=10, length=4,
                    width=1)

    l_depth = [0, 400, 700]  # depth point of supra/gran/infra
    tick_d = np.arange(0, 1501, 300)  # depth point for ticks
    # aax.tick_params(axis='both', length=0.9, width=0.5)
    aax.spines['top'].set_visible(False)
    aax.spines['right'].set_visible(False)
    aax.spines['left'].set_visible(False)
    aax.spines['bottom'].set_visible(False)

    for tick in aax.get_xticklabels():
        tick.set_fontname('sans-serif')
    for tick in aax.get_yticklabels():
        tick.set_fontname('sans-serif')
    img = aax.imshow(
        dats, cmap=cm, aspect=101 / 1500, extent=[0, 101, 1500, 0],
        interpolation='gaussian'
        )
    imag.append(img)

    # layer IV line
    for d in l_depth:
        aax.axhline(y=d, color=hc, linestyle='--', lw=1)

    aax.set_yticks(np.linspace(0, 1500, 16, endpoint=True), minor=True)
    aax.set_yticks(tick_d)
    aax.set_xticks([0, 25, 50, 75, 100], minor=True)
    aax.set_xticks([0, 50, 100])
    aax.label_outer()


# unit of a heatmap bar
def cbar_t(cbar, type):
    cbar.ax.tick_params(labelsize=7)
    if type == 'lfp':
        cbar.set_label(
            r'mV',
            labelpad=15, size=9
            )

    elif type == 'tsp':
        cbar.set_label(
            r'% Firing rate',
            labelpad=15, size=9
            )


# normalize the heatmap
def norm_color(img, types, ratio):
    """
    Normalize the heatmap for firing rate/lfp
    :param img: img list from plotting. Check individual nnm_*_sp_lfp script
    and search img
    :param types: type of the data. Either 'lfp' or 'tsp'
    :param ratio: ratio to adjust the max/min value for the heatmap
    :return: max value of the heatmap for the spike colorbar
    """

    if types == 'lfp':
        # vmax = np.round(
        #     max(ims.get_array().max() for ims in img) * ratio, decimals=2
        #     )
        vmin = np.round(
            min(ims.get_array().min() for ims in img) * ratio, decimals=2
            )
        vmax = -vmin
        norm = colors.TwoSlopeNorm(vcenter=0, vmin=vmin, vmax=vmax)

    elif types == 'spk':
        vmin = 0
        vmax = np.round(
            max(ims.get_array().max() for ims in img) * ratio, decimals=-1
            )
        print(vmax)
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    elif types == 'csd':
        vmax = max(
            max(ims.get_array().max() for ims in img),
            np.abs(min(ims.get_array().min() for ims in img))
            ) * ratio
        vmin = (-1) * vmax
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    elif types == 'd_spk':
        mx = np.round(
            max(ims.get_array().max() for ims in img) * ratio, decimals=-1
            )
        mn = np.round(
            min(ims.get_array().min() for ims in img) * ratio, decimals=-1
            )
        vmax = np.max([np.abs(mx), np.abs(mn)])
        vmin = -vmax
        norm = colors.TwoSlopeNorm(vcenter=0, vmin=vmin, vmax=vmax)

    elif types == 'd_lfp':
        mx = np.round(
            max(ims.get_array().max() for ims in img) * ratio, decimals=2
            )
        mn = np.round(
            min(ims.get_array().min() for ims in img) * ratio, decimals=2
            )
        vmax = np.max([np.abs(mx), np.abs(mn)])
        vmin = -vmax
        norm = colors.TwoSlopeNorm(vcenter=0, vmin=vmin, vmax=vmax)

    else:
        print('there is a problem with norm_color. check it')
        raise ValueError

    for ims in img:
        ims.set_norm(norm)

    return vmin, vmax


def nnm_labels(aaxs, notch, lvp, depth, ch, j, i):
    """
    This is the function specifically for minor plot setup for heatmap strf
    part
    :param aaxs: list of axes for notch, control, or white noise
    :param notch: width of the notch
    :param lvp: SPL list you are using for this plot
    :param depth: depth from parameters/parameters
    :param ch: channel list from parameters/ch
    :param j: order of lvp for loop
    :param i: order of len(ch) for loop
    :return:
    """
    if len(aaxs) == 2:
        # lines for the gap
        for axes in aaxs:
            for p in [-notch, notch]:
                axes.axhline(y=p, color='white', linestyle='-.', lw=0.6)
            # aaxc.axvline(0.2, 0, 1, label='pyplot vertical line')

        # y lables
        if j == lvp[0]:
            aaxs[1].set_ylabel(depth[i] + r'$\mu$' + 'm' + '\n\n\n\n\n\n ',
                               fontsize=10)
        else:
            pass

        # x label
        if i == len(ch) - 1:
            aaxs[1].text(1, -0.4, 't (ms)',
                         horizontalalignment='center',
                         verticalalignment='center',
                         # rotation='vertical',
                         transform=aaxs[1].transAxes,
                         fontdict={'weight': 'bold', 'size': 11}
                         )
        # subplot title
        elif i == 0:
            aaxs[0].title.set_text('NN')
            aaxs[1].title.set_text('Control')
        else:
            pass


def colorbar_set(fig, axs, img, types, vmax=0, vmin=0, ori='vertical'):
    """
    This is a function for minor colorbar setups
    :param fig: name of the main figure (e.g. c1_fig)
    :param axs: column / row of a subplot
    :param vmax: the maximum of the colorbar
    # :param lvi: the first element of lvp. Just to pick the coordination of
    fig text
    :param img: img list for current loop heatmap setups. Check c_img or l_img
    from nnm_*_sp_lfp script
    :param types: the type of the data. Either 'lfp' or 'tsp'
    :return:
    """
    if types == 'lfp':
        ticklist = [vmin, 0, vmax]
        cbart = fig.colorbar(
            img, ax=axs,
            orientation=ori,
            format='%.2f',
            fraction=0.02,
            ticks=ticklist
            )
        cbart.set_label('Amplitude ' + r'(mV)', labelpad=5, size=18)

    elif types == 'spk':
        ticklist = np.linspace(0, vmax, 3, endpoint=True)
        cbart = fig.colorbar(
            img, ax=axs,
            orientation=ori,
            format='%.0f',
            fraction=0.02,
            ticks=ticklist
            )
        cbart.set_label('Firing rate (spk / s)', labelpad=5, size=18)

    elif types == 'csd':
        ticklist = [vmin, 0, vmax]
        cbart = fig.colorbar(
            img, ax=axs,
            orientation=ori,
            format='%.1f',
            fraction=0.02,
            ticks=ticklist
            )
        cbart.set_label(r'mV/$mm^{2}$', labelpad=5, size=18)

    elif types == 'd_spk':
        ticklist = [vmin, 0, vmax]
        cbart = fig.colorbar(
            img, ax=axs,
            orientation=ori,
            format='%.0f',
            fraction=0.02,
            ticks=ticklist
            )
        cbart.set_label('Firing rate (spk / s)', labelpad=5, size=18)

    elif types == 'd_lfp':
        ticklist = [vmin, 0, vmax]
        cbart = fig.colorbar(
            img, ax=axs,
            orientation=ori,
            format='%.2f',
            fraction=0.02,
            ticks=ticklist
            )
        cbart.set_label('Amplitude ' + r'(mV)', labelpad=5, size=18)

    else:
        print('you did not choose the data type for colorbar_set.')
        raise ValueError

    cbart.ax.tick_params(labelsize=18)
    cbart.update_ticks()

def csd_calc(x, f_type, f_order):
    std_input = {
        'lfp': x,
        'coord_electrode': coord,
        'sigma': sigma,
        'f_type': f_type,
        'f_order': f_order
        }

    std = icsd.estimate_csd(**std_input)

    f_csd = np.transpose(std[1] / std[1].units) * std[1].units
    f_csd.units = pq.mV / (pq.mm ** 2)
    # print(f'unit conversion {std[1].units} to {f_csd.units}')
    return f_csd

def heat_plot(x, axs, img, type='lfp', zoom='no', z_range=None, z_img=None):
    if type == 'lfp':
        clmap = lcmap
        hcolor = 'white'
    elif type == 'csd':
        clmap = ccmap
        hcolor = 'k'
    else:
        raise ValueError("you didn't choose which data type you are plotting.")

    x = x / x.units

    # time axis tick
    t_ticks = np.linspace(0, 200, 9, endpoint=True)
    t_ticks2 = np.linspace(0, 200, 5, endpoint=True)

    # depth axis tick
    yticks = np.arange(0, 1501, 100)
    yticks2 = np.array([0, 400, 600, 800, 1000, 1200])

    imag = axs.imshow(
        x, cmap=clmap, aspect=213 / 1500,
        extent=[0, 200, 1500, 0], interpolation='gaussian'
        )
    img.append(imag)
    # aspect: the number of elements in x-axis

    axs.set_yticks(yticks2)
    axs.set_yticks(yticks, minor=True)
    axs.set_xticks(t_ticks, minor=True)
    axs.set_xticks(t_ticks2)

    axs.tick_params(axis='both', which='major', labelsize=18, length=6,
                    width=2)
    axs.tick_params(axis='both', which='minor', labelsize=10, length=4,
                    width=1.5)
    # lines
    l_depth = [400, 700]  # depth point of supra/gran/infra
    for d in l_depth:
        axs.axhline(y=d, color=hcolor, linestyle='--', lw=1.5)
    if zoom == 'yes':
        axins = zoomed_inset_axes(axs, 1.5, loc=1)
        # zoom area mark
        patch, pp1, pp2 = mark_inset(
            axs, axins, loc1=2, loc2=2, fc="none", ec="0.5"
            )
        pp1.loc1 = 2
        pp1.loc2 = 3
        pp2.loc1 = 3
        pp2.loc2 = 2
        z_imag = axins.imshow(x, cmap=clmap, aspect=213 / 1500,
                             extent=[0, 200, 1500, 0],
                             interpolation='gaussian')
        z_img.append(z_imag)
        axins.set_yticks(yticks2)
        axins.set_yticks(yticks, minor=True)
        axins.set_xticks(t_ticks, minor=True)
        axins.set_xticks(t_ticks2)
        axins.set_xlim(z_range[0], z_range[1])
        axins.set_ylim(z_range[2], z_range[3])
        axins.tick_params(axis='both', which='both', direction="in")
        plt.xticks(visible=False)
        plt.yticks(visible=False)
        # axins.tick_params(axis='both', which='major', length=5)
        # axins.tick_params(axis='both', which='minor', length=2.5)