import numpy as np
from astropy.stats import lombscargle


class HRVAnalyzer:
    VLF_MIN = 0.0
    VLF_MAX = 0.04
    LF_MIN = 0.04
    LF_MAX = 0.15
    HF_MIN = 0.15
    HF_MAX = 0.4

    _bvp = np.empty([1, 0])
    _ibi = np.empty([2, 0])
    _hr = np.empty([1, 0])
    _frequency = np.empty([1, 0])
    _power = np.empty([1, 0])

    def __init__(self, bvp, ibi, hr):
        self._bvp = bvp
        self._ibi = ibi
        self._ibi[:, 1] = self._ibi[:, 1] * 1000
        self._hr = hr

        print(self._ibi[:, 1])
        self._frequency, self._power = lombscargle.LombScargle(self._ibi[:, 0], self._ibi[:, 1],
                                                               normalization='psd').autopower(method='fast')

    def get_nnmean(self):
        return self._ibi.mean()

    def get_sdnn(self):
        return self._ibi.std(ddof=1)

    def get_hrmean(self):
        return self._hr.mean()

    def get_vlf(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.VLF_MAX)
        return self.get_freq(band)

    def get_vlf_peak_freq(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.VLF_MAX)
        return self.get_peak_freq(band)

    def get_lf(self):
        band = (self._frequency >= self.LF_MIN) & (self._frequency < self.LF_MAX)
        return self.get_freq(band)

    def get_lf_peak_freq(self):
        band = (self._frequency >= self.LF_MIN) & (self._frequency < self.LF_MAX)
        return self.get_peak_freq(band)

    def get_hf(self):
        band = (self._frequency >= self.HF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_freq(band)

    def get_hf_peak_freq(self):
        band = (self._frequency >= self.HF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_peak_freq(band)

    def get_tf(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_freq(band)

    def get_tf_peak_freq(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_peak_freq(band)

    def get_freq(self, band):
        return np.trapz(y=abs(self._power[band]), x=None, dx=0.1)

    def get_peak_freq(self, band):
        return self._frequency[band][self._power[band].argmax()]
