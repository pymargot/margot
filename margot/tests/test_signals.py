from margot import Symbol, MargotDataFrame, Ratio, BaseAlgo, Position, BackTest
from margot import finance, cboe, alphavantage as av

def test_algo():

    class Index(Symbol):
        close = cboe.Column(time_series='close')

    class VXBasis(MargotDataFrame):
        vixm = Index(symbol='VIX', trading_calendar='NYSE')

    class MyAlgo(BaseAlgo):
        data = MargotDataFrame()

    myalgo = MyAlgo(env={})
