# example code for visualization the EDFA gain spectrum dataset
from libs.edfa_examples import *

####################
# MAIN (examples)
####################
def run_examples(option):
    if option == 1:
        edfaType,gain,channelType,roadmName = "booster","18dB","random","rdm5-co1"
        plot_one_json_file_gain_spectrum(edfaType,gain,channelType,roadmName)

    elif option == 2:
        # get from website introduction or README / 
        edfaType,gain,channelType,roadmName = "preamp","18dB","fix","rdm1-co1"
        # edfaType,gain,channelType,roadmName,subChannelName,spectrumName
        subChannelName,spectrumName = "fully_loaded_channel_wdm","roadm_flatten_preamp_input_power_spectra"
        plot_json_one_element(edfaType,gain,channelType,roadmName,subChannelName,spectrumName)

    elif option == 3:
        channelTypes = ['fix', 'random', 'extraRandom', 'extraLow']
        edfaTypes = ["booster"] # ["booster","preamp"]
        roadmNames = ['rdm1-co1'] # ['rdm1-co1', 'rdm2-co1', 'rdm3-co1', 'rdm4-co1',
                                # 'rdm5-co1', 'rdm6-co1', 'rdm1-lg1', 'rdm2-lg1']
        gainLists = ["15dB","18dB","21dB"]
        generate_ML_features(edfaTypes,gainLists,roadmNames,channelTypes)
        # check the generated csv files at "misc/ML_features" folder

    else:
        raise Exception("not implemented.")

# run the examples
run_examples(option=2)