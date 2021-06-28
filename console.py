import math
import sys
import os
import json
import numpy as np
import warnings

# Classes import
from src.pebm_pkg.Biomarkers import Biomarkers
from src.pebm_pkg.FiducialPoints import FiducialPoints
from src.pebm_pkg.Preprocessing import Preprocessing 

# Functions import
from src.pebm_pkg.fecgyn_tgen import *
from src.pebm_pkg.Intervals_duration import *
from src.pebm_pkg.Waves_characteristics import *
from src.pebm_pkg.Statistics import *


def biomarkers_intervals(signal, **kwargs):
    bm = Biomarkers(signal, **kwargs)
    return bm.intervals()

def biomarkers_waves(signal, **kwargs):
    bm = Biomarkers(signal, **kwargs)
    return bm.waves()

def fiducial_points(signal, **kwargs):
    fp = FiducialPoints(signal, **kwargs)
    return fp.wavedet()

def preprocessing_notch(signal, **kwargs):
    pp = Preprocessing(signal, **kwargs)
    return pp.notch(kwargs['notch_freq'])

def preprocessing_bpflit(signal, **kwargs):
    pp = Preprocessing(signal, **kwargs)
    return pp.bpfilt()

def preprocessing_bsqi(signal, **kwargs):
    pp = Preprocessing(signal, **kwargs)
    return pp.bsqi()

def preprocessing_epltd(signal, **kwargs):
    pp = Preprocessing(signal, **kwargs)
    return pp.epltd()



# ignore all warning at runtime
warnings.filterwarnings("ignore")

# Internal Exceptions
class InvalidArgsException(Exception):
    pass

class FunctionCallException(Exception):
    pass

def read_signal_file(signal_file):
    with open(signal_file, "r") as _file:
        signal = [str(line).strip() for line in _file.readlines()]
        if "sample rate" in signal[0].lower():
            signal = signal[1:]
        return np.array(signal).astype(np.float)

def read_signal_vec(signal_vec):
    return np.array(signal_vec).astype(np.float)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise InvalidArgsException()
    else:
        # Arguments Processing
        signal_path = sys.argv[1]
        signal = read_signal_file(signal_path)
        func_name = sys.argv[2]
        func_args = json.loads(str(sys.argv[3])) if len(sys.argv)>3 else None

        # Function Call
        if func_name not in globals().keys():
            raise NotImplementedError("function {} is not implemented".format(func_name))
        else:
            func = globals()[func_name]
            try:
                if isinstance(func_args, list):
                    res = func(signal, *func_args)
                elif isinstance(func_args, dict):
                    res = func(signal, **func_args)
                elif func_args is None:
                    res = func(signal)
                if isinstance(res, np.ndarray):
                    print(json.dumps(res.tolist()))
                else:
                    print(str(res))
            except Exception:
                raise FunctionCallException()