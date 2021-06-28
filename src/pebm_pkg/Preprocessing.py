
import numpy as np
import mne
from scipy.signal import butter, sosfiltfilt



class Preprocessing:

    def __init__(self, signal, fs):
        self.signal = signal
        self.fs = fs
        self.notch_freq = None #canbe 60 or 50 HZ

    # def cut_signal(self, start_time, end_time):
    #     signal = self.signal
    #     fs = self.fs
    #     if start_time > end_time:
    #         return 1
    #     if start_time > len(self.signal)*(1/fs) or end_time > len(signal)*(1/fs):
    #         return 1
    #
    #     start_sample = np.floor(start_time* fs)
    #     end_sample = np.floor(start_time * fs)
    #     return signal[start_sample: end_sample]


    def notch(self, notch_freq):
        signal = self.signal
        fs = self.fs
        self.notch_freq = notch_freq
        # notch_freq have to be 50 or 60 HZ (make that condition)
        fsig = mne.filter.notch_filter(signal.astype(np.float), fs, freqs=notch_freq)
        self.signal =fsig
        return fsig


    def bpfilt(self):
        """
        This function uses a Butterworth filter. The coefficoents are computed automatically.
        Lowcut and highcut are in Hz
        """
        signal = self.signal
        fs = self.fs
        filter_order = 75 #??
        low_cut = 0.67
        high_cut = 100

        nyquist_freq = 0.5 * fs
        low = low_cut / nyquist_freq
        high = high_cut / nyquist_freq
        if fs <= high_cut*2:
            sos = butter(filter_order, low, btype="high", output='sos', analog=False)
        else:
            sos = butter(filter_order, [low, high], btype="band", output='sos', analog=False)
        fsig = sosfiltfilt(sos, signal)
        self.signal = fsig
        return fsig

    def bsqi(self):
        bsqi =0
        return bsqi

    def epltd(self):
        peaks = None
        return peaks

