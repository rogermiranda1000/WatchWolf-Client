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
		printer = lambda msg : print(f"[{username} - {host}:{str(port)}] {msg}")
		self._connector = ClientConnector(self, assigned_port, printer)
		self._client_connected_listener = on_client_connected
		self._client_disconnected_listener = on_client_disconnected
		
		self._thread_lock = threading.Lock()
		self._timedout = None
		Thread(target = self._login_timeout).start()
		
		self._bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username,
			"verbose": True
		})
		
		@On(self._bot, "login")
		def login(_):
			self._thread_lock.acquire()
			if self._timedout != None:
				# too late
				this._thread_lock.release()
				return
			self._timedout = False
			self._thread_lock.release()
			
			print(self._username + " connected to the server (" + self.server + ")")
			
			if self._client_connected_listener != None:
				self._client_connected_listener.client_connected(self)
			
		@On(self._bot, "end")
		def end(*args):
			print("Bot ended!", args)
		
		@On(self._bot, "chat")
		def handle(_, username, message, *args):
			print(args)
			self._connector.message_received(username, message)
	
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
	
	def send_message(self, msg: str):
		self._bot.chat(msg)
		
	def send_command(self, cmd: str):
		self._bot.chat(f"/{msg}")
