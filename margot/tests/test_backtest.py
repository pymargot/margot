from datetime import datetime

import pytz

from margot.data import Symbol, MargotDataFrame, Ratio
from margot.data.column import cboe
from margot.data.features import finance
from margot.signals import Position, BaseAlgo
from margot.backtest import BackTest


def test_simulation():

    class Index(Symbol):
        close = cboe.Column(time_series='close')
        sma = finance.SimpleMovingAverage(column='close',
                                      window=3)

    class VXBasisDF(MargotDataFrame):
        vix = Index('VIX', trading_calendar='NYSE')
        vix3m = Index('VIX3M', trading_calendar='NYSE')
        ratio = Ratio(numerator=vix.close, 
                    denominator=vix3m.close, 
                    label='vxbasis')

    vxa = VXBasisDF()

    vxb = vxa.to_pandas().copy()

    when = datetime(2020,1,1, tzinfo=pytz.UTC)
    vxa.simulate(when)

    assert(vxb[:when].equals(vxa.to_pandas()))
