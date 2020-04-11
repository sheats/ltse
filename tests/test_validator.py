import pytest

from trade import Trade
from validator import TradeValidator, InvalidSymbolException, InvalidBrokerException


@pytest.fixture
def valid_trade():
    """For convenience return a validator and trade that raises no errors"""
    validator = TradeValidator(symbols=["ABC", "XYZ"], brokers=["Broker 1", "Broker2"])

    trade = Trade(symbol="ABC", broker="Broker 1")
    return validator, trade


def test_valid_symbols(valid_trade):
    validator, trade = valid_trade
    validator.validate_trade(trade)
    trade.symbol = "AbC"
    validator.validate_trade(trade)

    with pytest.raises(InvalidSymbolException):
        # Bad symbol
        trade.symbol = "DEF"
        validator.validate_trade(trade)

    with pytest.raises(InvalidSymbolException):
        # No symbol
        trade.symbol = None
        validator.validate_trade(trade)

    with pytest.raises(InvalidSymbolException):
        # Bad data
        trade.symbol = 1
        validator.validate_trade(trade)


def test_valid_broker(valid_trade):
    validator, trade = valid_trade
    validator.validate_trade(trade)
    trade.broker = "BROker2"
    validator.validate_trade(trade)

    with pytest.raises(InvalidBrokerException):
        # No broker
        trade.broker = None
        validator.validate_trade(trade)

    with pytest.raises(InvalidBrokerException):
        # Empty
        trade.broker = ""
        validator.validate_trade(trade)

    with pytest.raises(InvalidBrokerException):
        # Not in the list
        trade.broker = "Not in the list"
        validator.validate_trade(trade)
