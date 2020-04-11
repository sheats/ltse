from decimal import Decimal
from datetime import datetime

import pytest

from trade import Trade
from validator import (
    TradeValidator,
    InvalidSymbolException,
    InvalidBrokerException,
    MissingDataException,
)


@pytest.fixture
def valid_trade():
    """For convenience return a validator and trade that raises no errors"""
    validator = TradeValidator(symbols=["ABC", "XYZ"], brokers=["Broker 1", "Broker2"])

    trade = Trade(
        timestamp=datetime(2017, 2, 1, 8),
        broker="Broker 1",
        sequence_id=123,
        trade_type=1,
        symbol="ABC",
        quantity=100,
        price=Decimal("9.99"),
        side="Buy",
    )
    return validator, trade


def test_valid_symbols(valid_trade):
    validator, trade = valid_trade

    with pytest.raises(InvalidSymbolException):
        # Bad symbol
        trade.symbol = "DEF"
        validator.validate_trade(trade)

    with pytest.raises(MissingDataException):
        # No symbol
        trade.symbol = None
        validator.validate_trade(trade)

    with pytest.raises(InvalidSymbolException):
        # Bad data
        trade.symbol = 1
        validator.validate_trade(trade)


def test_valid_broker(valid_trade):
    validator, trade = valid_trade

    with pytest.raises(MissingDataException):
        # No broker
        trade.broker = None
        validator.validate_trade(trade)

    with pytest.raises(MissingDataException):
        # Empty
        trade.broker = ""
        validator.validate_trade(trade)

    with pytest.raises(InvalidBrokerException):
        # Not in the list
        trade.broker = "Not in the list"
        validator.validate_trade(trade)


def test_trade_data_required(valid_trade):
    validator, trade = valid_trade

    trade.sequence_id = None
    with pytest.raises(MissingDataException):
        validator.validate_trade(trade)

    trade.sequence_id = ""
    with pytest.raises(MissingDataException):
        validator.validate_trade(trade)
