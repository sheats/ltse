# -*- coding: utf-8 -*-
from datetime import timedelta

THROTTLE_LIMIT = 3
LIMIT_SECONDS = 60


class MissingDataException(Exception):
    pass


class InvalidSymbolException(Exception):
    pass


class InvalidBrokerException(Exception):
    pass


class DuplicateTradeException(Exception):
    pass


class ThrottleException(Exception):
    pass


class BrokerTracker:
    def __init__(self, name):
        self.name = name
        self.trades = []
        self.sequence_ids = []

    def validate(self, trade):
        """Validates rules:
            1: No duplicate sequence IDs
            2: Only 3 trades for every 60 seconds are allowed.

        Returns number of trades that have been used of the allowed limits
        in format of '1/3' for 1 trade registered, 3 total allowed.
        """
        if trade.sequence_id in self.sequence_ids:
            raise DuplicateTradeException()

        # This logic makes huge assumption that trades will always come in
        # in sequential timestamp order.  I would assume that is safe for this
        # excercise and the real timestamps would probably be generated dynamically.
        # One edge case not handled here is two orders coming in at exactly the same time
        # which in the world of HFT is very possible.
        throttle_count = 1
        cutoff = trade.timestamp - timedelta(seconds=LIMIT_SECONDS)
        for previous_trade in self.trades:
            if previous_trade.timestamp == trade.timestamp:
                raise Exception("Cannot handle identical timestamps")
            if previous_trade.timestamp <= cutoff:
                break
            throttle_count += 1

        if throttle_count > THROTTLE_LIMIT:
            raise ThrottleException()

        self.sequence_ids.append(trade.sequence_id)
        self.trades.insert(0, trade)
        return f"{throttle_count}/{THROTTLE_LIMIT}"


class TradeValidator:
    def __init__(self, symbols, brokers):
        self.symbols = [s.upper() for s in symbols]
        self.brokers = {}
        for name in brokers:
            self.brokers[name.upper()] = BrokerTracker(name)

    def validate_trade(self, trade):
        if not trade.is_valid():
            raise MissingDataException()

        if trade.symbol not in self.symbols:
            raise InvalidSymbolException()

        if trade.broker not in self.brokers:
            raise InvalidBrokerException()

        self.brokers[trade.broker].validate(trade)
