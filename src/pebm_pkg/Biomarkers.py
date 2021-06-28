
from src.pebm_pkg.FiducialPoints  import *
from src.pebm_pkg.Intervals_duration import *
from src.pebm_pkg.Waves_characteristics import *
from src.pebm_pkg.Statistics import *

class Biomarkers:
    def __init__(self, signal, fs, fiducials =None):
        self.signal = signal
        self.fs = fs
        self.fiducials = fiducials
        self.intervals_b = {}
        self.waves_b = {}
        self.intervals_statistics ={}
        self.waves_statistics = {}

        if fiducials is None:
            fp = FiducialPoints(signal, fs)
            fiducials = fp.wavedet()
        self.fiducials = fiducials

    def intervals(self):
        signal = self.signal
        fs = self.fs
        fiducials = self.fiducials
        self.intervals_b = extract_intervals_duration(fs, fiducials)
        self.intervals_statistics = statistics(self.intervals_b)
        return self.intervals_b, self.intervals_statistics

    def waves(self):
        signal = self.signal
        fs = self.fs
        fiducials = self.fiducials
        self.waves_b = extract_waves_characteristics(signal, fs, fiducials)
        self.waves_statistics = statistics(self.waves_b)
        return self.waves_b, self.waves_statistics



