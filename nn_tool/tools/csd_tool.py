import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
# print(os.path.realpath(pathlib.Path('__init__.py').parent))
# print(os.getcwd())
from tools import icsd
import numpy as np
from parameter import parameters as pm
import quantities as pq
from matplotlib import colors
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.pyplot as plt

sys.path.pop(1)

comm = pm.Commonfeat
db = comm.db
sr_lfp = 1061.5 * pq.Hz
coord = np.arange(0, 1501, 100) * pq.micrometer
sigma = 1 / (100 * pq.micrometer)

val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='csd')
val2 = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1, ccmap='lfp')

ccmap = val.values()[-1]
lcmap = val2.values()[-1]


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

def heat_plot(x, axs, type='lfp', zoom='no', z_range=None):
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

    img = axs.imshow(
        x, cmap=clmap, aspect=213 / 1500,
        extent=[0, 200, 1500, 0], interpolation='gaussian'
        )
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
        z_img = axins.imshow(x, cmap=clmap, aspect=213 / 1500,
                             extent=[0, 200, 1500, 0],
                             interpolation='gaussian')
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
        return [img, z_img]
    else:
        return img
