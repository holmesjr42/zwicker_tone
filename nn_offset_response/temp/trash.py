import  numpy as np
import matplotlib.pyplot as plt
import pylustrator
pylustrator.start()

nn_s = [56.25, 64.29, 53.33, 76.92]
wn_s = [37.50, 35.71, 53.33, 53.85]
nn_l = [50.00, 92.86, 46.67, 61.54]
wn_l = [25.00, 42.86, 33.33, 38.46]
nns = [nn_s, nn_l]
wns = [wn_s, wn_l]

name = ['NN', 'WN']
cond = [
    '3 s / 1 s\n70 dB', '3 s / 1 s\n60 dB',
    '1 s / 1 s\n70 dB', '1 s / 1 s\n60 dB'
    ]
db = ['70', '60']
data = ['spk', 'lfp']
b_fig = plt.figure(0, figsize=(9, 9))
b_axs = b_fig.subplots(2, 1)

x = np.arange(len(nn_s))
width = 0.35

for i in range(len(data)):
    nn = b_axs[i].bar(x - width/2, nns[i], width, label=name[0],
                      color='tab:blue')
    wn = b_axs[i].bar(x + width/2, wns[i], width, label=name[1],
                      color='tab:orange')

    b_axs[i].set_xticks([0, 1, 2, 3])
    b_axs[i].set_xticklabels(cond)
    b_axs[i].set_yticks([0, 25, 50, 75, 100])
    b_axs[i].text(0.5, 1, data[i],
                 horizontalalignment='center',
                 verticalalignment='center',
                 # rotation='vertical',
                 transform=b_axs[i].transAxes,
                 fontdict={'weight': 'bold', 'size': 23}
                 )
b_axs[1].legend(prop={'size': 15}, loc='upper right', bbox_to_anchor=(1, 1))

#% start: automatic generated code from pylustrator
plt.figure(0).ax_dict = {ax.get_label(): ax for ax in plt.figure(0).axes}
import matplotlib as mpl
plt.figure(0).axes[0].texts[0].set_position([0.500000, 1.044444])
plt.figure(0).axes[1].set_position([0.125000, 0.062222, 0.775000, 0.350000])
plt.figure(0).axes[1].texts[0].set_position([0.500000, 1.050794])
#% end: automatic generated code from pylustrator
plt.show()