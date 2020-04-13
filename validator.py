# -*- coding: utf-8 -*-
from datetime import timedelta

THROTTLE_LIMIT = 3
LIMIT_SECONDS = 60


class BaseTradeValidationException(Exception):
    pass


class MissingDataException(BaseTradeValidationException):
    pass


class InvalidSymbolException(BaseTradeValidationException):
    pass


class InvalidBrokerException(BaseTradeValidationException):
    pass


class DuplicateTradeException(BaseTradeValidationException):
    pass


class ThrottleException(BaseTradeValidationException):
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
            raise DuplicateTradeException(
                f"{trade.sequence_id} sequency id has already been processed."
            )

        # This logic makes huge assumption that trades will always come in
        # in sequential timestamp order.  I would assume that is safe for this
        # excercise since I can control it and in a real program the timestamps would
        # be generated based on the clock.
        # One edge case not handled here is two orders coming in at exactly the same time
        # which in the world of HFT is very possible. Ignoring for now since that's not
        # in the requirements but wanted to call it out.
        throttle_count = 1
        cutoff = trade.timestamp - timedelta(seconds=LIMIT_SECONDS)
        for previous_trade in self.trades:
            # TODO: Check if trade is allowed if exactly 60 seconds
            # and write test accordingly
            if previous_trade.timestamp <= cutoff:
                break
            throttle_count += 1

        if throttle_count > THROTTLE_LIMIT:
            raise ThrottleException("Exceded throttle limit")

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
        is_valid, field = trade.is_valid()
        if not is_valid:
            raise MissingDataException(f"Trade missing value for field: {field}")

        if trade.symbol not in self.symbols:
            raise InvalidSymbolException(f"{trade.symbol} is not a valid symbol")

        broker_key = trade.broker.upper()
        if broker_key not in self.brokers:
            raise InvalidBrokerException(f"{trade.broker} is not a known broker")

        self.brokers[broker_key].validate(trade)
