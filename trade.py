# -*- coding: utf-8 -*-


class Trade:
    """Simple data class to represent what we know about a trade.

    Data is not guaranteed to be cleaned yet
    """

    _attributes = [
        "timestamp",
        "broker",
        "sequency_id",
        "type",
        "symbol",
        "quantity",
        "price",
        "side",
    ]

    def __init__(self, **kwargs):
        for attr in self._attributes:
            setattr(self, attr, kwargs.get(attr, None))
