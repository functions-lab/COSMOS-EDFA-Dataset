 ###############################################
# all the external libs for EDFA postprocessing 
###############################################

# data
import numpy as np
import pandas as pd
import scipy.stats as stats
import json,copy
from collections import defaultdict
import statistics
import shutil

# MISC
import math,os,shutil,fnmatch
import datetime,pprint
import matplotlib.pyplot as plt

####################
# DEFAULT CONFIGURATIONS
####################

# basic configuration
colorLabel = ['red','green','blue','black','yellow','olive','brown','purple']

CHANNEL_TYPES = ["fix","extraLow","random","extraRandom"]
EDFA_TYPES_TO_GAINS ={
    "booster":["15dB","18dB","21dB"],
    "preamp":["15dB","18dB","21dB","24dB","27dB"]
}
pp = pprint.PrettyPrinter(indent=4)

####################
# HELPER FUNCTIONS
####################

# add files paths both works for linux and windows
# input: [base_folder,subfolder1,subfolder2,subfolder3,target_file]
# output:"base_folder/subfolder1/.../target_file"
def get_path_to_file(folderList):
    return os.path.join(*folderList)

def getJsonData(fileName):
    with open(fileName, "r") as read_file:
        data = json.load(read_file)
    return data['measurement_data']    

def matchFile(pattern, foler):
    # match one file in the folder
    # example usage:
    # result = matchFile('*rdm1-co1*.json', '.../15dB/extraRandom/')
    # result is the full path 
    for file in os.listdir(foler):
        if fnmatch.fnmatch(file, pattern):
            return os.path.join(foler, file)


# other configuration
DATASET_PATH = get_path_to_file(["..","dataset"])
