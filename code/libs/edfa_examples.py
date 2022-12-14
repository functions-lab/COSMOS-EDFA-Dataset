from .edfa_visual_libs import *

####################
# SELECT FILES
####################

# return edfaType ("booster"), gain ("18dB"), channelType ("extraRandom")
# def select_certain_json_file():
#     # select EDFA types
#     edfaTypes = list(EDFA_TYPES_TO_GAINS.keys())
#     for indx in range(len(edfaTypes)):
#             print(str(indx)+":"+edfaTypes[indx])
#     edfaTypeIndx = int(input("type the indx of edfa types want to plot:")) - int('0')
#     edfaType = edfaTypes[edfaTypeIndx]
#     # select EDFA gain setting
#     for indx in range(len(EDFA_TYPES_TO_GAINS[edfaType])):
#             print(str(indx)+":"+EDFA_TYPES_TO_GAINS[edfaType][indx])
#     gainIndx = int(input("type the indx of gain setting want to plot:")) - int('0')
#     gain = EDFA_TYPES_TO_GAINS[edfaType][gainIndx]
#     # select channel loading files
#     for indx in range(len(CHANNEL_TYPES)):
#             print(str(indx)+":"+CHANNEL_TYPES[indx])
#     channelTypesIndx = int(input("type the indx of channel loading file want to plot:")) - int('0')
#     channelType = CHANNEL_TYPES[channelTypesIndx]
#     return edfaType,gain,channelType

def generate_json_file_path(edfaType,gain,channelType,roadmName):
    folderName = get_path_to_file([DATASET_PATH,edfaType,gain,channelType])
    return matchFile("*"+roadmName+"*.json",folderName)

# selec the file from this folder 

# def select_json_files(dataPath):
#     hasFolder, subFilePath = select_current_folder(dataPath)
#     while(hasFolder):
#         hasFolder, subFilePath = select_current_folder(subFilePath)
#     return subFilePath

# def select_current_folder(dataPath):
#     if os.path.isdir(dataPath):
#         subfolers = os.listdir(dataPath)
#         for filenameIndx in range(len(subfolers)):
#             print(str(filenameIndx)+":"+subfolers[filenameIndx])
#         key = int(input("type the indx of file/folder want to plot:")) - int('0')
#         fileName = subfolers[key]
#         dataPath = get_path_to_file([dataPath,fileName])
#         if os.path.isdir(dataPath): 
#             return True, dataPath
#     return False, dataPath

####################
# Print/plot arbitrary Json data
####################

def plot_json_one_element(edfaType,gain,channelType,roadmName,subChannelName,spectrumName):
    # edfaType,gain,channelType = select_certain_json_file()
    # edfaType,gain,channelType = "booster","18dB","fix"
    jsonPath = generate_json_file_path(edfaType,gain,channelType,roadmName)
    data = getJsonData(jsonPath)
    data_dict = get_json_one_item(data,subChannelName,spectrumName)
    plot_one_dict_to_bar(data_dict)
    pp.pprint(data_dict)

# input data dict
# output one 
def get_json_one_item(data,subChannelName,spectrumName):
    for metadata in data:
        OpenChannelType = metadata['open_channel_type'] 
        if OpenChannelType == subChannelName:
            return metadata[spectrumName]
    raise Exception(subChannelName+" not found in the data.")

# input dict
def plot_one_dict_to_bar(data_dict):
    channelIndx = list(data_dict.keys())
    y_data = [data_dict[indx] for indx in channelIndx]
    x_data = [int(indx) for indx in channelIndx]
    plt.figure()
    plt.grid()
    plt.bar(x_data,y_data)
    plt.xlabel("Channel Indices")
    plt.ylabel("Power (dBm)")
    plt.show()
    plt.savefig(get_path_to_file(["..","misc","figures","one_spectrum.png"]), dpi=480)

####################
# Plot arbitrary gain spectrum
####################

def plot_one_json_file_gain_spectrum(edfaType,gain,channelType,roadmName):

    random_thresholds={
        "random":[1,6,21,49],   # random
        "extraRandom":[1,6,21,49,96] # extra random 
    }

    savePath = get_path_to_file(["..","misc","figures"])
    figure_postName = ".png"

    dataFolderPath = get_path_to_file([DATASET_PATH,edfaType,gain,channelType])
    
    dataPath = matchFile("*"+roadmName+"*.json",dataFolderPath)
    print(dataPath)
    data = getJsonData(dataPath)
    # print(dataPath)
    whetherFixOrRandom = True if (channelType == "fix" or channelType == "extraLow") else False

    if whetherFixOrRandom:

        # process and plot data
        datas = splitDataByOpenChannel(data,edfaType,randomChannel=False)
        for j in range(len(datas)):
            OpenData = datas[j]
            OpenChannelType = OpenData[0]['open_channel_type'] 
            
            saveName = roadmName+"_"+channelType+"_"+\
                        OpenChannelType + ' gain profile'  + figure_postName
            saveName = get_path_to_file([savePath,saveName])
            title = OpenChannelType + '\n channel gain profile compare'
            EDFAdata = calculateGainDict(OpenData,edfaType,calculateRipple=True)
            plotGainData(j,EDFAdata,title,alphaNum=0.2,saveName=saveName)

    else:
        # process and plot data
        random_threshold = random_thresholds[channelType]
        datas = splitDataByOpenChannel(data,edfaType,randomChannel=True,threshold=random_threshold)
        for j in range(len(datas)):
            OpenData = datas[j]
            OpenChannelLenStart = random_threshold[j]
            OpenChannelLenEnd = random_threshold[j+1] - 1
            OpenChannelRange = str(OpenChannelLenStart) + '-' + str(OpenChannelLenEnd) 
            saveName = roadmName+"_"+channelType+"_"+\
                        'RANDOM random channel #='+ OpenChannelRange + ' gain profile compare' + figure_postName
            saveName = get_path_to_file([savePath,saveName])
            title = 'random channel #='+ OpenChannelRange + ' gain profile compare'
            EDFAdata = calculateGainDict(OpenData,edfaType,calculateRipple=True)
            plotGainData(j,EDFAdata,title,alphaNum=0.2,saveName=saveName) 


####################
# Convert Json raw data to ML readable data file
####################

from .edfa_feature_extraction_libs import *


####################
# PAPER PLOTS
####################

# ignore for now ... 


############################
# USER OWN HELPER FUNCTION
############################

# put your self defined function here 