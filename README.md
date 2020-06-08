# margot is a framework for quanting with pydata.
Margot is a library with two distinct components; these can be used together, or independently:
- margot.data
- margot.backtest

# Margot Data
The first component is margot.data.

Margot manages data collection, cleaning and assemblance into a well organised Pandas 
Dataframe using a clean, declarative API. If you've ever used Django you'll find this
approach familiar.

## Columns
Margot can retreive time series data from external sources, like AlphaVantage. To add 
a time series such as "closing_price" or "volume", we declare a Column.

e.g. to get closing_price from AlphaVantage:

    adj_close = av.Column(function='historical_daily_adjusted', column='adjusted_close')

## Features
Columns are useful, but we usually want to derived another time series from them, such
 as "returns" or "SMA20". Margot does this for you; we call them Features.

e.g.

    simple_returns = feature.SimpleReturns(column='adjusted_close')
    log_returns = feature.LogReturns(column='adjusted_close')
    sma20 = feature.SimpleMovingAverage(column='adjusted_close', window=20)

Margot Data includes many common financial Features, and it's very easy to add more.

## Symbols
Often, you want to make a dataframe combining a number of these columns and features.
Margot makes this very easy. e.g.

    class MyEquity(Symbol):

        adjusted_close = av.Column(function='historical_daily_adjusted', column='adjusted_close')
        log_returns = feature.LogReturns(column='adjusted_close')
        realised_vol = feature.RealisedVolatility(column='log_returns', window=30)
        upper_band = feature.UpperBollingerBand(column='adjusted_close', window=20, width=2.0)
        sma20 = feature.SimpleMovingAverage(column='adjusted_close', window=20)
        lower_band = feature.LowerBollingerBand(column='adjusted_close', window=20, width=2.0)

    spy = MyEquity(symbol='SPY)

## Ensembles
Usually you want to look at more than one symbol in a systematic trade. That's where ensembles
come in and really demonstrate the value of margot.data.

    class MyEnsemble(Ensemble):
        spy = Equity(symbol='SPY')
        iwm = Equity(symbol='IWM')
        spy_iwm_ratio = Ratio(numerator=spy.adjusted_close, 
                              denominator=iwm.adjusted_close,
                              label='spy_iwm_ratio')

    my_df = MyEnsemble().to_pandas() 

# Margot backtest
margot.backtest isn't yet included in these releases.

Margot backtest provides a base class to inherit where you define your trading algorithm, and an
implementation of a walk-forward backetesting algorithm that produced backtests of your algorithm 
using margot.data. 

Results from margot backtest can be analysed with pyfolio.

## Status
This is still an early stage software project, and should not be used for live trading.

## Getting Started

    pip install margot

## Documentation

in progress - for examples see the [notebook](https://github.com/atkinson/margot/blob/master/notebooks/margot.ipynb).

## Contributing

Feel free to make a pull request or chat about your idea first using [issues](https://github.com/atkinson/margot/issues).

Dependencies are kept to a minimum. Generally if there's a way to do something in the standard library (or numpy / Pandas), let's do it that way rather than add another library. 

## License
Margot is lecensed for use under Apache 2.0. For details see [the License](License.txt).
