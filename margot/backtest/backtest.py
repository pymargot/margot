import os
import logging
from datetime import date, datetime, timedelta

import pandas as pd
import numpy as np

import pytz


class BackTest(object):
    """Backtest an trading algo that's a descendent of BaseAlgo.

    _BackTest is still a work in progress - it probably doesn't even work yet_

    Attributes:
        algo: A boolean indicating if we like SPAM or not.
        starting_balance: An integer count of the eggs we have laid.
    """

    positions = None
    algo = None
    symbols = set()

    def __init__(self, algo_class, start_balance=100000):   # noqa: D107
        self.start_balance = start_balance
        self.algo_class = algo_class
        self.algo = algo_class()
        self.positions = None
        self.trades = None
        self.returns = pd.DataFrame(
            columns=[
                'returns',
                'log_returns'],
            dtype='float64')

    def calc_daily_returns(self, day):
        """Calculate the returns based on yesterdays positions, MoC to MoC.

        Args:
            day (date): the date for which we calculate returns.

        Daily returns are the difference between yesterdays adjusted_close
        and todays adjusted_close.
        """
        simple_returns = 0.0

        for symbol in self.symbols:
            # simple_returns = yesterdays_positions * todays_pct_change
            try:
                todays_pct_change = self.algo.symbols[symbol].data.pct_change(
                ).loc[day].adjusted_close
                yesterdays_position = self.positions.shift().loc[day, symbol]
                simple_returns = simple_returns + \
                    (todays_pct_change * yesterdays_position)
            except KeyError:
                pass
        self.positions.at[day, 'returns'] = simple_returns
        self.positions.at[day, 'log_returns'] = np.log(1 + simple_returns)

        return self.positions.dropna()

    def walk_forward(self, start: date, end: date):
        """Backtest the algo, walk forward for every trading day in the date range.

        Calculates the returns from taking the previous days positions.

        Args:
            start (date): The first day of the backtest.
            end (date): The last day of the backtest.

        Return:
            a DataFrame of daily simple returns, and log returns.

        Note: A walk forward backtest is much slower than backtesting a dataframe with shift(),
        but we can use it on the same algo that is deployed live. It's also a good way to standardise
        backtesting so that we can keep margot simple, and reuse performance calcs etc.
        """
        trading_days = get_calendar(
            self.algo.calendar).schedule[start:end].index

        for day in trading_days:
            # TODO simplify this.
            row = [p.as_dict() for p in self.algo.execute(day)]
            mapper = {k: v for d in row for k, v in d.items()}
            self.symbols = self.symbols.union(mapper.keys())
            self.positions = self.positions.append(
                pd.DataFrame(mapper, index=[day]))
            self.calc_daily_returns(day)
        return self.positions

    def create_position_timeseries(self):
        """Create Position time-series from signals.

        Runs through all of the backtest data by default.

        Returns:
            pd.DataFrame: time-series of Positions
        """
        pos = pd.DataFrame()
        for ts in self.algo.data.index: ### <- index will be a subset
            mapper = {}
            pos_list = self.algo.simulate_signal(ts)
            for p in pos_list:
                mapper.update(p.as_map())
            pos = pos.append(
                pd.DataFrame(mapper, index=[ts])
            )
        return pos

    def run(self):
        """Run the backtest.

        Returns:
            [type]: [description]
        """
        # first calculate the positions time series
        self.positions = self.create_position_timeseries()
        # deduce the trades; simulate entry and exit prices.
        # calculate the returns.
        # caclulate lookback rolling volatility
        # simulate resizing at trading time, according to a target volatility
        # simulate volatility sized returns.
        return self.positions
