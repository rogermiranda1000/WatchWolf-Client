#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition
from MinecraftClient import MinecraftClient
from ClientConnector import ClientConnector
from OnClientConnected import OnClientConnected
from OnClientDisconnected import OnClientDisconnected

import socket
from threading import Thread

import threading
import time

from javascript import require, On, Once, console
mineflayer = require("mineflayer", "latest")

# time to force the login
login_timeout_sec = 3

class MineflayerClient(MinecraftClient):
	def __init__(self, host: str, port: int, username: str, assigned_port: int, on_client_connected: OnClientConnected, on_client_disconnected: OnClientDisconnected):
		super().__init__(host, port, username)
		self._connector = ClientConnector(self, assigned_port)
		self._client_connected_listener = on_client_connected
		self._client_disconnected_listener = on_client_disconnected
		
		self._thread_lock = threading.Lock()
		self._timedout = None
		Thread(target = self._login_timeout).start()
		
		self._bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username
		})
		
		@On(self._bot, "login")
		def login(this):
			this._thread_lock.acquire()
			if this._timedout != None:
				# too late
				this._thread_lock.release()
				return
			this._timedout = False
			this._thread_lock.release()
			
			print(this._username + " connected to the server (" + this.server + ")")
			
			if this._client_connected_listener != None:
				this._client_connected_listener.client_connected(this)
	
	def _login_timeout(self):
		if self._client_connected_listener != None:
			time.sleep(login_timeout_sec)
			
			self._thread_lock.acquire()
			timedout = (self._timedout == None)
			if timedout:
				self._timedout = True
				self._client_connected_listener.client_connected(self)
			self._thread_lock.release()
			
			if timedout:
				print(self._username + ", at " + self.server + " timedout")
	
	@property
	def timedout(self) -> bool:
		return self._timedout
