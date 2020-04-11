import pytest

from trade import Trade
from validator import TradeValidator, InvalidSymbolException


def test_valid_symbols():
    validator = TradeValidator(symbols=["ABC"], brokers=[])
    validator.validate_trade(Trade(symbol="ABC"))  # no error
    with pytest.raises(InvalidSymbolException):
        # Bad symbol
        validator.validate_trade(Trade(symbol="DEF"))

    with pytest.raises(InvalidSymbolException):
        # No symbol
        validator.validate_trade(Trade(symbol=None))

    with pytest.raises(InvalidSymbolException):
        #
        validator.validate_trade(Trade(symbol=1))
