#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from .validator import TradeValidator


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
    trades = []
    with open("data/trades.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            trades.append(row)
    return trades


def main():
    valid_symbols = load_symbols()
    permitted_brokers = load_brokers()
    trades = load_trades()
    validator = TradeValidator(valid_symbols, permitted_brokers)
    for trade in trades:
        validator.validate_trade(trade)
    from pprint import pprint

    pprint(valid_symbols)
    pprint(permitted_brokers)
    pprint(trades)


if __name__ == "__main__":
    main()
