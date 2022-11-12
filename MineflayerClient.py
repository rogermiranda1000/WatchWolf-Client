#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition
from MinecraftClient import MinecraftClient
from ClientConnector import ClientConnector
from OnClientConnected import OnClientConnected
from OnClientDisconnected import OnClientDisconnected

import socket
from threading import Thread

from javascript import require, On, Once, console
mineflayer = require("mineflayer", "latest")

class MineflayerClient(MinecraftClient):
	def __init__(self, host: str, port: int, username: str, assigned_port: int, on_client_connected: OnClientConnected, on_client_disconnected: OnClientDisconnected):
		super().__init__(host, port, username)
		self._connector = ClientConnector(self, assigned_port)
		self._client_connected_listener = on_client_connected
		self._client_disconnected_listener = on_client_disconnected
		
		self._bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username
		})
		
		@On(self._bot, "login")
		def login(this):
			print(this._username + " connected to the server (" + this.server + ")")
			
			if this._client_connected_listener != None:
				this._client_connected_listener.client_connected(this)
