#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

class Position:
	def __init__(self, world: str, x: float, y: float, z: float):
		self._world = world
		self._x = x
		self._y = y
		self._z = z
	
	@property
	def world(self):
		return self._world
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@property
	def z(self):
		return self._z

	def __eq__(self, obj: Any) -> bool:
		if type(self) != type(obj):
			return false
		return self._world == obj._world and self._x == obj._x and self._y == obj._y and self._z == obj._z
	
	def __str__(self):
		return self._world + "{" + f"{x},{y},{z}" + "}"
