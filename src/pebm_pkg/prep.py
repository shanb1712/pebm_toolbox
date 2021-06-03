import sys

sys.path.append("/afib/parser/utils")
sys.path.append("/afib/preprocessing")
sys.path.append("/afib")
import csv
import os
import h5py
import mne
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import physionet_matlab
import scipy
import wfdb.processing
import consts as cts
import pathlib
from scipy.signal import savgol_filter, butter, sosfreqz, sosfiltfilt



bandpass_filter(ecg_lead, id, l, 0.67, 100, fs, 75, debug=False)



def bandpass_filter(data, id, lead, lowcut, highcut, signal_freq, filter_order, debug=False):
    """This function uses a Butterworth filter. The coefficoents are computed automatically. Lowcut and highcut are in Hz"""
    nyquist_freq = 0.5 * signal_freq
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq
    sos = butter(filter_order, [low, high], btype="band", output='sos', analog=False)
    y = sosfiltfilt(sos, data)
    y = mne.filter.notch_filter(y.astype(np.float), signal_freq, freqs=60, verbose=debug)
    if debug:
        filename_freq = "exam_" + str(id) + "_lead_" + str(lead) + ".png"
        filename_spect = "exam_" + str(id) + "_lead_" + str(lead) + "_spect.png"

        # get_freq_plot(data, y, sos, filter_order, signal_freq, filename_freq)
        get_spect_plot(data, y, signal_freq, filename_spect, dpi=400)
    return y








