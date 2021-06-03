import sys

sys.path.append("/afib/parser/utils")
sys.path.append("/afib/preprocessing")
sys.path.append("/afib")

import mne
import numpy as np
from scipy.signal import savgol_filter, butter, sosfreqz, sosfiltfilt


def cut_signal(signal, signal_freq, start_time, end_time):
    if start_time > end_time:
        return 1
    if start_time > len(signal)*(1/signal_freq) or end_time > len(signal)*(1/signal_freq):
        return 1

    start_sample = np.floor(start_time*signal_freq)
    end_sample = np.floor(start_time * signal_freq)
    return signal[start_sample: end_sample]


def notch_filter(signal, signal_freq, pl_freq):
    y = mne.filter.notch_filter(signal.astype(np.float), signal_freq, freqs=pl_freq)
    return y


def bandpass_filter(signal,signal_freq):
    """
    This function uses a Butterworth filter. The coefficoents are computed automatically.
    Lowcut and highcut are in Hz
    """
    filter_order = 75 #??
    low_cut = 0.67
    high_cut = 100

    nyquist_freq = 0.5 * signal_freq
    low = low_cut / nyquist_freq
    high = high_cut / nyquist_freq
    sos = butter(filter_order, [low, high], btype="band", output='sos', analog=False)
    y = sosfiltfilt(sos, signal)
    return y








