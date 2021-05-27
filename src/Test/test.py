from pebm_pkg.Extract_mor_features import extraction_MOR_features
#from Extract_mor_features import
import scipy.io as spio
import numpy as np


keys = ["Pon", "P", "Poff", "QRSon", "Q", "R", "S", "QRSoff", "Ton", "T", "Toff", "Ttipo", "Ttipoon",
                    "Ttipooff"]
# download matlab file, define signal and frequency.
#path = 'C:\Sheina\BioMarkers_Repo-baseline\BioMarkers_Repo-baseline\ecg-kit-master\For_Aleksandra'
position_mat = spio.loadmat('position.mat')
ecg_mat = spio.loadmat('human_200Hz.mat')
position = position_mat['position'][0,0]
all_keys =position_mat['position'].dtype.names
position_values =[]
position_keys =[]
# preprocess the position arrays
#-----------------------------------
for i, key in enumerate(all_keys):
    ret_val = position[i].squeeze()
    if (keys.__contains__(key)):

        ret_val[np.isnan(ret_val)] = 0
        ret_val = np.asarray(ret_val, dtype=np.int64)
        position_values.append(ret_val.astype(int))
        position_keys.append(key)
#-----------------------------------

features_dict = dict(zip(position_keys, position_values))

signal = np.asarray(ecg_mat['ecg'])
freq = ecg_mat['fs'][0,0]
# build a dictinary



# try Extract_mor_features
MOR_features =extraction_MOR_features(signal, freq, features_dict)

a = 5