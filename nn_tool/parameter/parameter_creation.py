import numpy as np
import pickle

# remove cr35
# import scipy.fftpack as ft

# frequency list creation
# f_path = '/home/bhc/codes/spikes_classics/parameters/'
#
# list_freqs = []
#
# for i in np.arange(49):
#     list_freqs.append(np.around(500 * 2 ** (i / 8)))
# np.save(f_path + 'list_freq.npy', list_freqs)
'''
file dataset coordination
'''
# d_animal: the animal which has the data with that SPLdB and that protocol
#           e.g. animal which nas nnm_3_0 at multi-tone pip 60 dB SPLdB
# datas: the coordination of the data set for that specific multi-tone pip
#        SPLdB and that protocol. First, use d_animal to pick the animal
#        which has that specific condition data and choose datas with the
#        specific condition to choose the coordination of that specific data
#        in hdf5 file.
#        e.g. if you want to have lfp cr50 nnm_3_1 50 dB,it will be a_l[5][
#        2] (a_l[animal coordination][SPLdB coordination]
# instead of removing the coordination, I fill up the data file
# coordination that does exist with NaN
# not exist
nan = np.nan

f_path = '/home/bhc/codes/spikes_classics/parameters'

d_animal = {'nnm_3_0': [  # coordination of a sample in each condition
    [
        0, 1, 2, 3, 4, 5, 6, nan,
        nan, 9, 10, 11, 12, nan, nan, nan,
        nan, nan, nan
    ],
    [
        nan, nan, 2, 3, 4, 5, nan, nan,
        nan, 9, 10, 11, 12, nan, 14, nan,
        nan, nan, nan
    ],
    [
        0, 1, 2, 3, 4, 5, 6, nan,
        nan, 9, 10, 11, 12, nan, 14, nan,
        nan, nan, nan
    ],
    [
        nan, 1, 2, 3, 4, 5, 6, nan,
        nan, 9, 10, 11, 12, nan, 14, nan,
        nan, nan, nan
    ],
    [
        0, 1, 2, 3, 4, 5, nan, nan,
        nan, 9, 10, 11, 12, nan, 14, nan,
        nan, nan, nan
    ]
],
    # 'nnm_3_0_05': [[0, nan, 2, 3, 4, 5, nan, nan, nan, 9],
    #                [0, nan, 2, 3, 4, 5, nan, nan, nan, 9],
    #                [0, nan, 2, 3, 4, nan, nan, nan, nan, 9],
    #                [0, nan, 2, 3, 4, 5, nan, nan, nan, 9],
    #                [0, nan, 2, 3, 4, nan, nan, nan, nan, 9]
    #                ],
    # 'nnm_hef': [[0, 1, 2, 3, 4, 5], [0, nan, 2, 3, 4, 5],
    #             [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5],
    #             [nan, nan, nan, nan, 5, nan]],
    # 'nnm_lef': [[0, nan, nan, 3, 4, 5], [0, nan, nan, 3, 4, 5],
    #             [0, nan, nan, 3, 4, 5], [0, nan, nan, 3, 4, 5],
    #             [nan, nan, nan, nan, 5, nan]],
    'nnm_3_1': [
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, 17, 18
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, 17, 18
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, 17, 18
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, 17, 18
        ]
    ],
    'nnm_1_1': [
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            0, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ]
    ],
    # 'nnm_wn_3_0': [[0, nan, 2, nan, 4, nan],
    #                [nan, nan, 2, 3, 4, nan],
    #                [nan, nan, nan, 3, 4, nan],
    #                [nan, nan, nan, 3, nan, nan]],
    'nnm_wn_3_1': [
        [
            nan, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, 5, 6, nan,
            nan, 9, 10, nan, nan, nan, nan, nan,
            nan, nan, nan
        ]
    ],
    'nnm_wn_1_1': [
        [
            nan, nan, 2, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, nan, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 4, 5, 6, nan,
            nan, 9, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ]
    ]
}

datas = {'nnm_3_0': [  # coordination of each spl data in each condition
    [
        0, 0, 0, 0, 0, 0, 0, nan,
        nan, 0, 0, 0, 0, nan, nan, 0,
        0, nan, nan
    ],
    [
        nan, nan, 1, 1, 1, 1, nan, nan,
        nan, 1, 1, 1, 1, nan, 1, nan,
        nan, nan, nan
    ],
    [
        1, 1, 2, 2, 2, 2, 2, nan,
        nan, 2, 2, 2, 2, nan, 2, nan,
        nan, nan, nan
    ],
    [
        nan, 2, 3, 3, 3, 3, 3, nan,
        nan, 3, 3, 3, 3, nan, 3, nan,
        nan, nan, nan
    ]
],
    # 'nnm_3_0_05': [[0, nan, 0, 0, 0, 0, nan, nan, nan, nan],
    #                [1, nan, 1, 1, 1, 1, nan, nan, nan, nan],
    #                [2, nan, 2, 2, 2, nan, nan, nan, nan, nan],
    #                [3, nan, 3, 3, 3, 2, nan, nan, nan, nan],
    #                [4, nan, 4, 4, 4, nan, nan, nan, nan, nan]
    #                ],
    # 'nnm_hef': [[0, 0, 0, 0, 0, 0], [1, nan, 1, 1, 1, 1],
    #             [2, 1, 2, 2, 2, 2], [3, 2, 3, 3, 3, 3],
    #             [nan, nan, nan, nan, 4, nan]],
    # 'nnm_lef': [[0, nan, nan, 0, 0, 0], [1, nan, nan, 1, 1, 1],
    #             [2, nan, nan, 2, 2, 2], [3, nan, nan, 3, 3, 3],
    #             [nan, nan, nan, nan, 4, nan]],
    'nnm_3_1': [
        [
            0, nan, 0, 0, 0, 0, 0, nan,
            nan, 0, 0, nan, nan, nan, nan, nan,
            nan, 0, 0
        ],
        [
            1, nan, 1, 1, 1, 1, 1, nan,
            nan, 1, 1, nan, nan, nan, nan, nan,
            nan, 1, 1
        ],
        [
            2, nan, 2, 2, 2, 2, 2, nan,
            nan, 2, 2, nan, nan, nan, nan, nan,
            nan, 2, 2
        ],
        [
            3, nan, 3, 3, 3, 3, 3, nan,
            nan, 3, 3, nan, nan, nan, nan, nan,
            nan, 3, 3
        ]
    ],
    'nnm_1_1': [[
        0, nan, 0, 0, 0, 0, 0, nan,
        nan, 0, nan, nan, nan, nan, nan, nan,
        nan, nan, nan
    ],
        [
            1, nan, 1, 1, 1, 1, 1, nan,
            nan, 1, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            2, nan, 2, 2, 2, 2, 2, nan,
            nan, 2, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            3, nan, 3, 3, 3, 3, 3, nan,
            nan, 3, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
    ],
    # 'nnm_wn_3_0': [[0, nan, 0, 0, nan], [nan, nan, 1, 0, 1, nan],
    #                [nan, nan, nan, 1, 2, nan],
    #                [nan, nan, nan, 2, nan, nan]],
    'nnm_wn_3_1': [
        [
            nan, nan, 0, 0, 0, 0, 0, nan,
            nan, 0, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 1, 1, 1, 1, nan,
            nan, 1, 1, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 2, 2, 2, 2, nan,
            nan, 2, 2, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 3, 3, 3, nan,
            nan, 3, 3, nan, nan, nan, nan, nan,
            nan, nan, nan
        ]
    ],
    'nnm_wn_1_1': [
        [
            nan, nan, 0, 0, 0, 0, 0, nan,
            nan, 0, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 1, 1, 1, 1, nan,
            nan, 1, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 2, 2, nan, 2, nan,
            nan, 2, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ],
        [
            nan, nan, nan, 3, 3, 2, 3, nan,
            nan, 3, nan, nan, nan, nan, nan, nan,
            nan, nan, nan
        ]
    ]
}

d_strf = {'nnm_3_0': [
    'strf_1', 'strf_1', 'strf_1', 'strf_1', 'strf_4',
    'strf_6', 'strf_1', nan, nan, 'strf_1',
    'strf_1', 'strf_1', 'strf_1', nan, 'strf_1',
    nan, nan, nan, nan
],
    # 'nnm_3_0_05': ['strf_1', nan, 'strf_1', 'strf_2', 'strf_3',
    #                'strf_6', nan, nan, nan
    #                ],
    # 'nnm_hef': ['strf_1', 'strf_1', 'strf_2', 'strf_4',
    #             'strf_1', 'strf_5'],
    # 'nnm_lef': ['strf_1', 'strf_1', 'strf_2', 'strf_4',
    #             'strf_2', 'strf_5'],
    'nnm_3_1': [
        'strf_1', nan, 'strf_1', 'strf_2', 'strf_5',
        'strf_3', 'strf_2', nan, nan, 'strf_2',
        'strf_2', nan, nan, nan, nan,
        nan, nan, 'strf_4', 'strf_1'
    ],
    'nnm_1_1': [
        'strf_1', nan, 'strf_2', 'strf_4', 'strf_6',
        'strf_4', 'strf_3', nan, nan, 'strf_3',
        nan, nan, nan, nan, nan,
        nan, nan, nan, nan
    ]
}

# best f for each animal
bf = [
    6727, 9514, 8724, 5657, 7336,
    8000, 2594, 20749, 1834, 8724,
    8000, 2378, 8000, 5657, 16000,
    16000, 6727, 11314, 11314
]

# activity time window for each animal
# tw = [[21, 35], [21, 28], [21, 30], [17, 25], [18, 31], [15, 25]]
# tw = [[22, 30], [21, 25], [20, 24], [18, 23], [13, 20], [16, 20]]
# I use 10 - 30 ms time window for all of my animals

tw = [
    [22, 30], [21, 25], [20, 24], [18, 23], [13, 20],
    [16, 20], [10, 20], nan, nan, [21, 40],
    [20, 30], [20, 30], [20, 30], nan, [20, 30],
    nan, nan
]

# tw = [
#     [10, 30], [10, 30], [10, 30], [10, 30], [10, 30],
#     [10, 30], [10, 30], nan, nan, [10, 30]
#     ]

lv = ['70', '60', '50', '40']

coord = {'animal': d_animal, 'datas': datas, 'bf': bf, 'tw': tw, 'lv': lv,
         'd_strf': d_strf}
with open('animal_dB_coord.pk', 'wb') as a_coord:
    pickle.dump(coord, a_coord, protocol=pickle.HIGHEST_PROTOCOL)

# with open(f_path + '/' + 'animal_dB_coord.pk',
#           'rb') as a_coord:
#     a = pickle.load(a_coord)
#
# b = a['animal']['nnm_3_1'][2][3]
