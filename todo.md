# To do list

* refactor data to be like Django ORM - DONE
* colums should be called features - DONE
* tidy up hdf5 files - DONE

* datasets, double layer indexed symbols
* pairs trading
* decouple positions + returns from rebalancing
* add 3DMA filter back to the vix basis
* risk management
* live trading
* accounting
* put a front end on it
* switch to bigquery?
* rename fields to something else (not series) - maybe column?

# concept

class Equity(Symbol):

    trading_calendar = tc.get_calendar('NYSE')

    adjusted_close = column.AlphaVantage(function='historical_daily_adjusted', field='adjusted_close')
    market_cap = column.MorningStar(function='historical_fundamental', field='market_cap')

    std20 = feature.RollingStandardDeviation(field='log_returns', lookback=20)
    upper = feature.UpperBollingerBand(field='adjusted_close', std=2)
    lower = feature.LowerBollingerBand(field ='adjusted_close', std =2)


 class VXDataset(Ensemble):

    vixm = Equity(symbol='VIXM')
    ixv = Equity(symbol='IXV')
    vix3m = Index(symbol='^VXV')
    vix = Index(symbol='^VIX')
