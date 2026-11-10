#!/usr/bin/env python3
# Copyright 2026 Northbay Traders
"""This module is responsible for comprehensively handling all invoice related operations."""
import json  # noqa: F401


def total(items):
    """This function calculates the total.

    Args:
        items: list of invoice lines
    """
    # Loop through each item
    return sum(i["price"] * i["qty"] for i in items)  # Note that prices are in paise
