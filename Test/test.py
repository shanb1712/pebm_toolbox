
from pebm_pkg.Preprocessing import *
from pebm_pkg.Biomarkers import *
import matplotlib.pyplot as plt
import scipy.io as spio
import numpy as np


keys = ["Pon", "P", "Poff", "QRSon", "Q", "qrs", "S", "QRSoff", "Ton", "T", "Toff", "Ttipo", "Ttipoon",
                    "Ttipooff"]
# download matlab file, define signal and frequency.
#path = 'C:\Sheina\BioMarkers_Repo-baseline\BioMarkers_Repo-baseline\ecg-kit-master\For_Aleksandra'
position_mat = spio.loadmat('position_gr.mat')
ecg_mat = spio.loadmat('human_200Hz_gr.mat')
position = position_mat['position'][0,0]
all_keys =position_mat['position'].dtype.names
position_values =[]
position_keys =[]
# preprocess the position arrays
#-----------------------------------
for i, key in enumerate(all_keys):
    ret_val = position[i].squeeze()
    if (keys.__contains__(key)):

        ret_val[np.isnan(ret_val)] = -1
        ret_val = np.asarray(ret_val, dtype=np.int64)
        position_values.append(ret_val.astype(int))
        position_keys.append(key)
#-----------------------------------

features_dict = dict(zip(position_keys, position_values))

signal = np.asarray(ecg_mat['ecg']).squeeze()
signal= signal[:-1]
freq = ecg_mat['fs'][0,0]
# build a dictinary



# try Extract_mor_features
pre = Preprocessing(signal, freq)
signal_f =pre.notch(50)
signal_f= pre.bpfilt()
t = np.linspace(0,30*60, 30*60*200)


fig = plt.figure()
plt.style.use('bmh')
x1, = plt.plot(t[0:1999], signal[0:1999], 'b')
x2, = plt.plot(t[0:1999], signal_f[0:1999], 'r')
plt. show()

obm = Biomarkers(signal, freq, features_dict)
ints, stat = obm.intervals()


a = 5