from .edfaBasicLib import *
'''
## split to sub-dataset for more easy combinations ....
### train
#### fix-baseline (without goalpost)
#### 80% random, extraLow, extraRandom
### test
#### goalpost without first 
#### 20% random
### augment
#### non-repeated fix without goalpost dataset
#### non-repeated goalpost
'''

def featureExtraction_ML(data_characterization,extractionType,channelType,featureType,channelNum=95,calculateRipple=False,\
    newCalibration=True,calculateAugment = False):
    if featureType not in ["train","test","augm"]:
        raise Exception("feature type not accurate.")
    ExtractedFeature = pd.DataFrame()
    for metadata in data_characterization:

        # different feature extraction from different measurements
        if extractionType == "preamp":

            repeat_index_start = 1
            # target gain & wss channels
            gain_target = metadata["roadm_dut_preamp_info"]["target_gain"]
            wss_channels = metadata['roadm_flatten_wss_active_channel_index']
            # PD reading
            edfa_input_power_total = metadata["roadm_dut_preamp_info"]["input_power"]
            edfa_output_power_total= metadata["roadm_dut_preamp_info"]["output_power"]
            # spectra readings
            EDFA_input_spectra  = np.array(list(metadata["roadm_dut_preamp_input_power_spectra"].values()))
            EDFA_output_spectra = np.array(list(metadata["roadm_dut_wss_input_power_spectra"].values()))
        
        elif extractionType == "booster":

            repeat_index_start = 0
            # target gain & wss channels
            gain_target = metadata["roadm_dut_edfa_info"]["target_gain"]
            wss_channels = metadata["roadm_dut_wss_active_channel_index"]
            # PD reading
            edfa_input_power_total = metadata["roadm_dut_edfa_info"]["input_power"]
            edfa_output_power_total= metadata["roadm_dut_edfa_info"]["output_power"]
            # spectra readings
            EDFA_input_spectra = np.array(list(metadata["roadm_dut_wss_output_power_spectra"].values()))
            EDFA_output_spectra = np.array(list(metadata["roadm_dut_booster_output"].values()))

        else:
            print(extractionType+" has not implemented!")
            exit(-1)

        # take training data in fix channel loading
        if channelType == "fix" and featureType == "train":
            # ignore all the goalpost since they are in test set
            if metadata["open_channel_type"] == "goalpost_channel_balanced_freq_low_medium":
                break
        
        # take test data for goalpost
        if channelType == "fix" and featureType == "test":
            # only take goalpost
            if "goalpost" not in metadata["open_channel_type"]:
                continue
            else: # ignore first repeat in the test set
                if "repeat_index" in metadata.keys():
                    repeat_index = metadata["repeat_index"]
                    # since booster start with 0 but preamp start with 1 ...
                    if repeat_index == repeat_index_start:
                        continue

        # take augment data
        if channelType == "fix" and featureType == "augm":
            # only take none-repeated augment data
            if "repeat_index" in metadata.keys():
                repeat_index = metadata["repeat_index"]
                # since booster start with 0 but preamp start with 1 ...
                if repeat_index != repeat_index_start:
                    continue
            # ignore all the goalpost
            if metadata["open_channel_type"] == "single_channel":# only take 0.5% data
                break

        # gain profile
        acutal_gain_spectra = []
        for i in range(channelNum):
            if calculateRipple:
                gain = EDFA_output_spectra[i] - EDFA_input_spectra[i] - gain_target # - delta1 - delta2
            else:
                gain = EDFA_output_spectra[i] - EDFA_input_spectra[i] # - delta1 - delta2
            acutal_gain_spectra.append(gain)
        # calculate one hot DUT WSS open channel
        DUT_WSS_activated_channels = [0]*channelNum
        for indx in wss_channels:
            DUT_WSS_activated_channels[indx-1] = 1

        # write the PD power info
        metaResult = {}
        # HeaderCSV = ['EDFA_input_spectra','EDFA_input_power_total','target_gain','calculated_gain_spectra']
        metaResult['target_gain'] = gain_target
        metaResult['EDFA_input_power_total'] = edfa_input_power_total
        metaResult['EDFA_output_power_total'] = edfa_output_power_total
        
        # write the spectra info
        for i in range(channelNum):
            post_indx = str(i).zfill(2)
            metaResult['EDFA_input_spectra_'+post_indx] = EDFA_input_spectra[i]
            metaResult['DUT_WSS_activated_channel_index_'+post_indx] = DUT_WSS_activated_channels[i]
            metaResult['calculated_gain_spectra_'+post_indx] = acutal_gain_spectra[i]
            metaResult['EDFA_output_spectra_'+post_indx] = EDFA_output_spectra[i]
        
        # ExtractedFeature = ExtractedFeature.append([metaResult],ignore_index=True)
        ExtractedFeature = pd.concat([ExtractedFeature,pd.DataFrame.from_dict([metaResult])],ignore_index=True)

    return ExtractedFeature


'''
    Input paras
        folderList = ['fix', 'random', 'extraRandom', 'extraLow']
        edfaTypes = ["booster","preamp"]
        fileList = ['rdm1-co1', 'rdm2-co1', 'rdm3-co1', 'rdm4-co1',
                    'rdm5-co1', 'rdm6-co1', 'rdm1-lg1', 'rdm2-lg1']
        gainList = ["15dB","18dB","21dB"]
    Output paras
        csv files generated at "misc/ML_features" folder
'''

def generate_ML_features(edfaTypes,gainList,fileList,folderList):
    # prePath
    train_ratio = 0.8
    output_prepath = get_path_to_file(["..","misc","ML_features"])

    for fileName in fileList:
        for edfaType in edfaTypes: # 
            print(fileName)
            trainExtractedFeature = pd.DataFrame()
            testRandomExtractedFeature = pd.DataFrame()
            testGoalpostExtractedFeature = pd.DataFrame()
            augmExtractedFeature = pd.DataFrame()
            for channelType in folderList:
                for gain in gainList:
                    filePath = get_path_to_file([DATASET_PATH,edfaType,gain,channelType])
                    fileName_booster = matchFile('*'+fileName+'*.json', filePath)

                    with open(fileName_booster, "r") as read_file:
                        data = json.load(read_file)

                    # feature extraction
                    if channelType == "fix":
                        # 
                        newFeature = featureExtraction_ML(
                            data["measurement_data"], edfaType,channelType,"train", data['measurement_setup']['roadm_wss_num_channel'])
                        trainExtractedFeature = pd.concat([trainExtractedFeature,newFeature],ignore_index=True)
                        # goalpost
                        newFeature = featureExtraction_ML(
                            data["measurement_data"], edfaType,channelType,"test", data['measurement_setup']['roadm_wss_num_channel'])
                        testGoalpostExtractedFeature = pd.concat([testGoalpostExtractedFeature,newFeature],ignore_index=True)
                        # augm feature
                        newFeature = featureExtraction_ML(
                            data["measurement_data"], edfaType,channelType,"augm", data['measurement_setup']['roadm_wss_num_channel'])
                        augmExtractedFeature = pd.concat([augmExtractedFeature,newFeature],ignore_index=True)

                    elif channelType == "random":  # random
                        newFeature = featureExtraction_ML(data["measurement_data"], edfaType,channelType,"test",
                                        data['measurement_setup']['roadm_wss_num_channel'])
                        # split the data here
                        training_data = newFeature.sample(frac=train_ratio, random_state=25)
                        testing_data = newFeature.drop(training_data.index)

                        trainExtractedFeature = pd.concat([trainExtractedFeature,training_data],ignore_index=True)
                        testRandomExtractedFeature = pd.concat([testRandomExtractedFeature,testing_data],ignore_index=True)

                    elif channelType == 'extraLow':
                        extraLowFeature = featureExtraction_ML(data["measurement_data"], edfaType,channelType,"train",
                                        data['measurement_setup']['roadm_wss_num_channel'])
                        trainExtractedFeature = pd.concat([trainExtractedFeature,extraLowFeature],ignore_index=True)

                    elif channelType == "extraRandom":
                        newFeature = featureExtraction_ML(data["measurement_data"], edfaType,channelType,"train",
                                        data['measurement_setup']['roadm_wss_num_channel'])
                        trainExtractedFeature = pd.concat([trainExtractedFeature,newFeature],ignore_index=True)

                    else:
                        print("haven't implemented yet!")
            
            # write the output to CSV file
            output_path = get_path_to_file([output_prepath,edfaType,fileName])
        
            trainExtractedFeature.to_csv(output_path+"_train.csv")
            testRandomExtractedFeature.to_csv(output_path+"_test_random.csv")
            testGoalpostExtractedFeature.to_csv(output_path+"_test_goalpost.csv")
            augmExtractedFeature.to_csv(output_path+"_augm.csv")
        
