import os
from margot import Symbol, MargotDataFrame, Ratio, BaseAlgo, Position, BackTest
from margot import finance, cboe, alphavantage as av

def test_symbol():

    class Equity(Symbol):
        adjusted_close = av.Column(
            time_series='adjusted_close')
        volume = av.Column(
            time_series='volume')

        simple_returns = finance.SimpleReturns(column='adjusted_close')
        log_returns = finance.LogReturns(column='adjusted_close')
        realised_vol = finance.RealisedVolatility(
            column='log_returns', window=30)

        upper_band = finance.UpperBollingerBand(
            column='adjusted_close', window=20, width=2.0)
        sma20 = finance.SimpleMovingAverage(column='adjusted_close', window=20)
        lower_band = finance.LowerBollingerBand(
            column='adjusted_close', window=20, width=2.0)

    env = {'DATA_CACHE': os.path.join(os.getcwd(), 'data')}
    spy = Equity(symbol='SPY', trading_calendar='NYSE', env=env)


def test_frame():

    class Index(Symbol):
        close = cboe.Column(time_series='close')

    class VXBasis(MargotDataFrame):
        vixm = Index(symbol='VIX3M', trading_calendar='NYSE')
        vix3m = Index(symbol='VIX', trading_calendar='NYSE')
        vx_basis = Ratio(
            numerator=vixm.close,
            denominator=vix3m.close,
            label='vx_basis_ratio')

    vxbasis = VXBasis()
    vxbasis.to_pandas()
    vxbasis.vx_basis.latest
    vxbasis.vx_basis.to_pandas()


def test_constructors():

    class Index(Symbol):
        adjusted_close = av.Column(
            time_series='adjusted_close')

    spy = Index(symbol='SPY', trading_calendar='NYSE')
    vtwo = Index(symbol='VTWO', trading_calendar='NYSE')

    assert(
        spy.to_pandas().tail()[
            'SPY', 'adjusted_close'].sum() != vtwo.to_pandas().tail()[
            'VTWO', 'adjusted_close'].sum()
    )


def test_finance_features():

    class Index(Symbol):
        adjusted_close = av.Column(
            time_series='adjusted_close')

        simple_returns = finance.SimpleReturns(column='adjusted_close')
        log_returns = finance.LogReturns(column='adjusted_close')
        real_vol = finance.RealisedVolatility(column='log_returns', window=20)
        sma = finance.SimpleMovingAverage(column='adjusted_close', window=10)
        upper = finance.UpperBollingerBand(
            column='adjusted_close', window=20, width=2.0)
        lower = finance.LowerBollingerBand(
            column='adjusted_close', window=20, width=2.0)

    spy = Index(symbol='SPY', trading_calendar='NYSE')

    spy.to_pandas()
