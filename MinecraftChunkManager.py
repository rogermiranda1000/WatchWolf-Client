#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock
from rtree import index
from typing import Tuple

class MinecraftChunkManager:
	def __init__(self):
		self._loaded_chunks = index.Index()
		self._loaded_chunks_world = None
		self._lock = Lock()
    
	def chunk_loaded(self, world: str, x: int, y: int):
		self._lock.acquire()
		if world != self._loaded_chunks_world:
			self._loaded_chunks = index.Index() # clear all chunks
			self._loaded_chunks_world = world
		self._loaded_chunks.insert(True, (x, y, x, y))
		self._lock.release()
	
	def chunk_unloaded(self, world: str, x: int, y: int):
		self._lock.acquire()
		if world == self._loaded_chunks_world: # if it's different we already removed those chunks
			self._loaded_chunks.delete(True, (x, y, x, y))
		self._lock.release()
	
	def is_chunk_loaded(self, world: str, x: int, y: int) -> bool:
		if world != self._loaded_chunks_world:
			return False
		
		self._lock.acquire()
		intersect = list(self._loaded_chunks.intersection((x, y, x, y)))
		self._lock.release()

		return len(intersect) > 0

	@staticmethod
	def location_to_chunk(x: float|int, y: float|int) -> Tuple[int,int]:
		x = int(x)
		y = int(y)
		return (x>>4, y>>4)