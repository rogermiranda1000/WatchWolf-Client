#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from datetime import datetime
from typing import List

# video save
import imageio
import io
import numpy as np

class ImageList:
	def __init__(self):
		self._list = []
		self._recording_queue = {} # list of indexes where the recording starts; the key is the id
		self._next_id = 0
		self._lock = threading.Lock()
	
	@property
	def recording(self):
		return len(self._recording_queue) > 0

	def append(self, frameStringData: bytes):
		self._lock.acquire()
		if not self.recording:
			self._lock.release()
			return # not recording
		
		self._list.append({
			'timestamp': datetime.now(),
			'data': frameStringData
		})
		self._lock.release()
	
	def start_recording(self) -> int:
		self._lock.acquire()
		id = self._next_id
		self._recording_queue[id] = ( len(self._list)-1 if len(self._list) > 0 else 0 )

		self._next_id += 1
		self._lock.release()
		return id
	
	@staticmethod
	def _get_fps(list: List[dict]) -> int:
		if len(list) < 2: return 1

		duration = (list[-1]['timestamp'] - list[0]['timestamp']).seconds
		if duration < 1: return 1
		return len(list) / duration

	def stop_recording(self, id: int, out: str):
		self._lock.acquire()
		start = self._recording_queue[id]
		data = self._list[start:]
		del self._recording_queue[id]
		if not self.recording: self._list = [] # as we're no longer recording, free the resources
		self._lock.release()

		fps = ImageList._get_fps(data)
		with imageio.get_writer(out, format='mp4', mode='I', fps=fps) as writer:
			for frame in data:
				f = np.fromstring(frame['data'], dtype = np.uint8)
				writer.append_data(imageio.imread(io.BytesIO(f)))