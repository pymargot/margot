

def test_algo():
    from margot.signals import algos
    from margot.data import MargotDataFrame, Symbol, Ratio
    from margot.data.column import cboe

    class Index(Symbol):
        close = cboe.Column(time_series='close')

    class VXBasis(MargotDataFrame):
        vixm = Index(symbol='VIX', trading_calendar='NYSE')

    class MyAlgo(algos.BaseAlgo):
        data = MargotDataFrame()

    myalgo = MyAlgo(env={})
