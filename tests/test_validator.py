from decimal import Decimal
from datetime import datetime

import pytest

from trade import Trade
from validator import (
    BrokerTracker,
    TradeValidator,
    InvalidSymbolException,
    InvalidBrokerException,
    MissingDataException,
    DuplicateTradeException,
    ThrottleException,
)


def _trade_factory(**kwargs):
    defaults = dict(
        timestamp=datetime(2017, 2, 1, 8),
        broker="Broker 1",
        sequence_id=123,
        trade_type="1",
        symbol="ABC",
        quantity=100,
        price=Decimal("9.99"),
        side="Buy",
    )
    defaults.update(kwargs)
    return Trade(**defaults)


def test_valid_symbols():
    validator = TradeValidator(symbols=["ABC", "XYZ"], brokers=["Broker 1", "Broker2"])

    with pytest.raises(MissingDataException):
        # No symbol
        trade = _trade_factory(symbol="")
        validator.validate_trade(trade)

    with pytest.raises(InvalidSymbolException):
        # Bad symbol
        trade = _trade_factory(symbol="DEF")
        validator.validate_trade(trade)


def test_valid_broker():
    validator = TradeValidator(symbols=["ABC", "XYZ"], brokers=["Broker 1", "Broker2"])

    with pytest.raises(MissingDataException):
        # No broker
        trade = _trade_factory(broker="")
        validator.validate_trade(trade)

    with pytest.raises(InvalidBrokerException):
        # Not in the list
        trade = _trade_factory(broker="Not in the list")
        validator.validate_trade(trade)


def test_trade_data_required():
    validator = TradeValidator(symbols=["ABC", "XYZ"], brokers=["Broker 1", "Broker2"])

    trade = _trade_factory()
    validator.validate_trade(trade)  # Test no error first

    with pytest.raises(MissingDataException):
        trade = _trade_factory(sequence_id=None)
        validator.validate_trade(trade)

    with pytest.raises(MissingDataException):
        trade = _trade_factory(sequence_id="")
        validator.validate_trade(trade)


def test_broker_tracker_no_dupe_sequence_ids():
    tracker = BrokerTracker("Broker Name")
    trade = _trade_factory(sequence_id=1, timestamp=datetime(2020, 4, 1, 8, 1, 0))
    # Initial trade should be valid
    tracker.validate(trade)
    with pytest.raises(DuplicateTradeException):
        # Same sequence id should throw error
        trade = _trade_factory(sequence_id=1, timestamp=datetime(2020, 4, 1, 8, 1, 1))
        tracker.validate(trade)

    # New sequence id allowed
    trade = _trade_factory(sequence_id=2, timestamp=datetime(2020, 4, 1, 8, 1, 3))
    tracker.validate(trade)


def test_broker_tracker_throttle_limits():
    trade00 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 0), sequence_id=1)
    trade01 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 1), sequence_id=2)
    trade02 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 2), sequence_id=3)
    trade03 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 3), sequence_id=4)
    trade59_9 = _trade_factory(
        timestamp=datetime(2020, 4, 1, 8, 1, 59, 999999), sequence_id=5
    )
    trade60 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 2, 0), sequence_id=5)
    trade120 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 3, 0), sequence_id=8)

    tracker = BrokerTracker("Broker Name")
    # First 3 trades should be fine, 4th should error
    assert tracker.validate(trade00) == "1/3"
    assert tracker.validate(trade01) == "2/3"
    assert tracker.validate(trade02) == "3/3"
    with pytest.raises(ThrottleException):
        tracker.validate(trade03)

    with pytest.raises(ThrottleException):
        # Check microseconds matter
        tracker.validate(trade59_9)

    # Allowed since trade00 should have just dropped off
    assert tracker.validate(trade60) == "3/3"
    # And now all trades shold have dropped off
    assert tracker.validate(trade120) == "1/3"


def test_broker_tracker_throttle_limits_same_timestamp():
    trade00 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 0), sequence_id=0)
    trade01 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 0), sequence_id=1)
    trade02 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 0), sequence_id=2)
    trade03 = _trade_factory(timestamp=datetime(2020, 4, 1, 8, 1, 0), sequence_id=3)
    tracker = BrokerTracker("Broker Name")

    # First 3 trades should be fine, 4th should error
    assert tracker.validate(trade00) == "1/3"
    assert tracker.validate(trade01) == "2/3"
    assert tracker.validate(trade02) == "3/3"
    with pytest.raises(ThrottleException):
        tracker.validate(trade03)
