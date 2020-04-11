# -*- coding: utf-8 -*-


class InvalidSymbolException(Exception):
    pass


class TradeValidator:
    def __init__(self, symbols, brokers):
        self.symbols = symbols
        self.brokers = brokers

    def validate_trade(self, trade):
        if trade.symbol is None or trade.symbol.strip() not in self.symbols:
            raise InvalidSymbolException()
