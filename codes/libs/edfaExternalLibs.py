 ###############################################
# all the external libs for EDFA postprocessing 
###############################################

# data
import numpy as np
import pandas as pd
from prettytable import PrettyTable
import scipy.stats as stats
import json,copy
from collections import defaultdict
import statistics

# MISC
import math,os,shutil,fnmatch
import datetime
import matplotlib.pyplot as plt

# ML
try:
    import tensorflow as tf
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow import math as TFmath
except:
    pass 
