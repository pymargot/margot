====================
Margot Documentation
====================

.. image:: https://api.codacy.com/project/badge/Grade/1d42c486297a49158494e5f31b25793b
   :target: https://app.codacy.com/manual/pymargot/margot?utm_source=github.com&utm_medium=referral&utm_content=pymargot/margot&utm_campaign=Badge_Grade_Dashboard

.. image:: https://img.shields.io/github/license/pymargot/margot
   :target: https://github.com/pymargot/margot/blob/master/LICENSE

.. image:: https://travis-ci.org/pymargot/margot.svg
   :target: https://travis-ci.org/github/pymargot/margot

.. image:: https://readthedocs.org/projects/margot/badge/?version=latest
   :target: https://margot.readthedocs.io/en/latest/?badge=latest

.. image:: https://codecov.io/gh/pymargot/margot/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pymargot/margot

.. image:: https://img.shields.io/pypi/wheel/margot

.. image:: https://img.shields.io/pypi/pyversions/margot

.. image:: https://img.shields.io/pypi/v/margot
   :target: https://pypi.org/project/margot/


Margot makes it super easy to backtest trading elgorithms. Firstly, Margot makes
it super easy tocreate neat and tidy Pandas dataframes for time-series analysis.

Margot manages data collection, caching, cleaning, feature generation,
management and persistence using a clean, declarative API. If you've
ever used Django you will find this approach similar to the Django ORM.

Margot also provides a simple framework for writing and backtesting systematic
trading algorithms.

Results from margot's trading algorithms can be analysed using pyfolio.

To get started::

    pip install margot

Next you need to make sure you have a couple of important environment variables
set::

    export ALPHAVANTAGE_API_KEY=YOUR_API_KEY
    export DATA_CACHE=PATH_TO_FOLDER_TO_STORE_HDF5_FILES

Once you've done that, try running the code in the notebook.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   about
   getting_started
   notebook.margot.data
   margot
