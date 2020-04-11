#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def load_symbols():
    symbols = []
    with open("data/symbols.txt", "r") as the_file:
        for line in the_file:
            symbols.append(line.strip())
    return symbols


def load_brokers():
    brokers = []
    with open("data/firms.txt", "r") as the_file:
        for line in the_file:
            brokers.append(line.strip())
    return brokers


def load_orders():
    pass


def main():
    valid_symbols = load_symbols()
    permitted_brokers = load_brokers()
    from pprint import pprint

    pprint(valid_symbols)
    pprint(permitted_brokers)


if __name__ == "__main__":
    main()
