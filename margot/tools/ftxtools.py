import logging
import ftx

class FTXObject():

    def __init__(self, token):
        for key in token:
            setattr(self, key, token[key])


class LeveragedToken(FTXObject):
    
    def calc_pending_rebalance(self):
        """
        Calculate pending rebalance.
        """
        desired_position = float(self.leverage) * \
        self.totalNav / self.underlyingMark

        current_position = self.positionPerShare * \
        self.outstanding

        return desired_position - current_position


class Future(FTXObject):

    def __init__(self, *args, **kwargs):
        self._lt_list = None
        super(Future, self).__init__(*args, **kwargs)

    @property
    def hourly_volume(self):
        return self.volume / 24

    @property
    def hourly_volume_usd(self):
        return self.volumeUsd24h / 24

    @property
    def lt_list(self):
        return self._lt_list

    def set_lt_list(self, lt_list):
        self._lt_list = lt_list

    @property
    def market_impact(self):
        """
        Basic metric for market impact.
        """
        return self.rebal_size / self.hourly_volume

    @property
    def pending_rebal_usd(self):
        return self.rebal_size * self.mark

    @property
    def rebal_size(self):
        pending_rebalance = 0.0
        for lt in self.lt_list:
            pending_rebalance += lt.calc_pending_rebalance()
        return pending_rebalance



class FTXStrategy():

    BUY = LONG = 'buy'
    SELL = SHORT = 'sell'

    perps = list()
    futures = list()
    leveraged_tokens = list()

    def __init__(self, api_key, api_secret, subaccount, debug) -> None:

        self.client = ftx.FtxClient(
            api_key=api_key, 
            api_secret=api_secret, 
            subaccount_name=subaccount)

        for token in self.client.list_lts():
            lt = LeveragedToken(token)
            self.leveraged_tokens.append(lt)

        for future in self.client.get_futures():
            lt_list = [
                lt for lt in self.leveraged_tokens
                    if lt.underlying == future['name']
                ]

            f = Future(future)
            f.set_lt_list(lt_list)
            self.futures.append(f)

        self.perps = [future for future in self.futures if future.perpetual]

        self.debug=debug

    def place_order(self, market, side, size_usd):
        latest = self.client.get_future(market)

        if side == self.BUY:
            limit = latest['ask'] * 1.0005
        else:
            limit = latest['bid'] * 0.9995

        size = size_usd / limit

        logging.info('debug={}, '\
            'market="{}", ' \
            'side="{}", ' \
            'price={:,.4f}, ' \
            'size={:,.4f}'.format(self.debug,
                                    market, 
                                    side, 
                                    limit, 
                                    size))

        if not self.debug:
            try:
                self.client.place_order(
                    market=market,
                    side=side, 
                    price=limit,
                    size=size,
                    type='limit')
            except Exception as e:
                print(e)


    def close_position(self, position):
        latest = self.client.get_future(position['future'])

        if position['side'] == self.SHORT:
            desired_side = self.BUY
        else:
            desired_side = self.SELL

        if desired_side == self.BUY:
            limit = latest['ask'] * 1.0010
        else:
            limit = latest['bid'] * 0.9990

        logging.info('debug={}, '\
                'market="{}", ' \
                'side="{}", ' \
                'price={:,.4f}, ' \
                'size={:,.4f}'.format(
                    self.debug,
                    position['future'], 
                    desired_side, 
                    limit, 
                    position['size']))

        if not self.debug:
            try:
                self.client.place_order(
                    market=position['future'],
                    side=desired_side, 
                    price=limit,
                    size=position['size'],
                    type='limit',
                    reduce_only=True)
            except Exception as e:
                print(e)


    def close_all_positions(self):
        """
        While closing the position, I want to be more agressive
        to get out before the reversion kicks in.
        """
        for position in self.client.get_positions():
            if position['size'] != 0.0:
                self.close_position(position)
    
        print('Closed all positions.')