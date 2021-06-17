import numpy as np
import pickle
from matplotlib import colors
import matplotlib.pyplot as plt

# k = "dataset/tsp/cr33_190321_tsp.hdf5"

# def update(changed_image):
#     for im in images:
#         if (changed_image.get_cmap() != im.get_cmap()
#                 or changed_image.get_clim() != im.get_clim()):
#             im.set_cmap(changed_image.get_cmap())
#             im.set_clim(changed_image.get_clim())
#
#
# for im in images:
#     im.callbacksSM.connect('changed', update)
# plt.show()
# creating time index for nn condition. [0]: lower boundary, [1] higher
# boundary
#
# nn31 = [np.arange(0, 176001, 4000), np.arange(4000, 180001, 4000)]
# nn11 = [np.arange(0, 178001, 4000), np.arange(2000, 180001, 4000)]
#
# nn_index = {'nn31': nn31, 'nn11': nn11}
#
# with open('/home/bhc/codes/spike_snakemake/parameters/nn_index.pk',
#           'wb') as a:
#     pickle.dump(nn_index, a, protocol=pickle.HIGHEST_PROTOCOL)

# rep = np.size(ind[0])
# ind_l = ind[0] * (sr_lfp / 1000)
# ind_h = ind[1] * (sr_lfp / 1000)
# for i in range(16):
#     for j in range(rep):
#         l_seg[i].append(lfp[i][np.int(ind_l[j]):
#                                np.int(ind_h[j] + 200) + 1])
# return l_seg

with open('/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data'
          '/average_tsp.pk', 'rb') as a:
    k = pickle.load(a)
print(k['nnm_3_1']['si']['60'][0][3])