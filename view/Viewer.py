#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple

class Viewer:
	def __init__(self, size: Tuple[int,int] = (512, 512), printer = lambda msg: print(msg)):
		self._size = size
		self._printer = printer

	def setup(self, bot):
		pass
	
	def close(self):
		pass
	
	def start_recording(self) -> int:
		pass
	
	def stop_recording(self, id: int, out: str):
		pass
