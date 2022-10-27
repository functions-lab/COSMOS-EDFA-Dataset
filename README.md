# COSMOS EDFA Dataset

COSMOS EDFA Dataset consists of the gain spectrum measurements using the built-in photodiodes (PDs) and optical channel monitors (OCMs) for 16 EDFAs within 8 commercial grade Lumentum ROADM-20 units deployed in the PAWR COSMOS testbed. The dataset includes measurements collected from 8 booster EDFAs, each with 3 gain settings, and 8 pre-amplifier EDFAs, each with 5 gain settings. For each EDFA at a given gain setting, 3,168 gain spectrum measurements are collected with a set of diverse channel loading configurations and varying input power levels. 

# Measurement pipeline
![Measurement pipeline!](/misc/md_support_materials/figures/measurement_setup.jpg)
The figure shows the block diagram of the block diagram of the Lumentum ROADM-20 unit and the measurement setup of a device under test (DUT) EDFA. Each ROADM unit consists of one MUX wavelength selective switch (WSS), one DEMUX  WSS, one booster EDFA, and one pre-amplifier EDFA, and is equipped with total power and channel power monitoring capabilities using the built-in PDs and OCMs with a power measurement resolution of 0.01 dB and 0.1 dB, respectively.  We use a comb source to generate a set of 95×50 GHz WDM channels in the C-band.

With a DUT booster EDFA, the output of the comb source is connected to an add port of the MUX WSS, which applies the channel loading configuration, adjusts the power level in each loaded channel, and generates a flat input power spectrum at the DUT EDFA. With a DUT pre-amplifier EDFA, the output of the comb source is first connected to the pre-amplifier EDFA and DEMUX WSS of the auxiliary ROADM, whose DEMUX WSS applies the channel loading configuration, adjusts the power level in each loaded channel, and generates a flat output power spectrum that is transmitted to the input of the DUT pre-amplifier EDFA. The output of the DUT EDFA is terminated.

The wavelength dependent gain spectrum of each EDFA, denoted by $g(\lambda_i)$, can be characterized by its input power spectrum, $S_{\textrm{in}}(\lambda_i)$, and output power spectrum, $S_{\textrm{out}}(\lambda_i)$, i.e., $g(\lambda_i) = S_{\textrm{out}}(\lambda_i)-S_{\textrm{in}}(\lambda_i), \forall i = 1,2,\dots,95$, where $\lambda_1 = 1529.16$ nm (196.050 THz) and $\lambda_{95} = 1566.72$ nm (191.350 THz).

# Channel Loading Configurations

For each EDFA, $g(\lambda_i)$ can vary significantly with different channel loading configurations. However, it is impossible to measure all $2^{95}$ configurations with 95$\times${50}\thinspace{GHz} channels where each channel can be switched ON/OFF. To address this challenge, we carefully design 5 sets of diverse channel loading configurations and using four *JSON* files to store the measurement results of the collected data:
* **Fixed Baseline** includes the fully loaded (WDM) channel configuration ($n=95$), 4 half loaded (lower/upper/even/odd) channel configurations ($n \in \{47,48\}$), and 7 selected single/double (adjacent) channel configurations. These channel loading stored in the *fix* dataset folder together with *Fixed Goalpost* mentioned below.
* **Fixed Goalpost** focuses on two sets of consecutive channels located in 3 channel groups (with short/medium/long wavelength), and includes 15 balanced and 12 imbalanced goalpost channel configurations with $n \in \{2,4,8,16,32\}$ and $n \in \{9,18\}$, respectively. These channel loading stored in the *fix* dataset folder together with *Fixed Baseline*.
* **Fixed Extra** includes the complete set of 95 single and 94 double (adjacent) channel loading configurations. These channel loading stored in the *extraLow* dataset folder.
* **Random Baseline** includes 100, 50, 20 random channel loading configurations for each value of $n \in \{1,2,\dots,5\}, \{6,8,\dots,20\}, \{21,24,\dots,48\}$, respectively
*  **Random Extra** expands \emph{Random Baseline} and includes 10 random channel loading configurations for each value of $n \in \{1,2,\dots,94,95\}$



# Dataset Folder Structure

The whole dataset folder structure is shown as following:

```
📦COSMOS-EDFA-Dataset 
 ┣ 📂codes  
 ┃ ┣ 📂libs  
 ┃ ┃ ┣ 📜edfaExternalLibs.py  
 ┃ ┃ ┗ 📜edfa_visual_libs.py  
 ┃ ┗ 📜examples.py  
 ┣ 📂dataset  
 ┃ ┣ 📂booster  
 ┃ ┃ ┣ 📂15dB  
 ┃ ┃ ┃ ┣ 📂extraLow  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm1-co1.xxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm1-lg1.xxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm2-co1.xxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm2-lg1.xxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm3-co1.bxxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm4-co1.xxx.json  
 ┃ ┃ ┃ ┃ ┣ 📜edfa_meas_rdm5-co1.xxx.json  
 ┃ ┃ ┃ ┃ ┗ 📜edfa_meas_rdm6-co1.xxx.json  
 ┃ ┃ ┃ ┣ 📂extraRandom  
 ┃ ┃ ┃ ┃ ┣ ...
 ┃ ┃ ┃ ┃ ┗ 📜edfa_meas_rdm6-co1.xxx.json  
 ┃ ┃ ┃ ┣ 📂fix  
 ┃ ┃ ┃ ┃ ┣ ...
 ┃ ┃ ┃ ┃ ┗ 📜edfa_meas_rdm6-co1.xxx.json  
 ┃ ┃ ┃ ┗ 📂random  
 ┃ ┃ ┃ ┃ ┣ ...
 ┃ ┃ ┃ ┃ ┗ 📜edfa_meas_rdm6-co1.xxx.json  
 ┃ ┃ ┣ 📂18dB  
 ┃ ┃ ┃ ┣ 📂extraLow  
 ┃ ┃ ┃ ┣ 📂extraRandom  
 ┃ ┃ ┃ ┣ 📂fix  
 ┃ ┃ ┃ ┗ 📂random  
 ┃ ┃ ┗ 📂21dB  
 ┃ ┗ 📂preamp  
 ┃ ┃ ┣ 📂15dB  
 ┃ ┃ ┣ 📂18dB  
 ┃ ┃ ┣ 📂21dB  
 ┃ ┃ ┣ 📂24dB  
 ┃ ┃ ┗ 📂27dB  
 ┣ 📂misc  
 ┃ ┣ 📂measurement_config  
 ┃ ┃ ┣ 📜lumentum_fixed_channel_config.json  
 ┃ ┃ ┗ ...
 ┗ 📜README.md
```
In the `code` folder, we provide examples for users to explore the collected data. 

In the `dataset` folder, all collected EDFA gain measurements in *JSON* format are stored. Specifically, the measurements files are organized by EDFA types (booster or pre-amplifier), gain setting, channel loading conditions, and ROADM names.

In the `misc` folder, we put related all other related files there. For example, channel loading configurations files are located in `measurement_config` folder. `figures` and `ML_features` folder store figures and ML model readable features in *csv* format generated by example codes, respectively. `md_support_materials` folder has all related materials for this document.


## Json File Structure
Each *JSON* file records one set of channel loading conditions with measurement number varies from 550 to 1100. In one *JSON* file, there are `measurement_setup` and `measurement_data`, where  `measurement_setup` structure is same for all files but `measurement_data` are slightly different for bExport a file



## Booster and pre-amplifier EDFA

 Pre-amplifier EDFA and for fix or random channel loading. We first show the structures of `measurement_setup`, and then go through `measurement_data` the booster *JSON* files and then show the one for pre-amplifier. 
## measurement_setup
```json
"measurement_setup": {
    "date": "2022.03.20.23.33.26",
    "comb_source": "CivilLaser EDFA + Nistica WSS + JSDU EDFA",
    "roadm_model": "Lumentum ROADM-20 Whitebox",
    "roadm_dut": "ROADM1_LG1_BED",
    "roadm_dut_edfa_module": "booster",
    "roadm_wss_channel_attenuation_default": 4.0,
    "roadm_wss_channel_attenuation_deviation": 3.0,
    "roadm_wss_num_channel": 95,
    "roadm_wss_channel_freq_center_start": 191350.0,
    "roadm_wss_channel_spacing": 50.0,
    "roadm_wss_channel_bw": 50.0,
    "roadm_wss_channel_freq_center_list": [
        191350.0,
        191400.0,
        ...
        196050.0
    ]
},
```
In the measurement setup, we record the date, ROADM device name, EDFA type (booster or pre-amplifier). There are two types of synchronization and they can complement each other:

- The workspace synchronization will sync all your files, folders and setc. Default attenuation in dB scale is assigned to the WSS before tings automatically. This will allow you to fetch your workspace on any other device-under-test (DUT) EDFA. We also record the wavelength channels we used. For example, from the file the first channel frequency is from `191325.0 GHz to 191375.0 GHz`, and the last would from `196025.0 GHz to 196075.0 GHz`. 


## measurement_data

### Booster EDFA
```json
"measurement_data": [
        {
            "open_channel_type": "channel_configuration_name ",
            "attenuation_setting": -2(dBm),
            "repeat_index": 0, # start from 0 for booster
            "calient_input_power_comb_source": float(dBm),
            "calient_input_power_roadm_dut_edfa": float(dBm),
            "roadm_dut_edfa_info": {...},
            "roadm_dut_line_port_info": {...},
            "roadm_dut_wss_port_info": {...},
            "roadm_dut_wss_num_active_channel": 95,
            "roadm_dut_wss_active_channel_index": [...],
            "roadm_dut_wss_attenuation": {...},
            "roadm_dut_wss_input_power_spectra": {...},
            "roadm_dut_wss_output_power_spectra": {...},
            "roadm_dut_booster_output": {...}
        },...,
    ]
```
Better to visualize where the data is ....

### Preamp EDFA
```json
    "measurement_data": [
        {
            "open_channel_type": "fully_loaded_channel_wdm",
            "attenuation_setting": -2(dBm),
            "repeat_index": 1, # start from 1 for booster
            "calient_input_power_comb_source": float(dBm),
            "calient_input_power_flatten_roadm_output": float(dBm),
            "roadm_flatten_preamp_info": {...},
            "roadm_flatten_wss_num_active_channel": 95,
            "roadm_flatten_wss_active_channel_index": [...],
            "roadm_flatten_line_port_info":  {...},
            "roadm_flatten_wss_attenuation": {...},
            "roadm_flatten_wss_input_power_spectra":  {...},
            "roadm_flatten_preamp_input_power_spectra":  {...},
            "roadm_dut_preamp_info":  {...},
            "roadm_dut_line_port_info":  {...},
            "roadm_dut_preamp_input_power_spectra":  {...},
            "roadm_dut_wss_input_power_spectra":  {...}
        },...
      ]
```
Better to visualize where the data is ....

### Each component in measurement_data [link to another md file]

# How to use the dataset

some introduction here.

## Example codes

### Dependency
`pip install numpy pandas matplotlib scipy pprint`

### Example codes
The example code can be found at `./codes/examples.py` . It supports three different usage of the collected data. 

 1. Plot arbitrary gain spectrum for one json file
-- Function explanation: plot the gain spectrum of any json file
-- How to run the code: `run_examples(option=1)` with parameters selected in the codes.

    
2. Print/plot arbitrary Json data 
-- Function explanation: plot any spectrum collected from any json file.  
-- How to run the code: `run_examples(option=2)` with parameters selected in the codes. Specifically, 

 3. Convert Json raw data to ML readable data file
-- Function explanation: convert selected json files into training/testing/augment dataset in *CSV* format
-- How to run the code: `run_examples(option=3)` with parameters selected in the codes.

### Related Parameters
**edfaTypes**: booster pre-amplifier EDFA
**gainList**: different gain settings
**channelTypes**: different channel loading condition for each EDFA
**fileList**: 8 commercial grade Lumentum ROADM-20 units deployed in the PAWR COSMOS testbed

```python
edfaTypes = ["preamp","booster"]
gainLists = ["15dB","18dB","21dB"] # for booster
gainLists = ["15dB","18dB","21dB","24dB","27dB"] # for preamp
channelTypes = ['fix', 'random', 'extraRandom', 'extraLow']
roadmNames = ['rdm1-co1', 'rdm2-co1', 'rdm3-co1', 'rdm4-co1',
			'rdm5-co1', 'rdm6-co1', 'rdm1-lg1', 'rdm2-lg1']
subChannelName # please refer to others
spectrumName # please refer to others
```

# Measurement result examples
```
Some example plots here
```


# Related papers


