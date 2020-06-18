[![](https://img.shields.io/pypi/v/margot)](https://pypi.org/project/margot/)
![](https://img.shields.io/pypi/pyversions/margot)
![](https://img.shields.io/pypi/wheel/margot)
[![](https://img.shields.io/github/license/pymargot/margot)](https://github.com/pymargot/margot/blob/master/LICENSE)
[![](https://travis-ci.org/pymargot/margot.svg?branch=master)](https://travis-ci.org/github/pymargot/margot)
[![](https://readthedocs.org/projects/margot/badge/?version=latest)](https://margot.readthedocs.io/en/latest/?badge=latest)
[![](https://codecov.io/gh/pymargot/margot/branch/master/graph/badge.svg)](https://codecov.io/gh/pymargot/margot)

# What is margot?
Margot is a library of components that may be used together or separately. The
first major component; *margot.data* is now available for public preview. 
It should be considered an early-beta. It works, but may still have sharp edges.

# What is margot data?
Margot data makes it super easy to create neat and tidy Pandas dataframes for 
time-series analysis.

Margot data aims to manage data collection, caching, cleaning, feature
generation, management and persistence using a clean, declarative API. If you've
ever used Django you'll find this approach similar to the Django ORM.

## Columns
The heart of any time-series dataframe is the original data. Margot can retrieve
time-series data from external sources (currently AlphaVantage). To add a time-
series from an original source, such as "closing_price" or "volume", we declare
a *Column*:

e.g. Let's get closing_price and volume from AlphaVantage:

    adjusted_close = av.Column(time_series='adjusted_close')

    daily_volume = av.Column(time_series='volume')

## Features
Columns are useful, but we usually want to derive new time-series from them,
such as "log_returns" or "SMA20". Margot does this for you; we've called these
derived time-series, *Features*.

    simple_returns = finance.SimpleReturns(column='adjusted_close')
    log_returns = finance.LogReturns(column='adjusted_close')
    sma20 = finance.SimpleMovingAverage(column='adjusted_close', window=20)

Features can be piled on top of one another. For example, to create a
time-series of realised volatility based on log_returns with a lookback of 30
trading days, simply add the following feature:

    realised_vol = finance.RealisedVolatility(column='log_returns', window=30)

Margot includes many common financial Features, and we'll be adding more soon.
It's also very easy to add your own.


## Symbols
Often, you want to make a dataframe combining a number of columns and features.
Margot makes this very easy by providing the Symbol class e.g.

    class MyEquity(Symbol):

        adjusted_close = av.Column(time_series='adjusted_close')
        log_returns = finance.LogReturns(column='adjusted_close')
        realised_vol = finance.RealisedVolatility(column='log_returns', 
                                                  window=30)
        upper_band = finance.UpperBollingerBand(column='adjusted_close', 
                                                window=20, 
                                                width=2.0)
        sma20 = finance.SimpleMovingAverage(column='adjusted_close', 
                                            window=20)
        lower_band = finance.LowerBollingerBand(column='adjusted_close', 
                                                window=20, 
                                                width=2.0)

    spy = MyEquity(symbol='SPY')

## MargotDataFrames
You usually you want to look at more than one symbol. That's where
MargotDataFrames come in. MargotDataFrames combine multiple
Symbols with dataframe-wide Features and Ratios. For example:

    class MyEnsemble(MargotDataFrame):
        spy = MyEquity(symbol='SPY', trading_calendar='NYSE')
        iwm = MyEquity(symbol='IWM', trading_calendar='NYSE')
        spy_iwm_ratio = Ratio(numerator=spy.adjusted_close, 
                              denominator=iwm.adjusted_close,
                              label='spy_iwm_ratio')

    my_df = MyEnsemble().to_pandas() 

The above code creates a Pandas DataFrame of two equities, and an additional
feature that calculates a time-series of the ratio of their respective
adjusted close prices.

## Margot's other parts
**not yet released.**

Margot aims to provide a simple framework for writing and backtesting trading
signal generation algorithms using margot.data.

Results from margot's trading algorithms can be analysed with pyfolio.

# Getting Started

    pip install margot

Next you need to make sure you have a couple of important environment variables
set::

    export ALPHAVANTAGE_API_KEY=YOUR_API_KEY
    export DATA_CACHE=PATH_TO_FOLDER_TO_STORE_HDF5_FILES

Once you've done that, try running the code in the [notebook](notebook.margot.data).

# Status
This is still an early stage software project, and should not be used for live
trading just yet.

# Documentation

For examples see the [notebook](notebook.margot.data).

The main documentation is at [readthedocs](https://margot.readthedocs.io/en/latest/).

# Contributing

Feel free to make a pull request or chat about your idea first using [issues](https://github.com/atkinson/margot/issues).

Dependencies are kept to a minimum. Generally if there's a way to do something
in the standard library (or numpy / Pandas), let's do it that way rather than
add another library. 

# License
Margot is licensed for use under Apache 2.0. For details see [the License](https://github.com/atkinson/margot/blob/master/LICENSE).
