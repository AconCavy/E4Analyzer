import glob
import os
import zipfile
import pandas as pd

from e4analyzer.empatica_e4 import EmpaticaE4

ResourcesPath = 'resources'
ExportPath = 'export'

Conditions = ['Base', 'Task 1', 'Task 2']
Start = [0, 450, 1200]
End = [300, 1050, 1800]
Timer = pd.DataFrame(data={'Start': Start, 'End': End}, index=Conditions)


def main():
    print(os.getcwd())
    paths = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*') if not ('.zip' in x)]
    zips = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*.zip')]
    zips = [x for x in zips if ([os.path.splitext(x)[0] in paths])]
    for zip_ in zips:
        extract_zip(zip_)
    paths = [x.replace('\\', '/') for x in glob.glob(ResourcesPath + '/*') if not ('.zip' in x)]
    print(paths)
    print(zips)

    for path in paths:
        print(path)
        name = os.path.basename(path)
        data = pd.DataFrame(columns=Conditions)
        e4 = EmpaticaE4(path=path)

        hr = e4.get_hr()
        base_hr = hr[Timer['Start']['Base']:Timer['End']['Base'] - 11]
        task1_hr = hr[Timer['Start']['Task 1']:Timer['End']['Task 1'] - 11]
        hr_length = (Timer['End']['Task 2'] - 10 if Timer['End']['Task 2'] - 10 < len(hr) else len(hr)) - 1
        task2_hr = hr[Timer['Start']['Task 2']:hr_length]
        hr_mean = pd.Series([base_hr.mean(), task1_hr.mean(), task2_hr.mean()], index=Conditions, name='HR Mean')
        data = data.append(hr_mean)

        hr_sd = pd.Series([base_hr.std(ddof=1), task1_hr.std(ddof=1), task2_hr.std(ddof=1)], index=Conditions,
                          name='HR SD')
        data = data.append(hr_sd)

        eda = e4.get_eda()
        base_eda = eda[Timer['Start']['Base'] * 4:Timer['End']['Base'] * 4 - 1]
        task1_eda = eda[Timer['Start']['Task 1'] * 4:Timer['End']['Task 1'] * 4 - 1]
        eda_length = (Timer['End']['Task 2'] * 4 if Timer['End']['Task 2'] * 4 < len(eda) else len(eda)) - 1
        task2_eda = eda[Timer['Start']['Task 2']:eda_length]
        eda_mean = pd.Series([base_eda.mean(), task1_eda.mean(), task2_eda.mean()], index=Conditions, name='EDA Mean')
        data = data.append(eda_mean)

        eda_sd = pd.Series([base_eda.std(ddof=1), task1_eda.std(ddof=1), task2_eda.std(ddof=1)], index=Conditions,
                           name='EDA SD')
        data = data.append(eda_sd)

        base_score = base_hr.mean() * base_eda.mean()
        task1_score = task1_hr.mean() * task1_eda.mean()
        task2_score = task2_hr.mean() * task2_eda.mean()
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


if __name__ == '__main__':
    main()
