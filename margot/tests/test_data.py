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
    from margot.data.fields import av
    from margot.data import features

    class Equity(Symbol):
        adjusted_close = av.Field(function='historical_daily_adjusted', field='adjusted_close')
        volume = av.Field(function='historical_daily_adjusted', field='volume')

        simple_returns = features.SimpleReturns(field='adjusted_close')
        log_returns = features.LogReturns(field='adjusted_close')
        realised_vol = features.RealisedVolatility(field='log_returns', window=30)

    env = { 'DATA_CACHE': os.path.join( os.getcwd(), 'data' ) }
    spy = Equity(symbol='SPY', env=env)
    