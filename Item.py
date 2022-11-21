#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any
from ItemType import ItemType

class Item:
	def __init__(self, type: ItemType, amount: int):
		self._type = type
		self._amount = amount

	def set_amount(self, amount: int):
		self._amount = amount
	
	@property
	def type(self) -> ItemType:
		return self._type
	
	@property
	def amount(self) -> int:
		return self._amount

	def __eq__(self, obj: Any) -> bool:
		if type(self) != type(obj):
			return false
		return self._type == obj._type and self._amount == obj._amount

	def __str__(self):
		return str(self._type) + "{" + str(self._amount) + "}"