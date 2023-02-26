import pandas as pd


class CleanData:
    def __init__(self):
        self.window_size = 20
        self.gamma = 0.5

    def calibrate_params(self):
        pass

    def is_outlier(self, series):
        rolling_mean = series.rolling(self.window_size).mean()
        rolling_std = series.rolling(self.window_size).std()
        demeaned_series = (series - rolling_mean).abs()
        2 * rolling_std + self.gamma
