
import pandas as pd
from pebm_pkg.Intervals_duration import extract_intervals_duration
from pebm_pkg.Waves_characteristics import extract_waves_characteristics


def extraction_MOR_features(signal, freq, features_dict):
    """This function produces the MOR features for a 12-leads ecg and concatenate them into a df"""
    interval_durations_feats = extract_intervals_duration(freq, features_dict)
    waves_characteristics_feats = extract_waves_characteristics(signal, freq, features_dict)
    MOR_features = pd.concat([interval_durations_feats, waves_characteristics_feats], axis=1)
    return MOR_features