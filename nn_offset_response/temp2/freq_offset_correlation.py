import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from parameter import parameters as pm
import pylustrator
import matplotlib.pyplot as plt

# pylustrator.start()
sys.path.pop(1)