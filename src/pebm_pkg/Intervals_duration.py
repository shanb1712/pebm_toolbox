
import numpy as np

#
# def comp_diff(R_points):  # @Jeremy, for PVC detection
#     R_points = np.asarray(R_points)
#     cnt_diff_ecg = []
#     for idx_q in range(1, len(R_points)):
#         cnt_diff = R_points[idx_q] - R_points[idx_q - 1]
#         cnt_diff_ecg.append(cnt_diff)
#     return cnt_diff_ecg

def compute_int(freq, features_dict, factor=1000):
    begin_fiducial = features_dict[0]
    end_fiducial = features_dict[1]
    #int = np.zeros(1,len(begin_fiducial))
    units = (factor / freq)
    int = (end_fiducial - begin_fiducial) * units
    int[(begin_fiducial==-1) | (end_fiducial==-1)] = -1
    return int




# def compute_statistics(freq, features_dict, interval, factor=1000):
#     begin_fiducial = features_dict[0]
#     end_fiducial = features_dict[1]
#     indexes_effectives = begin_fiducial * end_fiducial > 0
#     begin_fiducial = begin_fiducial[indexes_effectives]
#     end_fiducial = end_fiducial[indexes_effectives]
#     units = (factor / freq)  # ms
#     Dival = (end_fiducial - begin_fiducial) * units
#     feat = pd.DataFrame({'Dmed_' + str(interval): [compute_median(Dival)],
#                          # 'Dmean_' + str(interval) + '_' + str(lead): [compute_mean(Dival)],
#                          'Dstd_' + str(interval): [compute_std(Dival)],
#                          # 'Dmax_' + str(interval) + '_' + str(lead): [maximum(Dival)],
#                          })
#     return feat


# def compute_RR_IR_statistics(freq, features_dict, interval, factor=1000):
#     R_points = features_dict[0]
#     R_locations = R_points[R_points > 0]
#     RR_index = R_locations[:-1] * R_locations[1:] > 0
#     rr = np.asarray(comp_diff(R_locations))
#     units = (factor / freq)  # ms
#     Dival = (rr[RR_index]) * units
#     IR = np.asarray(rr[RR_index]) / compute_mean(rr[RR_index])
#     feat = pd.DataFrame({'Dmed_' + str(interval): [compute_median(Dival)],
#                          # 'Dmean_' + str(interval) + '_' + str(lead): [compute_mean(Dival)],
#                          'Dstd_' + str(interval): [compute_std(Dival)],
#                          # 'Dmax_' + str(interval) + '_' + str(lead): [maximum(Dival)],
#                          'IRmedian': [compute_median(IR)],
#                          # 'IRmean_' + str(lead): [compute_mean(IR)],
#                          'IRstd' : [compute_std(IR)],
#                          # 'IRmax_' + str(lead): [maximum(IR)],
#                          })
#     return feat


# def compute_PR2_statistics(freq, features_dict, interval, factor=1000):
#     P_locations = features_dict[0]
#     R_points = features_dict[1]
#     indexes_effectives = R_points * P_locations > 0
#     RR_index = (R_points[:-1] * R_points[1:] > 0)
#     R_points_effective, P_locations_effective = R_points[indexes_effectives], P_locations[indexes_effectives]
#     units = (factor / freq)  # ms
#     PR_interval = (R_points_effective - P_locations_effective) * units
#     RR_interval = (np.asarray(comp_diff(R_points))) * units
#     final_index = RR_index * indexes_effectives[1:] > 0
#     PR_interval_final = (R_points[1:][final_index] - P_locations[1:][final_index]) * units
#     if len(PR_interval_final) == len(RR_interval[final_index]) and len(PR_interval_final) > 0:
#         RAPR = compute_mean(PR_interval_final / RR_interval[final_index])
#     elif len(PR_interval_final) > 0:
#         RAPR = compute_mean(PR_interval_final[1:] / RR_interval[final_index])
#     else:
#         RAPR = 0
#     feat = pd.DataFrame({'MDPR' : [compute_median(PR_interval)],
#                          # 'MAPR_' + str(lead): [compute_mean(PR_interval)],
#                          'RAPR': [RAPR]})
#     return feat


def compute_QTc(QT,RR, factor=1000):
    # Factor uses to convert between units used for morphological
    # calculation (i.e ms) to sec, which needed for QTc calculation
    # self check: (1) https://www.clinigate.com/clinicalc/corrected-qt-interval-qtc.php
    #             (2) https://www.thecalculator.co/health/QTc-Calculator-385.html
    #QT_keys = ['DmedQTc_b','DmedQTc_frid','DmedQTc_fra',]
    #QTc_dict = {}
    HR = np.median(RR)
    HRf = HR / factor
    n = len(QT)
    QTc_b, QTc_frid, QTc_fra, QTc_hod = [None]*n, [None]*n, [None]*n, [None]*n
    for i, QTi in enumerate(QT):
        if ((HR ==-1)| (QTi==-1)):
            QTc_b[i], QTc_frid[i], QTc_fra[i], QTc_hod[i] = [-1, -1, -1, -1]
        else:
            QTc_b[i] = QTi / np.sqrt(HRf)  # ms
            QTc_frid[i] = QTi / HRf**(1/float(3))  # ms
            QTc_fra[i] = QTi + (0.154 * (1 - HRf) * factor)  # ms
            QTc_hod[i] = QTi + (0.00175 * (60 / HRf - 60) * factor) # ms
    QTc_dict = dict(QTc_b=np.asarray([QTc_b], dtype=np.float64).squeeze(),
                    QTc_frid=np.asarray([QTc_frid], dtype=np.float64).squeeze(),
                    QTc_fra=np.asarray([QTc_fra], dtype=np.float64).squeeze(),
                    QTc_hod=np.asarray([QTc_hod], dtype=np.float64).squeeze())
    return QTc_dict


def extract_intervals_duration(fs, features_dict, factor=1000):
    #feat_df = pd.DataFrame()
    intervals_points = dict(Pwave=[features_dict['Pon'], features_dict['Poff']],
                     PR=[features_dict['Pon'], features_dict['QRSon']],
                     PRseg=[features_dict['Poff'], features_dict['QRSon']],
                     PR2=[features_dict['P'], features_dict['qrs']],
                     QRS=[features_dict['QRSon'], features_dict['QRSoff']],
                     QT=[features_dict['QRSon'], features_dict['Toff']],
                     Twave=[features_dict['Ton'], features_dict['Toff']],
                     TPseg=[features_dict['Toff'][:-1],features_dict['Pon'][1:]],
                     RR=[features_dict['qrs'][:-1], features_dict['qrs'][1:]])
    intervals = {}
    for key in intervals_points:
        intervals[key] = compute_int(fs, intervals_points[key], factor=1000)
    QTc_dict = compute_QTc(intervals['QT'], intervals['RR'], factor=1000)
    intervals.update(QTc_dict)
    return intervals
