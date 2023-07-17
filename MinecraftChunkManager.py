#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock
from typing import Tuple

class MinecraftChunkManager:
	def __init__(self):
		self._loaded_chunks = []
		self._to_remove = [] # somehow unloaded before loading?
		self._loaded_chunks_world = None
		self._lock = Lock()
    
	def chunk_loaded(self, world: str, x: int, y: int):
		self._lock.acquire()
		if world != self._loaded_chunks_world:
			# clear all chunks
			self._loaded_chunks = []
			self._to_remove = []

			# we're on a different world now
			self._loaded_chunks_world = world

		if (x, y) in self._to_remove:
			self._to_remove.remove((x, y)) # we've just removed (not-added) that chunk
		else:
			self._loaded_chunks.append((x, y))
		self._lock.release()
	
	def chunk_unloaded(self, world: str, x: int, y: int):
		self._lock.acquire()
		if world == self._loaded_chunks_world: # if it's different we already removed those chunks
			try:
				self._loaded_chunks.remove((x, y))
			except ValueError:
				self._to_remove.append((x, y))
		self._lock.release()
	
	def is_chunk_loaded(self, world: str, x: int, y: int) -> bool:
		if world != self._loaded_chunks_world:
			return False
		
		self._lock.acquire()
		intersect = (x, y) in self._loaded_chunks
		self._lock.release()

		return intersect

	@staticmethod
	def location_to_chunk(x: float|int, y: float|int) -> Tuple[int,int]:
		return (int(x)>>4, int(y)>>4)