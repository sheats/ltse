# -*- coding: utf-8 -*-


class InvalidSymbolException(Exception):
    pass


class InvalidBrokerException(Exception):
    pass


class TradeValidator:
    def __init__(self, symbols, brokers):
        self.symbols = [s.upper() for s in symbols]
        self.brokers = [b.upper() for b in brokers]

    def validate_trade(self, trade):

        if not trade.symbol or str(trade.symbol).strip().upper() not in self.symbols:
            raise InvalidSymbolException()

        if not trade.broker or str(trade.broker).strip().upper() not in self.brokers:
            raise InvalidBrokerException
