# To do list

* refactor data to be like Django ORM - DONE
* colums should be called features - DONE
* tidy up hdf5 files - DONE

* pairs trading
* decouple positions + returns from rebalancing
* add 3DMA filter back to the vix basis
* risk management
* live trading
* accounting
* put a front end on it
* switch to bigquery?


# concept

class Equity(Symbol):

    trading_calendar = tc.get_calendar('NYSE')

    adjusted_close = fields.AlphaVantage(function='historical_daily_adjusted', field='adjusted_close')
    market_cap = field.MorningStar(function='historical_fundamental', field='market_cap')

    std20 = column.RollingStandardDeviation(field='log_returns', lookback=20)
    upper = column.UpperBollingerBand(field='adjusted_close', std=2)
    lower = columnn.LowerBollingerBand(field ='adjusted_close', std =2)


 class VXDataset(DataSet):

    vixm = Equity(symbol='VIXM')
    ixv = Equity(symbol='IXV')
    vix3m = Index(symbol='^VXV')
    vix = Index(symbol='^VIX')
