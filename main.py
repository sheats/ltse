# -*- coding: utf-8 -*-
import json
import csv
from json import JSONEncoder
from decimal import Decimal
from datetime import datetime

from trade import Trade
from validator import (
    TradeValidator,
    BaseTradeValidationException,
    MissingDataException,
    InvalidSymbolException,
    InvalidBrokerException,
    DuplicateTradeException,
    ThrottleException,
)


class TradeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Trade):
            return o.__dict__
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o.quantize(Decimal("0.01")))


def _load_text_file(path):
    items = []
    with open(path, "r") as the_file:
        for line in the_file:
            items.append(line.strip())
    return items


def load_symbols():
    return _load_text_file("data/symbols.txt")


def load_brokers():
    return _load_text_file("data/firms.txt")


def load_trades():
    # Time stamp,broker,sequence id,type,Symbol,Quantity,Price,Side
    trades = []
    with open("data/trades.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Goofy datetime format, python doesn't seem to have a format code for
            # not zero padded days.
            # Also, Assuming it's oct 5 vs may 10 but no way to know
            ts = row["Time stamp"].replace("/5/", "/05/")
            timestamp = datetime.strptime(ts, "%m/%d/%Y %H:%M:%S")

            trades.append(
                Trade(
                    timestamp=timestamp,
                    broker=row["broker"],
                    sequence_id=int(row["sequence id"]),
                    trade_type=row["type"],
                    symbol=row["Symbol"],
                    quantity=int(row["Quantity"]),
                    price=Decimal(row["Price"]),
                    side=row["Side"],
                )
            )
    trades.sort(key=lambda t: (t.timestamp, t.sequence_id))
    return trades


def main():
    valid_symbols = load_symbols()
    permitted_brokers = load_brokers()
    validator = TradeValidator(valid_symbols, permitted_brokers)
    valid = []
    invalid = []
    for trade in load_trades():
        try:
            validator.validate_trade(trade)
        except BaseTradeValidationException as exc:
            trade.reason = str(exc)  # will put reason in invalid.json below
            invalid.append(trade)
        else:
            valid.append(trade)

    with open("invalid.txt", "w") as invalid_file:
        for trade in invalid:
            invalid_file.write(f"{trade.broker} {trade.sequence_id}\n")

    with open("valid.txt", "w") as invalid_file:
        for trade in valid:
            invalid_file.write(f"{trade.broker} {trade.sequence_id}\n")

    # Extra Credit
    with open("invalid.json", "w") as invalid_json_file:
        invalid_json_file.write(json.dumps(invalid, indent=4, cls=TradeEncoder))

    with open("valid.json", "w") as valid_json_file:
        valid_json_file.write(json.dumps(valid, indent=4, cls=TradeEncoder))


if __name__ == "__main__":
    main()
