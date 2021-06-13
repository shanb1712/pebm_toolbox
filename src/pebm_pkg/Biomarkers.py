
from pebm_pkg.FiducialPoints  import *
from pebm_pkg.Intervals_duration import *
#from pebm_pkg.Waves_characteristics import *
from pebm_pkg.Statistics import *

class Biomarkers:
    def __init__(self, signal, fs, position =None):
        self.signal = signal
        self.fs = fs
        self.position = position
        self.intervals_b = {}
        self.waves_b = {}
        self.intervals_statistics ={}
        self.waves_statistics = {}

        if position is None:
            fp = FiducialPoints(signal, fs)
            position = fp.wavedet()
        self.position = position

    def intervals(self):
        signal = self.signal
        fs = self.fs
        position = self.position
        self.intervals_b = extract_intervals_duration(fs, position)
        self.intervals_statistics = statistics(self.intervals_b)
        return self.intervals_b, self.intervals_statistics

    def waves(self):
        signal = self.signal
        fs = self.fs
        position = self.position
        self.waves_b = extract_waves_characteristics(signal, fs, position)
        self.waves_statistics = statistics(self.waves_b)
        return self.waves_b, self.waves_statistics

    # def compute_biomarkers(self):
    #     signal = self.signal
    #     fs = self.fs
    #     position = self.position
    #     self.interval_durations = extract_intervals_duration(fs, position)
    #     self.waves_characteristics = extract_waves_characteristics(signal, fs, position)
    #     biomarkers = self.interval_durations.update(self.waves_characteristics)
    #     return biomarkers
    #
    # def compute_stat(self, mode='all'):
    #     signal = self.signal
    #     fs = self.fs
    #     position = self.position
    #     if (mode =='all') | (mode == 'int'):
    #         if not self.interval_durations:
    #             self.interval_durations = extract_intervals_duration(fs, position)
    #
    #     if (mode == 'all') | (mode == 'wav'):
    #         if not self.waves_characteristics:
    #             self.waves_characteristics = extract_waves_characteristics(signal, fs, position)
    #     if (mode == 'int'):
    #         self.statistics = compute_statistics(self.interval_durations)
    #     return self.statistics

