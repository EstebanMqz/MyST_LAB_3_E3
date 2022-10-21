
"""
# -- ---------------------------------------------------------------------------------------------------------      -- #
# -- project: Lab 3 (Behavioral Finance) is a project that has tools to analyze the performance of trade history.   -- #
# -- script: functions.py : Python script with the main functionality                                               -- #
# -- author: EstebanMqz                                                                                             -- #
# -- license: GNU General Public License v3.0                                                                       -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_3_E3                                                        -- #
# -- ---------------------------------------------------------------------------------------------------------      -- #
"""

import numpy as np
import plotly.graph_objects as go #plotly
import plotly.express as px
from data import *


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def s_metrics(prices):
    """
    Function that calculates daily simple return metrics of prices.

        Parameters
        ----------
        prices: dataframe of price(s).

        Returns
        -------
        returns: Simple returns on a daily basis.
        mean_returns: Mean of returns (annualized).
        cov: Covariance (annualized).
        index: Name of the metrics dataframe calculated as str.
    """
    returns = prices.pct_change().fillna(0) #NAs filled w/ 0s to preserve daily returns for all rows (days) in every column (ticker)
    mean_ret = returns.mean() * 252 #E(r)
    cov = returns.cov() * 252 #Covariance

    return returns, mean_ret, cov

