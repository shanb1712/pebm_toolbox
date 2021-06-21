import pandas as pd
#from pebm_pkg.Preprocessing_features import compute_mean, compute_median, compute_std, minimum, maximum
import numpy as np

def compute_Amp(ecg, freq, features_dict, factor=1000):

    amp = np.ones(len(features_dict[0]))*-1
    if len(features_dict) == 1:
        amp[features_dict[0] != -1] = ecg[features_dict[0][features_dict[0] != -1]]

    else:
        begin_amp = np.ones(len(features_dict[0])) * -1
        end_amp = np.ones(len(features_dict[0])) * -1
        begin_amp[features_dict[0] != -1] = ecg[features_dict[0][features_dict[0] != -1]]
        end_amp[features_dict[1] != -1] = ecg[features_dict[1][features_dict[1] != -1]]
        amp = np.abs(end_amp - begin_amp)
        amp[(begin_amp == -1) | (end_amp == -1)] = -1

    return amp

def compute_Area(ecg, freq, features_dict, factor=1000):

    begin_fiducial = features_dict[0]
    end_fiducial = features_dict[1]
    area = np.ones(len(features_dict[0]))*-1
    r_index = (begin_fiducial != -1) & (end_fiducial != -1)
    area = area[r_index]
    bfi = begin_fiducial[r_index].astype(int)
    efi = end_fiducial[r_index].astype(int)
    for i in range(0, len(bfi)-1):
        area[i] = np.sum(np.abs(ecg[bfi[i]: efi[i]]))

    units = (factor / freq)
    area= area*units
    return area




# def comp_diff(R_points):  # @Jeremy, for PVC detection
#     R_points = np.asarray(R_points)
#     cnt_diff_ecg = []
#     for idx_q in range(1, len(R_points)):
#         cnt_diff = R_points[idx_q] - R_points[idx_q - 1]
#         cnt_diff_ecg.append(cnt_diff)
#     return cnt_diff_ecg
#
#
# def calculate_QRS_Area(ecg, QRSOn, QRSOff):
#     """
#     Automatic detection of premature atrial contractions in the electrocardiogram Vessela T. Krasteva, Irena I. Jekova, Ivaylo I. Christov
#     """
#     QRS_Area = np.zeros(len(QRSOn))
#     for i in range(len(QRSOn)):
#         QRS_Area[i] = np.sum(np.abs(ecg[QRSOn[i]: QRSOff[i]]))
#     Median_5_Area = []
#     for i in range(5, len(QRSOn)):
#         Median_5_Area.append(compute_median(QRS_Area[i - 5:i]))
#     Median_5_Area = np.asarray(Median_5_Area)
#     if len(QRS_Area) < 6:
#         return [0]
#     return (np.abs(QRS_Area[5:] - Median_5_Area) / Median_5_Area) * 100
#
#
# def calculate_QRS_Width(QRSOn, QRSOff):
#     """
#     Automatic detection of premature atrial contractions in the electrocardiogram Vessela T. Krasteva, Irena I. Jekova, Ivaylo I. Christov
#     """
#     QRS_Width = np.asarray(np.asarray(QRSOff) - np.asarray(QRSOn))
#     Median_5_Width = []
#     for i in range(5, len(QRSOn)):
#         Median_5_Width.append(compute_median(QRS_Width[i - 5:i]))
#     Median_5_Width = np.asarray(Median_5_Width)
#     if len(QRS_Width) < 6:
#         return [0]
#     return (np.abs(QRS_Width[5:] - Median_5_Width) / Median_5_Width) * 100
#
#
# def compute_statistics(ecg, features_dict, interval):
#     begin_fiducial = features_dict[0]
#     end_fiducial = features_dict[1]
#     indexes_effectives = begin_fiducial * end_fiducial > 0
#     interval_ref = min(len(begin_fiducial), len(end_fiducial))
#     begin_fiducial = begin_fiducial[:interval_ref]
#     end_fiducial = end_fiducial[:interval_ref]
#     indexes_effectives = indexes_effectives[:interval_ref]
#     begin_fiducial = begin_fiducial[indexes_effectives]
#     end_fiducial = end_fiducial[indexes_effectives]
#     ecg_intervals = [ecg[begin_fiducial[i]:end_fiducial[i]] for i in range(len(begin_fiducial))]
#     ecg_intervals_mean = [compute_mean(ecg_intervals[i]) for i in range(len(ecg_intervals))]
#     ecg_intervals_median = [compute_median(ecg_intervals[i]) for i in range(len(ecg_intervals))]
#     ecg_intervals_std = [compute_std(ecg_intervals[i]) for i in range(len(ecg_intervals))]
#     ecg_intervals_max = [maximum(ecg_intervals[i]) for i in range(len(ecg_intervals))]
#     feat = pd.DataFrame({'med_' + str(interval): [compute_median(ecg_intervals_median)],
#                          # 'mean_' + str(interval) + '_' + str(lead): [compute_mean(ecg_intervals_mean)],
#                          'std_' + str(interval): [compute_std(ecg_intervals_std)],
#                          # 'max_' + str(interval) + '_' + str(lead): [maximum(ecg_intervals_max)],
#                          })
#     return feat
#
#
# def compute_RR_statistics(ecg, features_dict, interval):
#     R_points = features_dict[0]
#     RR_index = R_points[:-1] * R_points[1:] > 0
#     R_points_RR = R_points[:-1][RR_index]
#     ecg_intervals = np.asarray(ecg[R_points_RR])
#     DR = ecg_intervals[1:] - ecg_intervals[:-1]
#     feat = pd.DataFrame({'med_' + str(interval): [compute_median(ecg_intervals)],
#                          # 'mean_' + str(interval) + '_' + str(lead): [compute_mean(ecg_intervals)],
#                          'std_' + str(interval): [compute_std(ecg_intervals)],
#                          # 'max_' + str(interval) + '_' + str(lead): [maximum(ecg_intervals)],
#                          'med_D' + str(interval): [compute_median(DR)],
#                          # 'mean_D' + str(interval) + '_' + str(lead): [compute_mean(DR)],
#                          'std_D' + str(interval): [compute_std(DR)],
#                          # 'max_D' + str(interval) + '_' + str(lead): [maximum(DR)],
#                          })
#     return feat
#
#
# def compute_QRS_measures(ecg, freq, features_dict,interval):
#     QRSon_points = features_dict[0]
#     QRSoff_points = features_dict[1]
#     indexes_effectives = QRSon_points * QRSoff_points > 0
#     QRSon_points = QRSon_points[indexes_effectives]
#     QRSoff_points = QRSoff_points[indexes_effectives]
#     QRSon_ecg = ecg[QRSon_points]
#     QRSArea = np.asarray([np.sum(ecg[QRSon_points[i]:QRSoff_points[i]]) for i in range(len(QRSon_points))])
#     QRSAreaDiff = calculate_QRS_Area(ecg, QRSon_points, QRSoff_points)
#     QRSWidthDiff = calculate_QRS_Width(QRSon_points, QRSoff_points)
#     feat = pd.DataFrame({'med_' + str(interval): [compute_median(QRSon_ecg)],
#                          # 'mean_' + str(interval) + '_' + str(lead): [compute_mean(QRSon_ecg)],
#                          'std_' + str(interval): [compute_std(QRSon_ecg)],
#                          # 'max_' + str(interval) + '_' + str(lead): [maximum(QRSon_ecg)],
#                          'Smed_' + str(interval): [compute_median(QRSArea)],
#                          # 'Smean_' + str(interval) + '_' + str(lead): [compute_mean(QRSArea)],
#                          'Sstd_' + str(interval): [compute_std(QRSArea)],
#                          # 'Smax_' + str(interval) + '_' + str(lead): [maximum(QRSArea)],
#                          'Smed_' + str(interval) + '_Diff': [compute_median(QRSAreaDiff)],
#                          # 'Smean_' + str(interval) + '_Diff' + '_' + str(lead): [compute_mean(QRSAreaDiff)],
#                          'Sstd_' + str(interval) + '_Diff': [compute_std(QRSAreaDiff)],
#                          # 'Smax_' + str(interval) + '_Diff' + '_' + str(lead): [maximum(QRSAreaDiff)],
#                          'Dmed_' + str(interval) + '_Diff': [compute_median(QRSWidthDiff)],
#                          # 'Dmean_' + str(interval) + '_Diff' + '_' + str(lead): [compute_mean(QRSWidthDiff)],
#                          'Dstd_' + str(interval) + '_Diff': [compute_std(QRSWidthDiff)],
#                          # 'Dmax_' + str(interval) + '_Diff' + '_' + str(lead): [maximum(QRSWidthDiff)],
#                          })
#
#     J_offset = int(0.04*freq) #40ms after the QRSoff
#     QRSoff_points = np.asarray(QRSoff_points)
#     QRSoff_points = QRSoff_points[QRSoff_points + J_offset < len(ecg)]
#     J_ecg = ecg[QRSoff_points + J_offset]
#     feats_J = pd.DataFrame({'med_J_': [compute_median(J_ecg)],
#                             # 'mean_J_' + str(lead): [compute_mean(J_ecg)],
#                             'std_J_': [compute_std(J_ecg)],
#                             # 'max_J_' + str(lead): [maximum(J_ecg)],
#                             })
#     feats = pd.concat([feat, feats_J], axis=1)
#     return feats


def extract_waves_characteristics(ecg, freq, features_dict):

    amplitude_points = dict(Pwave_amp=[features_dict['P'], features_dict['Poff']],
                     Twave_amp=[features_dict['T'], features_dict['Toff']],
                     Rwave_amp=[features_dict['qrs']],
                     STamp=[features_dict['QRSoff'], features_dict['Ton']])
    area_points = dict(Parea=[features_dict['Pon'], features_dict['Poff']],
                 Tarea=[features_dict['Ton'], features_dict['Toff']],
                 QRSarea=[features_dict['QRSon'], features_dict['QRSoff']])
    amplitude = {}
    for key in amplitude_points:
        amplitude[key] = compute_Amp(ecg, freq, amplitude_points[key], factor=1000)
    area ={}
    for key in area_points:
        area[key] = compute_Area(ecg, freq, area_points[key], factor=1000)
    J_offset = int(0.04 * freq)
    J_ecg = ecg[features_dict['QRSoff'] + J_offset]
    J_point= dict(Jpoint = J_ecg)
    Waves = {}
    Waves.update(amplitude)
    Waves.update(area)
    Waves.update(J_point)

    return Waves