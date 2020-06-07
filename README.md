# margot is a framework for quanting with pydata.

Margot currently includes three components; these can be used together, or independently:

- margot.data
- margot.backtest
- margot.live

# Margot Data

The first component is margot.data.

Margot Data manages data collection, cleaning and assemblance into a well organised 
Pandas Dataframe using a clean, declarative API inspired by Django ORM.

## Columns

Data retreived from external sources, such as "closing_price" or "volume", we call Columns.

e.g. to get closing_price from AlphaVantage:

    adj_close = av.Column(function='historical_daily_adjusted', column='adjusted_close')

## Features

Columns can be augmented by derived time-series, such as "returns" or "SMA20", which we call, Features.

e.g.

    simple_returns = feature.SimpleReturns(column='adjusted_close')
    log_returns = feature.LogReturns(column='adjusted_close')
    sma20 = feature.SimpleMovingAverage(column='adjusted_close', window=20)

Margot Data includes many common financial Features, and it's very easy to add more.

## Symbols

Often, you want to make a dataframe combining a number of these columns and features. Margot Data
makes this very easy. e.g.

    class MyEquity(Symbol):

        adjusted_close = av.Column(function='historical_daily_adjusted', column='adjusted_close')
        log_returns = feature.LogReturns(column='adjusted_close')
        realised_vol = feature.RealisedVolatility(column='log_returns', window=30)
        upper_band = feature.UpperBollingerBand(column='adjusted_close', window=20, width=2.0)
        sma20 = feature.SimpleMovingAverage(column='adjusted_close', window=20)
        lower_band = feature.LowerBollingerBand(column='adjusted_close', window=20, width=2.0)

    spy = MyEquity(symbol='SPY)

## Ensembles

    class MyEnsemble(Ensemble):
        spy = Equity(symbol='SPY')
        iwm = Equity(symbol='IWM')
        spy_iwm_ratio = Ratio(numerator=spy.adjusted_close, denominator=iwm.adjusted_close, label='spy_iwm_ratio')

    my_df = MyEnsemble().to_pandas() 

# Margot backtest

The second major component, margot.backtest isn't yet included in these releases.

Margot backtest provides a base class to inherit where you define your trading algorithm, and an
implementation of a walk-forward backetesting algorithm that produced backtests of your algorithm 
using margot.data. Results of the backtest can be analysed with pyfolio.

# Margot live

Margot live allows you to trade live using the exact same algorithm you backtested using margot.backtest.


## Status
This is still an early stage software project, and should not be used for live trading.

## Getting Started

pip install margot

## Documentation

in progress - for examples see the [notebooks](https://github.com/atkinson/margot/blob/master/notebooks/margot.ipynb).

## Contributing

Feel free to make a pull request; but please feel even free-er to chat about your idea first via issues.

The general idea is to **keep things simple**. This is intended to be long-running operational software; it must be easy to maintain, and easy to understand.

Dependencies are kept to a minimum. Generally if there's a way to do something in the standard library (or numpy / Pandas), let's do it that way rather than seeking the convenience of another library. 

## Resources 

If you come across this, I suggest you checkout http://robotwealth.com. Kris and James taught me everything I know about trading. They're like 5th Dan blackbelts at quantitative finance. You should try one of their bootcamps.

## License
This version of this software may only be used under the terms set out in [the License](License.txt).
