import os
import logging
from datetime import date, datetime, timedelta

import pandas as pd
import numpy as np

import pytz


class BackTest(object):
    """Backtest an trading algo that's a descendent of BaseAlgo.

    .. warning:: **BackTest is still a work in progress - it probably doesn't
        even work yet!**

    Attributes:
        algo: A boolean indicating if we like SPAM or not.
        starting_balance: An integer count of the eggs we have laid.
    """

    positions = None
    algo = None
    symbols = set()

    def __init__(self, algo, start_balance=100000):   # noqa: D107
        self.start_balance = start_balance
        self.algo = algo
        self.positions = None
        self.trades = None
        self.returns = pd.DataFrame(
            columns=[
                'simple_returns',
                'log_returns'],
            dtype='float64')

    def calculate_returns(self):
        """Calculate returns.

        Assumes the trade is made the next period after a signal is generated.

        You should construct your MargotDataFrame to be indexed by the trading
        periods (e.g. days).
        """
        #TODO: Remove the assumption about simple_returns. i reckon look for the
        # column, then derive simple then log returns.

        returns = self.positions.shift()
        for column in returns.columns: 
            returns.loc[:, column] = self.algo.data.to_pandas(
            ).loc[:, (column, 'simple_returns')] * returns.loc[:, column]

        returns.loc[:, 'simple_returns'] = returns.sum(axis=1)
        returns['log_returns'] = np.log(1 + returns['simple_returns'])
        return returns.replace(np.nan, 0)

    def create_trade_signals_timeseries(self):
        """Create time-series of when position changes occur.

        Return the subset of the positions time-series to indicate positions
            when signals indicate trade should be placed.

        Returns:
            pd.DataFrame: A dataframe of signals when changes to positions are
                suggested.
        """
        # We must start with an uninvested position.
        self.positions.head(1).replace([1.0, -1.0], 0, inplace=True)
        return self.positions.diff().replace(0, np.nan).dropna(how='all')

    def create_position_timeseries(self, periods):
        """Create Position time-series from signals.

        Runs through all of the backtest data, generating position indicating
        signals.

        Args:
            periods (int): the number of periods to backtest over,
                counted back from the end of the dataset. If no value is
                supplied then the whole dataset is used.

        Returns:
            pd.DataFrame: time-series of Positions
        """
        pos = pd.DataFrame()

        if periods:
            index = self.algo.data.to_pandas(periods).index
        else:
            index = self.algo.data.index

        for ts in index:
            mapper = {}
            pos_list = self.algo.simulate_signal(ts)
            for p in pos_list:
                mapper.update(p.as_map())

            pos = pos.append(pd.DataFrame(mapper, index=[ts]))
        return pos

    def run(self, periods=None):
        """Run the backtest.

        Returns:
            [type]: [description]
        """
        # first calculate the positions time series
        self.positions = self.create_position_timeseries(periods)
        # deduce the trades; simulate entry and exit prices.
        self.trade_signals = self.create_trade_signals_timeseries()

        # Consider the algo being run on 1st day of month e.g. RP
        # can calculate returns daily based on positions held - and
        #   schedule algo runs on e.g. 1st of month.

        # calculate the returns.
        self.returns = self.calculate_returns()
        # caclulate lookback rolling volatility
        # simulate resizing at trading time, according to a target volatility
        # simulate volatility sized returns.
        return self.returns

    def volatility(self, days=30, periods=252):
        """Return a single float value for realised historical volatility.

        TODO: Change the periods parameter to instead examine the data.
        Args:
            days (int, optional): Days to lookback. Defaults to 30.
        """
        # TODO: tail(days) assumes daily.
        return self.returns.log_returns.tail(days).std() * np.sqrt(252)



