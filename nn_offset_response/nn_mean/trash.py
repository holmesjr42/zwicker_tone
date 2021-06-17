import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")
print(sys.path)
from tools import spike_tools as st
import h5py
from tools import nn_tool as nt
from parameter import parameters as pm
import numpy as np
import statsmodels.stats.api as sms

sys.path.pop(1)