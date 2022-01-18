import os
import pathlib
import platform

import numpy as np
import pickle

from matplotlib.colors import ListedColormap
import seaborn as sns

# assigning paths for the tool and data directories.
data_path = 'OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/'
param_path_ = pathlib.Path(__file__).parents[2] / "nn_tool/parameter"
param_path = str(param_path_)


def data_path_selection():
    if platform.node() == 'DESKTOP-K2A53B8':
        partition = 'D:/'
    elif platform.node() == 'DESKTOP-SDAA-AURORA':
        if platform.system() == 'Windows':
            partition = 'D:/'
        else:
            raise ValueError(
                f'This script is not available for the system {platform.system()}'
                f'in {platform.node()}'
                )
    else:
        raise ValueError('There is no partition for the data path.')
    return partition


partition = data_path_selection()
file_path = os.path.join(partition, data_path)

sr_lfp = 1061.48  # lfp sampling rate, Hz


class Commonfeat:
    with open(param_path + '/animal_dB_coord.pk',
              'rb') as a_coord:
        db = pickle.load(a_coord)

    list_freq = np.load(param_path + '/list_freq.npy', allow_pickle=True)

    # any other variables are included in spike_tools
    f_path = file_path

    # animal/data folder name
    animals = ['cr29_190228', 'cr30_190305', 'cr31_190312', 'cr33_190321',
               'cr50_190724', 'cr79_200211', 'cr90_201023', 'cr92_201029',
               'cr93_201110', 'cr94_201112', 'cr95_201117']

    p_info = np.load(param_path + '/time_index_multi_tones_500ms_180s.npy',
                     allow_pickle=True)

    octaves = np.array(
        [-1.5, -1.38, -1.25, -1.13, -1, -0.88, -0.75, -0.63, -0.5,
         -0.37, -0.25, -0.13, 0, 0.12, 0.25, 0.38, 0.5, 0.63, 0.75,
         0.87, 1, 1.12, 1.25, 1.37, 1.5])

    # best f for each animal
    bf = [6727, 9514, 8724, 5657, 2828,
          7336, 8000, 2594, 20749, 1834,
          8724, 8000
          ]
    # best f dict
    bf_dic = {
        'cr29': 6727, 'cr30': 9514, 'cr31': 8724, 'cr33': 5657,
        'cr50': 7336, 'cr79': 8000, 'cr90': 2594, 'cr92': 20749,
        'cr93': 1834, 'cr94': 8724, 'cr95': 8000, 'cr96': 2378,
        'cr98': 5657, 'cr101': 16000, 'cr102': 16000, 'cr103': 6727,
        'cr121c': 11314, 'cr122b': 11314
        }

    # channel represents supr, gran, infra layer
    ch_l = [3, 7, 11]
    ch_list = [[0, 6], [6, 9], [9, 16]]
    # # activity time window for each animal
    # tw = [[12, 46], [10, 41], [10, 41], [10, 41], [10, 38], [10, 31], [10, 41]]


"""
continuous nn
"""


class Nnmcontfeat:
    # conditions
    conds = ['nnm_3_0']
    # conds = ['nnm_3_0', 'nnm_3_0_05', 'nnm_lef', 'nnm_hef']

    # condition dict
    lists = {
        'nnm_3_0': ['nnm_3_0', 'nnm_3_0_strf']
        # 'nnm_3_0_05': ['nnm_3_0_05', 'nnm_3_0_05_strf']
        # 'nnm_lef': ['nnm_lef', 'nnm_lef_strf'],
        # 'nnm_hef': ['nnm_hef', 'nnm_hef_strf']
        }


"""
nn on-off
"""


class Nnsifeat:
    # timed index for multi-tone pip trigger

    with open(param_path + '/time_index_multi_tones_500ms_180s_nn_si.pk',
              'rb') as pip:
        p_infos = pickle.load(pip)

    p_info31 = {'nn': p_infos['t_index_31_nn'], 'si': p_infos['t_index_31_si']}

    p_info11 = {'nn': p_infos['t_index_11_nn'], 'si': p_infos['t_index_11_si']}

    # conditions
    conds = ['nnm_3_1', 'nnm_1_1', 'nnm_wn_3_1', 'nnm_wn_1_1']

    # condition dicts
    lists = {
        'nnm_3_1': ['nnm_3_1', 'nnm_3_1_strf', 'nnm_wn_3_1'],
        'nnm_1_1': ['nnm_1_1', 'nnm_1_1_strf', 'nnm_wn_1_1'],
        }


class Datas:
    try:
        with open(file_path + 'average_tsp.pk', 'rb') as a:
            nnm_t = pickle.load(a)

        with open(file_path + 'average_lfp.pk', 'rb') as a:
            nnm_l = pickle.load(a)

        with open(file_path + 'average_freq.pk', 'rb') as a:
            nnm_f = pickle.load(a)

    except FileNotFoundError:
        pass


# class Setup:
#     """
#     setup for plotting things
#     """
#
#     def __init__(self, mode=0, yl=0.1, cond=None, cond2=None,
#                  nb=5, ch=None, ws=0.1, hs=0.2, ccmap=None, ratio=0.7,
#                  dm=None):
#         """
#
#         :param cond:
#         :param cond2:
#         :param ch: channels you want to use
#         :param ccmap: color scheme for heatmaps
#         """
#
#         if ch is None:
#             ch = np.array([4, 6, 8, 10, 12])
#         if ccmap is None or ccmap == 'spk':
#             ccmap = ListedColormap(sns.color_palette("mako", 256))
#         elif ccmap == 'lfp':
#             ccmap = ListedColormap(sns.color_palette("icefire", 256))
#             # "vlag" "icefire"
#         elif ccmap == 'csd':
#             ccmap = ListedColormap(sns.color_palette("rainbow_r", 256))
#
#         self.mode = mode
#         self.yl = yl
#         self.cond = cond
#         self.cond2 = cond2
#         self.nb = nb
#         self.ch = ch
#         self.ws = ws
#         self.hs = hs
#         self.ccmap = ccmap
#         self.ratio = ratio
#         self.dm = dm
#
#
#     def values(self):
#         depths = ['0', '100', '200', '300', '400', '500', '600', '700',
#                   '800', '900', '1000', '1100', '1200', '1300', '1400', '1500']
#
#         l_color = ['#e6e6e6', '#4e69ab']
#         cb = '#e6e6e6'
#         cc = 0
#         depth = []
#
#         if self.dm is None:
#             dcmap = sns.color_palette('colorblind').as_hex()
#         else:
#             dcmap = 'jet'
#
#         for i in self.ch:
#             depth.append(depths[i])
#
#         if self.cond2 == 'tsp':
#             cc = l_color[0]
#         elif self.cond2 == 'lfp':
#             cc = l_color[1]
#         else:
#             print('ni nun ong-i-gumung')
#
#         return [self.mode, self.yl, self.cond, self.cond2, self.nb, self.ch,
#                 depth, dcmap, self.ws, self.hs, self.ratio, cc, cb, self.ccmap]
#
#     def extra_setup(self):
#
#         c_n = ['nnm_3_0', 'nnm_3_1', 'nnm_1_1']
#         c_s = ['nnm_3_0_strf', 'nnm_3_1_strf', 'nnm_1_1_strf']
#         c_w = ['nnm_wn_3_1', 'nnm_wn_1_1']
#
#         cnon = ['nnm_3_1_on', 'nnm_1_1_on']
#         cnoff = ['nnm_3_1_off', 'nnm_1_1_off']
#         cwoff = ['nnm_wn_3_1_off', 'nnm_wn_1_1_off']
#
#         cc_s_onoff = ['nnm_3_1_strf', 'nnm_1_1_strf']
#         cw_s_onoff = ['nnm_wn_3_1_strf', 'nnm_wn_1_1_strf']
#
#         layer_name = ['Supragranular\nlayer', 'Granular\nlayer',
#                       'Infragranular\nlayer']
#
#         layer_num = [[0, 6], [6, 9], [9, 16]]  # index for each layer's
#         # start-end points
#
#         l_list = ['supr', 'gran', 'infr']
#
#         freq = [4, 8, 12, 16, 20]  # -1, -0.5, 0, 0.5, 1 octave indice
#
#         f_name = ['Lower edge frq', 'Center frq', 'Higher edge Frq']
#
#         l_style = ['dashdot', '-', 'dashed']
#
#         paradigm = ['Control', 'NN-ON', 'NN-OFF', 'WN-OFF']
#
#         return layer_name, layer_num, l_list, freq, f_name, l_style, \
#                paradigm, c_n, c_s, c_w, cnon, cnoff, \
#                cwoff, cc_s_onoff, cw_s_onoff
#
#     def nn31_plot(self):
#         db_lv = ['70', '60']
#         db_ind = [0, 1]
#
#         dcmap = sns.color_palette('colorblind').as_hex()
#         # color palette of plots
#
#         names = ['nn_3_1', 'nn_wn_3_1']  # for accessing data stored in dict
#
#         legends = [
#             ['NN - ON', 'WN - ON'],
#             ['NN - OFF', 'WN - OFF'],
#             ['NN', 'WN']
#         ]  # for plotting
#
#         ch = [1, 7, 11]  # channel number which represents each layer in
#         # l_list
#
#         l_list = ['supr', 'gran', 'infr']  # list of layers. it represents
#         # supragranular layer, granular layer, infragranular layer following
#         # the list element order.
#
#         layer_name = ['Supragranular\nlayer', 'Granular\nlayer',
#                       'Infragranular\nlayer']  # for plotting
#
#         return db_lv, db_ind, dcmap, names, legends, ch, l_list, layer_name
#
#     def nn11_plot(self):
#         db_lv = ['70', '60']
#         db_ind = [0, 1]
#
#         dcmap = sns.color_palette('colorblind').as_hex()
#         # color palette of plots
#
#         names = ['nn_1_1', 'nn_wn_1_1']  # for accessing data stored in dict
#
#         legends = [['NN - OFF', 'WN - OFF'], ['NN', 'WN']]  # for plotting
#
#         ch = [0, 7, 11]  # channel number which represents each layer in
#         # l_list
#
#         l_list = ['supr', 'gran', 'infr']  # list of layers. it represents
#         # supragranular layer, granular layer, infragranular layer following
#         # the list element order.
#
#         layer_name = ['Supragranular\nlayer', 'Granular\nlayer',
#                       'Infragranular\nlayer']  # for plotting
#
#         return db_lv, db_ind, dcmap, names, legends, ch, l_list, layer_name
class Setup:
    """
    setup for plotting things
    """

    def __init__(self, ch=None, ch_offset=None, hcmap_mode=None, mode=None):
        """
        :param ch: channels you want to use
        :param ch_offset: channels you want to use for offset analysis
        :param hcmap_mode: color scheme for different heatmaps---choose 'spk', 'lfp', or 'csd' for the right color
        :param mode: if you want to have fun, set it 'fun'
        """

        depths = ['0', '100', '200', '300', '400', '500', '600', '700',
                  '800', '900', '1000', '1100', '1200', '1300', '1400', '1500']

        l_color = ['#e6e6e6', '#4e69ab']

        descrete_cmap = None

        depth = []

        hcmap = None
        ref_line_color = None  # line color for axh/axvline for notch band and granular layer

        c_n = ['nnm_3_0', 'nnm_3_1', 'nnm_1_1']
        c_s = ['nnm_3_0_strf', 'nnm_3_1_strf', 'nnm_1_1_strf']
        c_w = ['nnm_wn_3_1', 'nnm_wn_1_1']

        cnon = ['nnm_3_1_on', 'nnm_1_1_on']
        cnoff = ['nnm_3_1_off', 'nnm_1_1_off']
        cwoff = ['nnm_wn_3_1_off', 'nnm_wn_1_1_off']

        cc_s_onoff = ['nnm_3_1_strf', 'nnm_1_1_strf']
        cw_s_onoff = ['nnm_wn_3_1_strf', 'nnm_wn_1_1_strf']

        layer_name = ['Supragranular\nlayer', 'Granular\nlayer',
                      'Infragranular\nlayer']

        layer_num = [[0, 6], [6, 9], [9, 16]]  # index for each layer's
        # start-end points
        l_list = ['supr', 'gran', 'infr']

        freq = [4, 8, 12, 16, 20]  # -1, -0.5, 0, 0.5, 1 octave indice

        f_name = ['Lower edge frq', 'Center frq', 'Higher edge Frq']

        l_style = ['dashdot', '-', 'dashed']

        paradigm = ['Control', 'NN-ON', 'NN-OFF', 'WN-OFF']

        legends = [
            ['NN - ON', 'WN - ON'],
            ['NN - OFF', 'WN - OFF'],
            ['NN', 'WN']
            ]  # for plotting

        # offset setups
        db_lv = ['70', '60']
        db_ind = [0, 1]

        cond_3_1 = ['nn_3_1', 'nn_wn_3_1']
        cond_1_1 = ['nn_1_1', 'nn_wn_1_1']

        self.mode = mode
        self.depths = depths
        self.c_n = c_n
        self.c_s = c_s
        self.c_w = c_w
        self.cnon = cnon
        self.cnoff = cnoff
        self.cwoff = cwoff
        self.cc_s_onoff = cc_s_onoff
        self.cw_s_onoff = cw_s_onoff
        self.layer_name = layer_name
        self.layer_num = layer_num
        self.l_list = l_list
        self.freq = freq
        self.f_name = f_name
        self.l_style = l_style
        self.paradigm = paradigm
        self.legends = legends

        self.db_lv = db_lv
        self.db_ind = db_ind
        self.cond_3_1 = cond_3_1
        self.cond_1_1 = cond_1_1
        if ch is None:
            ch = np.array([4, 6, 8, 10, 12])

        if ch_offset is None:
            ch_offset = [1, 7, 11]

        if mode is None:
            descrete_cmap = sns.color_palette('colorblind').as_hex()
            ref_line_color = 'white'
            if hcmap_mode is None or hcmap_mode == 'spk':
                hcmap = ListedColormap(sns.color_palette("mako", 256))
            elif hcmap_mode == 'lfp':
                hcmap = ListedColormap(sns.color_palette("icefire", 256))
                # "vlag" "icefire"
            elif hcmap_mode == 'csd':
                hcmap = ListedColormap(sns.color_palette("icefire_r", 256))
            else:
                print('You did not choose right option for a color scheme, '
                      'set -ccmap- between spk, lfp, or csd.')

        elif mode == 'fun':
            descrete_cmap = ['cyan', 'magenta', 'yellow', 'lime', 'darkorchid']
            ref_line_color = 'magenta'
            if hcmap_mode is None or hcmap_mode == 'spk':
                hcmap = 'cool'
            elif hcmap_mode == 'lfp':
                hcmap = 'turbo'
                # "vlag" "icefire"
            elif hcmap_mode == 'csd':
                hcmap = 'turbo_r'
            else:
                print('You did not choose the right option for a color '
                      'scheme, set -ccmap- between spk, lfp, or csd.')
                raise ValueError

        else:
            print('You did not choose the right option for the mode. Choose '
                  'fun if you want to have fun')

        for i in ch:
            depth.append(depths[i])

        self.depth = depth
        self.hcmap = hcmap
        self.d_camp = descrete_cmap
        self.ref_line_color = ref_line_color
        self.ch = ch
        self.ch_offset = ch_offset


class Nn:

    def __init(self):
        ind_3_1 = [np.arange(0, 180000 - 4000 + 1, 4000),
                   np.arange(4000, 180000 + 1, 4000)]
        ind_1_1 = [np.arange(0, 180000 - 2000 + 1, 2000),
                   np.arange(2000, 180000 + 1, 2000)]

        names = [
            'nn_3_1', 'nn_wn_3_1', 'nn_1_1', 'nn_wn_1_1',
            'nn_3_1_nt', 'nn_wn_3_1_nt', 'nn_1_1_nt', 'nn_wn_1_1_nt'
            ]
        db = ['70', '60']  # SPL of nn_offset

        l_dat = ['mean', 'q27']  # lfp session mean/confidence interval
        s_dat = ['rastor', 'psth', 's_psth',
                 'time']  # spk session rastor, psths, time

        self.ind_3_1 = ind_3_1
        self.ind_1_1 = ind_1_1
        self.names = names
        self.db = db
        self.l_dat = l_dat
        self.s_dat = s_dat


if __name__ == "__main__":
    st = Setup()
    print(st.depth)
