#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from itertools import count
import os, json

ITEMS_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "items.json")

_items = []
with open(ITEMS_FILE_PATH) as f:
    items = json.load(f)
    for item in items:
        _items.append(item["name"].upper())

ItemType = Enum('ItemType', zip(_items,         \
                                count())) # start at 0