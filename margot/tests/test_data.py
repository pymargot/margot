import os


def test_symbol():
    from margot.data import Symbol
    from margot.data.column import alphavantage as av
    from margot.data.features import finance

    class Equity(Symbol):
        adjusted_close = av.Column(
            function='historical_daily_adjusted',
            time_series='adjusted_close')
        volume = av.Column(
            function='historical_daily_adjusted',
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
    spy = Equity(symbol='SPY', env=env)


def test_frame():
    from margot.data import MargotDataFrame, Symbol, Ratio
    from margot.data.column import alphavantage as av
    from margot.data.features import finance

    class Index(Symbol):
        adjusted_close = av.Column(
            function='historical_daily_adjusted',
            time_series='adjusted_close')

    class VXBasis(MargotDataFrame):
        vixm = Index(symbol='VIXM')
        vix3m = Index(symbol='^VXV')
        vx_basis = Ratio(
            numerator=vixm.adjusted_close,
            denominator=vix3m.adjusted_close,
            label='vx_basis_ratio')

    vxbasis = VXBasis()
    vxbasis.to_pandas()

    assert(
        vxbasis.vix3m.to_pandas().tail()[
            '^VXV',
            'adjusted_close'].sum() == Index('^VXV').to_pandas().tail()[
            '^VXV',
            'adjusted_close'].sum())


def test_constructors():
    from margot.data import MargotDataFrame, Symbol, Ratio
    from margot.data.column import alphavantage as av

    class Index(Symbol):
        adjusted_close = av.Column(
            function='historical_daily_adjusted',
            time_series='adjusted_close')

    spy = Index(symbol='SPY')
    vtwo = Index(symbol='VTWO')

    assert(
        spy.to_pandas().tail()[
            'SPY', 'adjusted_close'].sum() != vtwo.to_pandas().tail()[
            'VTWO', 'adjusted_close'].sum()
    )


def test_finance_features():
    from margot.data import MargotDataFrame, Symbol, Ratio
    from margot.data.column import alphavantage as av
    from margot.data.features import finance

    class Index(Symbol):
        adjusted_close = av.Column(
            function='historical_daily_adjusted',
            time_series='adjusted_close')

        simple_returns = finance.SimpleReturns(column='adjusted_close')
        log_returns = finance.LogReturns(column='adjusted_close')
        real_vol = finance.RealisedVolatility(column='log_returns', window=20)
        sma = finance.SimpleMovingAverage(column='adjusted_close', window=10)
        upper = finance.UpperBollingerBand(
            column='adjusted_close', window=20, width=2.0)
        lower = finance.LowerBollingerBand(
            column='adjusted_close', window=20, width=2.0)

    spy = Index(symbol='SPY')

    spy.to_pandas()
