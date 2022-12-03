#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition
from MinecraftClient import MinecraftClient
from ClientConnector import ClientConnector
from OnClientConnected import OnClientConnected
from OnClientDisconnected import OnClientDisconnected

from Position import Position
from Item import Item

import socket
from threading import Thread

import threading
import time

from javascript import require, On, Once, console
mineflayer = require('mineflayer', 'latest')
Vec3 = require("vec3").Vec3

# time to force the login
login_timeout_sec = 3

class MineflayerClient(MinecraftClient):
	def __init__(self, host: str, port: int, username: str, assigned_port: int, on_client_connected: OnClientConnected, on_client_disconnected: OnClientDisconnected):
		super().__init__(host, port, username)
		self._printer = lambda msg,username=username,host=host,port=port : print(f"[{username} - {host}:{str(port)}] {msg}")
		self._connector = ClientConnector(self, assigned_port, self._printer)
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
		
		Thread(target = self._connector.run, args = ()).start()
		
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
		def end(_, reason): # TODO is it really the reason?
			print("Bot ended: " + reason)
		
		@On(self._bot, "chat")
		def handle(_, username, message, *args):
			self._connector.message_received(username, message)
	
	def __del__(self):
		pass # TODO stop socket server
	
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
	
	# @ref https://github.com/PrismarineJS/mineflayer/blob/master/examples/digger.js
	def break_block(self, block: Position):
		target = self._bot.blockAt(Vec3(int(block.x), int(block.y), int(block.z)))
		if target and self._bot.canDigBlock(target):
			try:
				self._bot.dig(target) # TODO await
				self._printer(f"Finished breaking block at {block}")
			except Exception as err:
				self._printer(f"[e] Break block at {block} raised error {err.message}")
	
	def equip_item_in_hand(self, item: Item):
		pass
