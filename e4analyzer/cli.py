import glob
import os
import zipfile
import pandas as pd

from .empatica_e4 import EmpaticaE4
from .hrv_analyzer import HRVAnalyzer

ResourcesPath = 'resources'
ExportPath = 'export'

Conditions = ['Base', 'Task 1', 'Task 2']
Start = [0, 450, 1200]
End = [300, 1050, 1800]
Timer = pd.DataFrame(data={'Start': Start, 'End': End}, index=Conditions)


def main():
    print(os.getcwd())
    if not os.path.exists(ExportPath):
        os.mkdir(ExportPath)

    paths = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*') if not ('.zip' in x)]
    zips = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*.zip')]
    zips = [x for x in zips if ([os.path.splitext(x)[0] in paths])]
    for zip_ in zips:
        extract_zip(zip_)
    paths = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*') if not ('.zip' in x)]

    for path in paths:
        print(path)
        name = os.path.basename(path)
        data = pd.DataFrame(columns=Conditions)
        e4 = EmpaticaE4(path=path)

        ibi = e4.get_ibi()
        base_ibi = ibi[(Timer['Start']['Base'] <= ibi[:, 0]) & (ibi[:, 0] < Timer['End']['Base'])]
        base_ibi[:, 0] -= Timer['Start']['Base']
        task1_ibi = ibi[(Timer['Start']['Task 1'] <= ibi[:, 0]) & (ibi[:, 0] < Timer['End']['Task 1'])]
        task1_ibi[:, 0] -= Timer['Start']['Task 1']
        task2_ibi = ibi[(Timer['Start']['Task 2'] <= ibi[:, 0]) & (ibi[:, 0] < Timer['End']['Task 2'])]
        task2_ibi[:, 0] -= Timer['Start']['Task 2']

        hr = e4.get_hr()
        base_hr = hr[Timer['Start']['Base']:Timer['End']['Base'] - 11]
        task1_hr = hr[Timer['Start']['Task 1']:Timer['End']['Task 1'] - 11]
        hr_length = (Timer['End']['Task 2'] - 10 if Timer['End']['Task 2'] - 10 < len(hr) else len(hr)) - 1
        task2_hr = hr[Timer['Start']['Task 2']:hr_length]

        base_hrv = HRVAnalyzer(ibi=base_ibi, hr=base_hr)
        task1_hrv = HRVAnalyzer(ibi=task1_ibi, hr=task1_hr)
        task2_hrv = HRVAnalyzer(ibi=task2_ibi, hr=task2_hr)

        nnmean = pd.Series([base_hrv.get_nnmean(), task1_hrv.get_nnmean(), task2_hrv.get_nnmean()], index=Conditions,
                           name='NN Mean (ms)')
        data = data.append(nnmean)

        sdnn = pd.Series([base_hrv.get_sdnn(), task1_hrv.get_sdnn(), task2_hrv.get_sdnn()], index=Conditions,
                         name='SDNN (ms)')
        data = data.append(sdnn)

        base_hr_mean = base_hrv.get_hrmean()
        task1_hr_mean = task1_hrv.get_hrmean()
        task2_hr_mean = task2_hrv.get_hrmean()
        hr_mean = pd.Series([base_hr_mean, task1_hr_mean, task2_hr_mean], index=Conditions,
                            name='HR Mean (bpm)')
        data = data.append(hr_mean)

        hr_sd = pd.Series([base_hrv.get_hrsd(), task1_hrv.get_hrsd(), task2_hrv.get_hrsd()], index=Conditions,
                          name='HR SD (bpm)')

        data = data.append(hr_sd)
        base_lf = base_hrv.get_lf()
        task1_lf = task1_hrv.get_lf()
        task2_lf = task2_hrv.get_lf()
        lf = pd.Series([base_lf, task1_lf, task2_lf], index=Conditions,
                       name='LF (ms2/Hz)')
        data = data.append(lf)

        base_hf = base_hrv.get_hf()
        task1_hf = task1_hrv.get_hf()
        task2_hf = task2_hrv.get_hf()
        hf = pd.Series([base_hf, task1_hf, task2_hf], index=Conditions, name='HF(ms2/Hz)')
        data = data.append(hf)

        lf_hf = pd.Series([base_lf / base_hf, task1_lf / task1_hf, task2_lf / task2_hf], index=Conditions, name='LF/HF')
        data = data.append(lf_hf)

        sd1 = pd.Series([base_hrv.get_pp_sd1(), task1_hrv.get_pp_sd1(), task2_hrv.get_pp_sd1()], index=Conditions,
                        name='PP SD1 (ms)')
        data = data.append(sd1)

        sd2 = pd.Series([base_hrv.get_pp_sd2(), task1_hrv.get_pp_sd2(), task2_hrv.get_pp_sd2()], index=Conditions,
                        name='PP SD2 (ms)')
        data = data.append(sd2)

        eda = e4.get_eda()
        base_eda = eda[Timer['Start']['Base'] * 4:Timer['End']['Base'] * 4 - 1]
        task1_eda = eda[Timer['Start']['Task 1'] * 4:Timer['End']['Task 1'] * 4 - 1]
        eda_length = (Timer['End']['Task 2'] * 4 if Timer['End']['Task 2'] * 4 < len(eda) else len(eda)) - 1
        task2_eda = eda[Timer['Start']['Task 2']:eda_length]

        base_eda_mean = base_eda.mean()
        task1_eda_mean = task1_eda.mean()
        task2_eda_mean = task2_eda.mean()
        eda_mean = pd.Series([base_eda_mean, task1_eda_mean, task2_eda_mean], index=Conditions,
                             name='EDA Mean (uS)')
        data = data.append(eda_mean)

        eda_sd = pd.Series([base_eda.std(ddof=1), task1_eda.std(ddof=1), task2_eda.std(ddof=1)], index=Conditions,
                           name='EDA SD (uS)')
        data = data.append(eda_sd)

        base_score = base_hr_mean * base_eda_mean
        task1_score = task1_hr_mean * task1_eda_mean
        task2_score = task2_hr_mean * task2_eda_mean
        score = pd.Series([base_score, task1_score, task2_score], index=Conditions, name='Score (HR*EDA)')
        data = data.append(score)

        data.to_csv(ExportPath + '/_name.csv'.replace('_name', name), float_format='%.3f')


def extract_zip(path):
    if os.path.exists(path):
        with zipfile.ZipFile(path) as existing_zip:
            dir_path = os.path.splitext(path)[0]
            existing_zip.extractall(dir_path)
            return True
    return False
