from .edfaExternalLibs import *

def matchFile(pattern, foler):
    # match one file in the folder
    # example usage:
    # result = matchFile('*rdm1-co1*.json', '.../benchmark/extraRandom/')
    # result is the full path 
    for file in os.listdir(foler):
        if fnmatch.fnmatch(file, pattern):
            return os.path.join(foler, file)

def getJsonData(fileName):
    with open(fileName, "r") as read_file:
        data = json.load(read_file)
    return data['measurement_data']

Lumentum_pd_threshold = -29

Lumentum_ocm_threshold = {
    "booster in" : (-35.9,3.8),
    "booster out" : (-14.9,6.8),
    "line in" : (-35.4,-3.0),
    "preamp out" : (-14.6,6.8),
    "mux in" : (-28.1,0.3)
}

def returnValidOCMListdata(dataset,key):
    returnData = []
    for data in dataset:
        if data < Lumentum_ocm_threshold[key][0]:
            continue# drop and do nothing
        elif data > Lumentum_ocm_threshold[key][1]:
            print(str(data),key,str(Lumentum_ocm_threshold[key][1]))
            continue
            raise ValueError("one channel ("+str(data)+" dBm) above the threshold of "+key+"("+Lumentum_ocm_threshold[key][1]+")")
        else:
            returnData.append(data)
    return np.array(returnData)

def splitDataByOpenChannel(data,label="booster",randomChannel=False,threshold=[1,6,21,49]):
    result = []
    if label == "booster":  wss_channel_label = "roadm_dut_wss_active_channel_index"
    elif label == "preamp": wss_channel_label = "roadm_flatten_wss_active_channel_index" 
    else: raise ValueError(label+" haven't been implemented.")

    if randomChannel: channelType = 'roadm_dut_wss_active_channel_index'
    else: channelType = 'open_channel_type'

    if channelType == 'open_channel_type':
        uniqueOpenChannelName = list(set([item['open_channel_type'] for item in data]))
        for openName in uniqueOpenChannelName:
            currentOpenData = []
            for metadata in data:
                if metadata['open_channel_type'] == openName:
                    currentOpenData.append(metadata)
                else:
                    continue
            result.append(currentOpenData)
    else: # roadm_dut_wss_active_channel_index
        uniqueOpenChannelLen = [ [*range(threshold[i],threshold[i+1])] for i in range(len(threshold)-1)]
        for openLen in uniqueOpenChannelLen:
            currentOpenData = []
            for metadata in data:
                if len(metadata[wss_channel_label]) in openLen:
                    currentOpenData.append(metadata)
                else:
                    continue
            result.append(currentOpenData)
    return result

def logsumexp10(x):
    return 10*np.log10(np.sum(np.power(10,x/10)))

def get_pd_power(data_characterization,label="booster"):
    input_power_list, output_power_list = [],[]
    # labels by preamp or booster
    if label == "booster":
        dut_edfa_label = "roadm_dut_edfa_info"
    elif label == "preamp":
        dut_edfa_label = "roadm_dut_preamp_info"
    else:
        raise ValueError(label+"haven't implemented")
    
    for metadata in data_characterization:
        input_power_list.append(metadata[dut_edfa_label]["input_power"])
        output_power_list.append(metadata[dut_edfa_label]["output_power"])

    return input_power_list, output_power_list


def calculateGainDict(data_characterization,label="booster",calculateRipple=False):
    gain_profiles = defaultdict(list)
    # labels by preamp or booster
    if label == "booster":
        dut_edfa_label = "roadm_dut_edfa_info"
        input_power_label = "roadm_dut_wss_output_power_spectra"
        input_limit_label = "booster in"
        output_power_spectra= "roadm_dut_booster_output"
        output_limit_label = "booster out"
        wss_channel_label = "roadm_dut_wss_active_channel_index"
    elif label == "preamp":
        dut_edfa_label = "roadm_dut_preamp_info"
        input_power_label = "roadm_dut_preamp_input_power_spectra"
        input_limit_label = "line in"
        output_power_spectra= "roadm_dut_wss_input_power_spectra"
        output_limit_label = "preamp out"
        wss_channel_label = "roadm_flatten_wss_active_channel_index"
    else:
        raise ValueError(label+"haven't implemented")
    #######################################################################
    for metadata in data_characterization:
        # target gain
        gain_target = metadata[dut_edfa_label]["target_gain"]
        wss_channels = metadata[wss_channel_label]
        #delta 1
        edfa_input_power_total = metadata[dut_edfa_label]["input_power"]
        wss_output_power_spectra = np.array(list(metadata[input_power_label].values()))
        wss_output_power_spectra_tmp = returnValidOCMListdata(wss_output_power_spectra,input_limit_label)
        wss_output_power_spectra_total = logsumexp10(wss_output_power_spectra_tmp)
        delta1 = edfa_input_power_total - wss_output_power_spectra_total

        #delta 2
        edfa_output_power_total = metadata[dut_edfa_label]["output_power"]
        booster_out_spectra = np.array(list(metadata[output_power_spectra].values()))
        booster_output_spectra_tmp = returnValidOCMListdata(booster_out_spectra,output_limit_label)
        booster_output_spectra_total = logsumexp10(booster_output_spectra_tmp)
        delta2 = booster_output_spectra_total - edfa_output_power_total
        
        # gain profile
        for i in range(len(wss_channels)):
            indx = wss_channels[i] # indx start from 1, python list start from [0]
            if calculateRipple:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1] - gain_target # - delta1 - delta2
            else:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1] # - delta1 - delta2
            gain_profiles[indx].append(gain)
    return gain_profiles

def calculateGainDict_withinOCMrange(data_characterization,label="booster",calculateRipple=False):
    gain_profiles = defaultdict(list)
    # labels by preamp or booster
    if label == "booster":
        dut_edfa_label = "roadm_dut_edfa_info"
        input_power_label = "roadm_dut_wss_output_power_spectra"
        input_limit_label = "booster in"
        output_power_spectra= "roadm_dut_booster_output"
        output_limit_label = "booster out"
        wss_channel_label = "roadm_dut_wss_active_channel_index"
    elif label == "preamp":
        dut_edfa_label = "roadm_dut_preamp_info"
        input_power_label = "roadm_dut_preamp_input_power_spectra"
        input_limit_label = "line in"
        output_power_spectra= "roadm_dut_wss_input_power_spectra"
        output_limit_label = "preamp out"
        wss_channel_label = "roadm_flatten_wss_active_channel_index"
    else:
        raise ValueError(label+"haven't implemented")
    #######################################################################
    for metadata in data_characterization:
        # target gain
        gain_target = metadata[dut_edfa_label]["target_gain"]
        wss_channels = metadata[wss_channel_label]
        #delta 1
        edfa_input_power_total = metadata[dut_edfa_label]["input_power"]
        wss_output_power_spectra = np.array(list(metadata[input_power_label].values()))
        wss_output_power_spectra_tmp = returnValidOCMListdata(wss_output_power_spectra,input_limit_label)
        wss_output_power_spectra_total = logsumexp10(wss_output_power_spectra_tmp)
        delta1 = edfa_input_power_total - wss_output_power_spectra_total

        #delta 2
        edfa_output_power_total = metadata[dut_edfa_label]["output_power"]
        booster_out_spectra = np.array(list(metadata[output_power_spectra].values()))
        booster_output_spectra_tmp = returnValidOCMListdata(booster_out_spectra,output_limit_label)
        booster_output_spectra_total = logsumexp10(booster_output_spectra_tmp)
        delta2 = booster_output_spectra_total - edfa_output_power_total
        
        # gain profile
        for i in range(len(wss_channels)):
            indx = wss_channels[i] # indx start from 1, python list start from [0]
            if calculateRipple:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1] - gain_target # - delta1 - delta2
            else:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1] # - delta1 - delta2
            gain_profiles[indx].append(gain)
    return gain_profiles

class PolyFit(object):
    def __init__(self,orderNum):
        self.order = orderNum

    def fit(self,x,y):
        self.paras = np.polyfit(x,y,self.order)

    def predict(self,x):
        func = np.poly1d(self.paras)
        return func(x)

def fitCurve(order,x,y,x_predict):
    fitFunc = PolyFit(order)
    fitFunc.fit(x,y)
    return fitFunc.predict(x_predict)

def plotRippleData(indxForFigure,data,title,saveName=None):
    plt.figure(indxForFigure)
    x_axis = [indx for indx in range(len(data))]
    y_fit = fitCurve(5,x_axis,data,x_axis)
    plt.plot(x_axis,y_fit,'y--')
    plt.scatter(x_axis,data)
    plt.xlabel('Channel indice')
    plt.ylabel('Gain (dB)')
    plt.title(title)
    plt.show()
    if saveName:
        plt.savefig(saveName)

def recoverDict(dataDict):
    x_axis, y_data = [],[]
    for key in dataDict.keys():
        x_axis.extend([key]*len(dataDict[key]))
        y_data.extend(dataDict[key])
    return x_axis, y_data

def sortTwoList(list1,list2):
    # list1 = ["c", "b", "d", "a"]
    # list2 = [2, 3, 1, 4]
    # output
    # list1 = ['a', 'b', 'c', 'd']
    # list2 = [4, 3, 2, 1]
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    return list1, list2
    
def statisticDict(dataDict):
    x_axis, y_data_min, y_data_mean, y_data_max = [],[],[],[]
    for key in dataDict:
        x_axis.append(key)
        y_data_min.append(min(dataDict[key]))
        y_data_mean.append(statistics.mean(dataDict[key]))
        y_data_max.append(max(dataDict[key]))
    x_axis_return,y_data_min = sortTwoList(x_axis,y_data_min)
    x_axis_return,y_data_mean = sortTwoList(x_axis,y_data_mean)
    x_axis_return,y_data_max = sortTwoList(x_axis,y_data_max)
    return x_axis_return, y_data_min, y_data_mean, y_data_max

def plotGainData(indxForFigure,fitOrder,dataDict,title,
        saveName=None,scatterColor="blue",alphaNum=0.2,
        gridLine=True,makerSize=2):
    plt.figure(indxForFigure)
    x_axises, y_data = recoverDict(dataDict)
    x_axis, y_data_min, y_data_mean, y_data_max = statisticDict(dataDict)
    plt.plot(x_axis,y_data_mean,color=scatterColor)
    if gridLine:
        plt.grid(linestyle = '--', linewidth = 0.5)
    # plt.legend(["min fit","mean fit","max fit"], loc ="upper right")
    plt.fill_between(x_axis, y_data_min, y_data_max,
                 facecolor=scatterColor,   # The fill color
                 color=scatterColor,       # The outline color
                 alpha=alphaNum,           # Transparency of the fill
                 label='_nolegend_')           
    plt.scatter(x_axises,y_data,c = scatterColor,alpha=alphaNum,s=makerSize,label='_nolegend_')
    plt.xlabel('Channel Indices')
    plt.ylabel('Gain ripple (dB)')
    plt.title(title)
    if saveName:
        plt.savefig(saveName, bbox_inches='tight', dpi=600)

def plotGainDataNormalize(indxForFigure,fitOrder,dataDict,title,
        saveName=None,scatterColor="blue",alphaNum=0.2,
        gridLine=True,makerSize=2):
    plt.figure(indxForFigure)
    x_axises, y_data = recoverDict(dataDict)
    x_axis, y_data_min, y_data_mean, y_data_max = statisticDict(dataDict)
    y_mean_mean = np.mean(y_data_mean)
    plt.plot(x_axis,[tmp - y_mean_mean for tmp in y_data_mean],color=scatterColor)
    if gridLine:
        plt.grid(linestyle = '--', linewidth = 0.5)
    plt.fill_between(x_axis, [subdata - y_mean_mean for subdata in y_data_min], 
                             [subdata - y_mean_mean for subdata in y_data_max],
                 facecolor=scatterColor,   # The fill color
                 color=scatterColor,       # The outline color
                 alpha=alphaNum)           # Transparency of the fill
    plt.scatter(x_axises,
                [subsubdata - y_mean_mean for subsubdata in y_data ],
                c = scatterColor,alpha=alphaNum,s=makerSize)
    plt.xlabel('Channel Indices')
    plt.ylabel('Gain ripple (dB)')
    plt.title(title)
    if saveName:
        plt.savefig(saveName, dpi=600)

def ChannelToWavelength(indices):
    c_speed = 299792458 # 3e8
    LUMENTUM_WSS_NUM_CHANNEL = 95
    LUMENTUM_WSS_CHANNEL_FREQ_CENTER_START = 191350.0
    LUMENTUM_WSS_CHANNEL_BW = 50.0
    LUMENTUM_WSS_CHANNEL_FREQ_CENTER_LIST = [c_speed/(LUMENTUM_WSS_CHANNEL_FREQ_CENTER_START + idx*LUMENTUM_WSS_CHANNEL_BW)
                                          for idx in range(LUMENTUM_WSS_NUM_CHANNEL)]
    if any(isinstance(i, list) for i in indices): # check nested list
        result = []
        for indice in indices:
            result.append([LUMENTUM_WSS_CHANNEL_FREQ_CENTER_LIST[indc-1] for indc in indice])
    else:
        result = [LUMENTUM_WSS_CHANNEL_FREQ_CENTER_LIST[indc-1] for indc in indices]

    return result

def plotGainDataInWavelength(indxForFigure,fitOrder,dataDict,title,
        saveName=None,scatterColor="blue",alphaNum=0.2,
        gridLine=True,makerSize=2):
    plt.figure(indxForFigure)
    x_axises, y_data = recoverDict(dataDict)
    x_axis, y_data_min, y_data_mean, y_data_max = statisticDict(dataDict)
    # y_fit_min = fitCurve(fitOrder,x_axis,y_data_min,x_axis)
    # y_fit_mean = fitCurve(fitOrder,x_axis,y_data_mean,x_axis)
    # y_fit_max = fitCurve(fitOrder,x_axis,y_data_max,x_axis)
    # plt.plot(x_axis,y_fit_min,'y--')
    x_axis, x_axises = ChannelToWavelength(x_axis), ChannelToWavelength(x_axises)

    plt.plot(x_axis,y_data_mean,color=scatterColor)
    if gridLine:
        plt.grid(linestyle = '--', linewidth = 0.5)
    plt.fill_between(x_axis, y_data_min, y_data_max,
                 facecolor=scatterColor,   # The fill color
                 color=scatterColor,       # The outline color
                 alpha=alphaNum,           # Transparency of the fill
                 label='_nolegend_') 
    plt.scatter(x_axises,y_data,c = scatterColor,alpha=alphaNum,s=makerSize,label='_nolegend_')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Gain ripple (dB)')
    plt.title(title)
    if saveName:
        plt.savefig(saveName, bbox_inches='tight', dpi=600)

########################################################################################
## one span
def calculate1spanGainDict(data_characterization,calculateRipple=False):
    gain_profiles = defaultdict(list)
    for metadata in data_characterization:
        # target gain
        # gain_target = metadata["roadm_booster_preamp_info"]["target_gain"]
        # dut_line_out = metadata["roadm_dut_line_port_info"]["output-power"]
        # dut_wss_in = metadata["roadm_dut_wss_port_info"]["input-power"]
        # wss_channels = metadata["roadm_booster_wss_active_channel_index"]
        #delta 1
        # edfa_input_power_total = metadata["roadm_dut_edfa_info"]["input_power"]
        wss_output_power_spectra = np.array(list(metadata["roadm_booster_wss_input_power_spectra"].values()))

        #delta 2
        # edfa_output_power_total = metadata["roadm_dut_edfa_info"]["output_power"]
        booster_out_spectra = np.array(list(metadata["roadm_preamp_wss_input_power_spectra"].values()))

        # gain profile
        dataNum = metadata['roadm_booster_wss_active_channel_index']
        for i in range(len(dataNum)):
            indx = dataNum[i] # indx start from 1, python list start from [0]
            if calculateRipple:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1]# - gain_target 
            else:
                gain = booster_out_spectra[indx-1] - wss_output_power_spectra[indx-1]
            gain_profiles[indx].append(gain)
    return gain_profiles

def splitDataByOpenChannel1span(data,type,threshold=[1,6,21,49]):
    result = []
    if type == 'open_channel_type':
        uniqueOpenChannelName = list(set([item['open_channel_type'] for item in data]))
        for openName in uniqueOpenChannelName:
            currentOpenData = []
            for metadata in data:
                if metadata['open_channel_type'] == openName:
                    currentOpenData.append(metadata)
                else:
                    continue
            result.append(currentOpenData)
    else: # roadm_dut_wss_active_channel_index
        uniqueOpenChannelLen = [ [*range(threshold[i],threshold[i+1])] for i in range(len(threshold)-1)]
        for openLen in uniqueOpenChannelLen:
            currentOpenData = []
            for metadata in data:
                if metadata['roadm_booster_wss_num_active_channel'] in openLen:
                    currentOpenData.append(metadata)
                else:
                    continue
            result.append(currentOpenData)
    return result