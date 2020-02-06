import numpy as np
from astropy.timeseries import lombscargle


class HRVAnalyzer:
    VLF_MIN = 0.0
    VLF_MAX = 0.04
    LF_MIN = 0.04
    LF_MAX = 0.15
    HF_MIN = 0.15
    HF_MAX = 0.4

    _ibi = np.empty([2, 0])
    _hr = np.empty([1, 0])
    _frequency = np.empty([1, 0])
    _power = np.empty([1, 0])
    _band_vlf = np.empty([1, 0])
    _band_lf = np.empty([1, 0])
    _band_hf = np.empty([1, 0])

    def __init__(self, ibi, hr):
        self._ibi = ibi
        self._hr = hr
        self._frequency, self._power = lombscargle.LombScargle(self._ibi[:, 0], self._ibi[:, 1],
                                                               normalization='psd').autopower(method='fast')
        self._band_vlf = (self._frequency >= self.VLF_MIN) & (self._frequency < self.VLF_MAX)
        self._band_lf = (self._frequency >= self.LF_MIN) & (self._frequency < self.LF_MAX)
        self._band_hf = (self._frequency >= self.HF_MIN) & (self._frequency < self.HF_MAX)

    def get_nnmean(self):
        return self._ibi[:, 1].mean()

    def get_sdnn(self):
        return self._ibi[:, 1].std(ddof=1)

    def get_hrmean(self):
        return self._hr.mean()

    def get_hrsd(self):
        return self._hr.std(ddof=1)

    def get_vlf(self):
        return self.get_freq(self._band_vlf)

    def get_vlf_peak_freq(self):
        return self.get_peak_freq(self._band_vlf)

    def get_lf(self):
        return self.get_freq(self._band_lf)

    def get_lf_peak_freq(self):
        return self.get_peak_freq(self._band_lf)

    def get_hf(self):
        return self.get_freq(self._band_hf)

    def get_hf_peak_freq(self):
        return self.get_peak_freq(self._band_hf)

    def get_tf(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_freq(band)

    def get_tf_peak_freq(self):
        band = (self._frequency >= self.VLF_MIN) & (self._frequency < self.HF_MAX)
        return self.get_peak_freq(band)

    def get_freq(self, band):
        return np.trapz(y=self._power[band], x=self._frequency[band])

    def get_peak_freq(self, band):
        return self._frequency[band][self._power[band].argmax()]

    def get_pp_sd1(self):
        tmp = (self._ibi[:-1, 1] - self._ibi[1:, 1]) / np.sqrt(2)
        return tmp.std(ddof=1)

    def get_pp_sd2(self):
        tmp = (self._ibi[:-1, 1] + self._ibi[1:, 1]) / np.sqrt(2)
        return tmp.std(ddof=1)

    def get_freq_features(self):
        return self._frequency, self._power, [self._band_vlf, self._band_lf, self._band_hf]
