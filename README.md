[![](https://api.codacy.com/project/badge/Grade/1d42c486297a49158494e5f31b25793b)](https://app.codacy.com/manual/pymargot/margot?utm_source=github.com&utm_medium=referral&utm_content=pymargot/margot&utm_campaign=Badge_Grade_Dashboard)
[![](https://img.shields.io/pypi/v/margot)](https://pypi.org/project/margot/)
[![](https://travis-ci.org/pymargot/margot.svg?branch=master)](https://travis-ci.org/github/pymargot/margot)
[![](https://readthedocs.org/projects/margot/badge/?version=latest)](https://margot.readthedocs.io/en/latest/?badge=latest)
[![](https://codecov.io/gh/pymargot/margot/branch/master/graph/badge.svg)](https://codecov.io/gh/pymargot/margot)
[![](https://img.shields.io/github/license/pymargot/margot)](https://github.com/pymargot/margot/blob/master/LICENSE)
![](https://img.shields.io/pypi/pyversions/margot)
![](https://img.shields.io/pypi/wheel/margot)

# What is margot?
Margot makes it super easy to backtest trading elgorithms. Firstly, Margot makes
it super easy tocreate neat and tidy Pandas dataframes for time-series analysis.

Margot manages data collection, caching, cleaning, feature generation,
management and persistence using a clean, declarative API. If you've
ever used Django you will find this approach similar to the Django ORM.

Margot also provides a simple framework for writing and backtesting systematic
trading algorithms.

Results from margot's trading algorithms can be analysed using pyfolio.

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

The documentation is at [readthedocs](https://margot.readthedocs.io/en/latest/).

# Contributing

Feel free to make a pull request or chat about your idea first using [issues](https://github.com/atkinson/margot/issues).

Dependencies are kept to a minimum. Generally if there's a way to do something
in the standard library (or numpy / Pandas), let's do it that way rather than
add another library. 

# License
Margot is licensed for use under Apache 2.0. For details see [the License](https://github.com/atkinson/margot/blob/master/LICENSE).
