import numpy as np


class EmpaticaE4:
    _path = ''
    _bvp = np.empty([1, 0])
    _ibi = np.empty([2, 0])
    _hr = np.empty([1, 0])
    _eda = np.empty([1, 0])

    def __init__(self, path):
        self._path = path
        self._bvp = np.loadtxt(self._path + '/BVP.csv', skiprows=2, delimiter=",", dtype=float)
        self._hr = np.loadtxt(self._path + '/IBI.csv', skiprows=1, delimiter=",", dtype=float)
        self._hr = np.loadtxt(self._path + '/HR.csv', skiprows=2, delimiter=",", dtype=float)
        self._eda = np.loadtxt(self._path + '/EDA.csv', skiprows=2, delimiter=",", dtype=float)

    def get_bvp(self):
        return self._bvp

    def get_ibi(self):
        return self._ibi

    def get_hr(self):
        return self._hr

    def get_eda(self):
        return self._eda
