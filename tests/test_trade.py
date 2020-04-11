from decimal import Decimal
from datetime import datetime
from trade import Trade


def test_is_valid():
    assert not Trade(
        timestamp=datetime(2017, 2, 1, 8),
        broker="Broker 1",
        sequence_id=123,
        trade_type=1,
        symbol="ABC",
        quantity=100,
        price=None,
        side="Buy",
    ).is_valid()

    assert not Trade(
        timestamp=datetime(2017, 2, 1, 8),
        broker="Broker 1",
        sequence_id=123,
        trade_type=1,
        symbol="ABC",
        quantity=None,
        price=Decimal("9"),
        side="Buy",
    ).is_valid()
