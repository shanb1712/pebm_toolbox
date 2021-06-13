
class FiducialPoints:

    def __init__(self, signal, fs, peaks= None):
        self.signal = signal
        self.fs = fs
        if peaks is None:
            pre = Preprocessing(signal, fs)
        self.peaks= peaks

    def wavedet(self):
        signal = self.signal
        fs = self.fs
        peaks = self.peaks
        #exe from snir
        position = 0
        return position

