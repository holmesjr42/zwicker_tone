import numpy as np


def o_cut(cf, option='norm'):

    if option == 'nnm_lef':
        e_c = cf * 2 ** 0.5
        f_h = e_c * 2 ** 1.5
        f_l = e_c * 2 ** (-1.5)
        oct_h = int(np.round(8 * np.log2(f_h / 500)))
        oct_l = int(np.round(8 * np.log2(f_l / 500)))

        return [oct_l, oct_h, e_c]

    elif option == 'nnm_hef':
        e_c = cf * 2 ** (-0.5)
        f_h = e_c * 2 ** 1.5
        f_l = e_c * 2 ** (-1.5)
        oct_h = int(np.round(8 * np.log2(f_h / 500)))
        oct_l = int(np.round(8 * np.log2(f_l / 500)))

        return [oct_l, oct_h, e_c]

    else:
        f_h = cf * 2 ** 1.5
        f_l = cf * 2 ** (-1.5)
        oct_h = int(np.round(8 * np.log2(f_h / 500)))
        oct_l = int(np.round(8 * np.log2(f_l / 500)))

        return [oct_l, oct_h, cf]

'''
This is the function to acquire the octave locations of  spectral gap edges 
and the gap center frequency. The reference point of the octave is 500 Hz as
indicated in the original stimulus matlab script. default, gap width 1 oct, 
gap center, bf; half, gap width, 0.5 oct, gap center, bf; lef, gap width, 
1 oct, gap center, half oct above bf; hef, gap width, 1 oct, gap center, 
half oct below bf.
'''


def o_range(bf, option='norm'):

    if option == 'nnm_3_0_05':
        e_l = bf * 2 ** (-0.25)
        e_h = bf * 2 ** 0.25
        e_c = bf
        o_l = int(np.round(8 * np.log2(e_l / 500)))
        o_h = int(np.round(8 * np.log2(e_h / 500)))
        o_c = int(np.round(8 * np.log2(e_c / 500)))

        return [o_l, o_c, o_h]

    if option == 'nnm_lef':
        e_l = bf
        e_h = bf * 2 ** 1
        e_c = bf * 2 ** 0.5
        o_l = int(np.round(8 * np.log2(e_l / 500)))
        o_h = int(np.round(8 * np.log2(e_h / 500)))
        o_c = int(np.round(8 * np.log2(e_c / 500)))

        return [o_l, o_c, o_h]

    if option == 'nnm_hef':
        e_l = bf * 2 ** (-1)
        e_h = bf
        e_c = bf * 2 ** (-0.5)
        o_l = int(np.round(8 * np.log2(e_l / 500)))
        o_h = int(np.round(8 * np.log2(e_h / 500)))
        o_c = int(np.round(8 * np.log2(e_c / 500)))

        return [o_l, o_c, o_h]

    else:
        e_l = bf * 2 ** (-0.5)
        e_h = bf * 2 ** 0.5
        e_c = bf
        o_l = int(np.round(8 * np.log2(e_l / 500)))
        o_h = int(np.round(8 * np.log2(e_h / 500)))
        o_c = int(np.round(8 * np.log2(e_c / 500)))

        return [o_l, o_c, o_h]