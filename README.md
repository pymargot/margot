# What is margot?

## margot wants you to be a better quant.

margot is a "batteries included" library for systematic trading with an emphasis on ease of use.

## margot wants to help you:

**- Wrangle data** - use a simple Django ORM inspired API to blend data from a variety of sources into a consolidated time-series dataframe.

**- Reuse features** - a library of reusable features to apply to your data.

**- Make custom features** - easily create features out of your preferred indicators or ratios, and incorporate them in to your algorithms in a repeatable way. 

**- Write algorithms that trade** - TODO express your idea using simple logic, without getting bogged down by the nuances of Pandas or stochastic algebra.

**- Walk-forward backtest your algos** - TODO Backtest your algorithm, generating a historical returns time-series that can be analysed using pyfolio.

**- Manage risk** - TODO Learn the expected volatility of a strategy so that you can size it into your portfolio.

**- Allocate accordingly** - TODO allocate funds to a strategy based on realised volatility.

**- Trade** - TODO execute your trades with your brokers API.

**- Bookkeep** - TODO track fees and P&L, per strategy.

## Status
This is still an early stage software project, and should not be used for live trading.

## Getting Started

pip install margot

## Documentation

in progress - for examples see the notebooks folder.

## Contributing
Feel free to make a pull request; but please feel even free-er to chat about your idea first via issues.

The general idea is to **keep things simple**. This is intended to be long-running operational software; it must be easy to maintain, and easy to understand.

Dependencies are kept to a minimum. Generally if there's a way to do something in the standard library (or numpy / Pandas), let's do it that way rather than seeking the convenience of another library. 

## Resources 

If you come across this, I suggest you checkout http://robotwealth.com. Kris and James taught me everything I know about trading. They're like 5th Dan blackbelts at quantitative finance. You should try one of their bootcamps.

## License
This version of this software may only be used under the terms set out in [the License](License.txt).
