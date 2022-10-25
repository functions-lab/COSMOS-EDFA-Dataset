# example code for visualization the EDFA gain spectrum dataset
from .libs.edfa_visual_libs import *
# basic configuration
DATASET_PATH = get_path_to_file(["..","dataset"])
CHANNEL_TYPES = ["fix","extraLow","random","extraRandom"]
EDFA_TYPES_TO_GAINS ={
    "booster":["15dB","18dB","21dB"],
    "preamp":["15dB","18dB","21dB","24dB","27dB"]
}

####################
# SELECT FILES
####################

# add files paths both works for linux and windows
# input: [base_folder,subfolder1,subfolder2,subfolder3,target_file]
# output:"base_folder/subfolder1/.../target_file"
def get_path_to_file(folderList):
    return os.path.join(*folderList)

# return edfaType ("booster"), gain ("18dB"), channelType ("extraRandom")
def select_certain_json_file():
    # select EDFA types
    edfaTypes = list(EDFA_TYPES_TO_GAINS.keys())
    for indx in range(len(edfaTypes)):
            print(str(indx)+":"+edfaTypes[indx])
    edfaTypeIndx = int(input("type the indx of edfa types want to plot:")) - int('0')
    edfaType = edfaTypes[edfaTypeIndx]
    # select EDFA gain setting
    for indx in range(len(EDFA_TYPES_TO_GAINS[edfaType])):
            print(str(indx)+":"+EDFA_TYPES_TO_GAINS[edfaType][indx])
    gainIndx = int(input("type the indx of gain setting want to plot:")) - int('0')
    gain = EDFA_TYPES_TO_GAINS[edfaType][gainIndx]
    # select channel loading files
    for indx in range(len(CHANNEL_TYPES)):
            print(str(indx)+":"+CHANNEL_TYPES[indx])
    channelTypesIndx = int(input("type the indx of channel loading file want to plot:")) - int('0')
    channelType = CHANNEL_TYPES[channelTypesIndx]
    return edfaType,gain,channelType

def generate_json_file_path(edfaType,gain,channelType):
    return get_path_to_file([DATASET_PATH,edfaType,gain,channelType])

# selec the file from this folder 
def select_json_files(dataPath):
    hasFolder, subFilePath = select_current_folder(dataPath)
    while(hasFolder):
        hasFolder, subFilePath = select_current_folder(subFilePath)
    return subFilePath

def select_current_folder(dataPath):
    if os.path.isdir(dataPath):
        subfolers = os.listdir(dataPath)
        for filenameIndx in range(len(subfolers)):
            print(str(filenameIndx)+":"+subfolers[filenameIndx])
        key = int(input("type the indx of file/folder want to plot:")) - int('0')
        fileName = subfolers[key]
        dataPath = get_path_to_file([dataPath,fileName])
        if os.path.isdir(dataPath): 
            return True, dataPath
    return False, dataPath

####################
# SHOW FOLDER STRUCTURE
####################

# show folder structure
  # by READ ME file

####################
# SHOW JSON STRUCTURE
####################

# sub channel loading Names
def show_names_in_one_channel_loadings():
    pass

# show metastructure 
def show_json_measurement_setup(edfaTypes):
    pass

def show_json_measurement_details(edfaTypes):
    pass

####################
# SHOW ONE JSON DATA
####################


def show_json_one_item(data,subChannelName,Item):
    pass

####################
# HELPER PLOTS
####################


# bar plot helper function -> plot one list 



# import from outside one file
# paper line plot 1
# def paper_plot_1(): pass

# paper line plot 2

# paper overview heatmap plot


# paper power range 




# import from json file 
def import_EDFA_files(jsonFile):
    with open(jsonFile, "r") as read_file:
        data = json.load(read_file)
    return data

# show one channel loading 
def show_one_channel_loading():
    jsonFileName = select_json_files(DATASET_PATH)
    edfaData = import_EDFA_files(jsonFileName)


def __init__(void):
    pass
