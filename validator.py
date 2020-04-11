# -*- coding: utf-8 -*-


class MissingDataException(Exception):
    pass


class InvalidSymbolException(Exception):
    pass


class InvalidBrokerException(Exception):
    pass


class TradeValidator:
    def __init__(self, symbols, brokers):
        self.symbols = [s.upper() for s in symbols]
        self.brokers = [b.upper() for b in brokers]

    def validate_trade(self, trade):
        if not trade.is_valid():
            raise MissingDataException()

        if trade.symbol not in self.symbols:
            raise InvalidSymbolException()

        if trade.broker not in self.brokers:
            raise InvalidBrokerException()
