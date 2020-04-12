# -*- coding: utf-8 -*-
from datetime import datetime


class Trade:
    """Simple data class to represent what we know about a trade.
    All trades need to be instantiated through this class since
    we strip and uppercase any strings for consistency.

    All arguments are required and expected to be of the correct data format.

    """

    def __init__(
        self, timestamp, broker, sequence_id, trade_type, symbol, quantity, price, side
    ):
        self.timestamp = timestamp
        self.broker = broker.strip().upper()
        self.sequence_id = sequence_id
        self.trade_type = trade_type
        self.symbol = symbol.strip().upper()
        self.quantity = quantity
        self.price = price
        self.side = side.strip().upper()

    def is_valid(self):
        """All fields are required"""
        for val in self.__dict__.values():
            if not val:
                return False
        return True
