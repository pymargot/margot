"""
class Equity(Symbol):
    log_returns = column.LogReturns(field='adjusted_close')
    3dma = column.RollingSimpleMovingAverage(field='adjusted_close', lookback=3)
    std20 = column.RollingStandardDeviation(field='log_returns', lookback=20)
    upper = column.UpperBollingerBand(field='adjusted_close', std=2)
    lower = columnn.LowerBollingerBand(field ='adjusted_close', std =2)

 class VXDataset(DataSet):
    vixm = Equity(symbol='VIXM')
    ixv = Equity(symbol='IXV')
    vix3m = Index(symbol='^VXV')
    vix = Index(symbol='^VIX')

ds = VXDataset()
df = ds.get_pandas(start, end)
"""


def test_symbol():
    import os
    from margot.data import Symbol
    from margot.data.column import av
    from margot.data import feature

    class Equity(Symbol):
        adjusted_close = av.Column(
            function='historical_daily_adjusted',
            column='adjusted_close')
        volume = av.Column(
            function='historical_daily_adjusted',
            column='volume')

        simple_returns = feature.SimpleReturns(column='adjusted_close')
        log_returns = feature.LogReturns(column='adjusted_close')
        realised_vol = feature.RealisedVolatility(
            column='log_returns', window=30)

        upper_band = feature.UpperBollingerBand(
            column='adjusted_close', window=20, width=2.0)
        sma20 = feature.SimpleMovingAverage(column='adjusted_close', window=20)
        lower_band = feature.LowerBollingerBand(
            column='adjusted_close', window=20, width=2.0)

    env = {'DATA_CACHE': os.path.join(os.getcwd(), 'data')}
    spy = Equity(symbol='SPY', env=env)
