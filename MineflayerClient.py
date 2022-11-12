#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition
from ClientConnector import ClientConnector
from OnClientDisconnected import OnClientDisconnected

import socket
from threading import Thread

from javascript import require
mineflayer = require("mineflayer", "latest")

class MineflayerClient(ClientPetition):
	def __init__(self, host: str, port: str, username: str, assigned_port: int, on_client_disconnected: OnClientDisconnected):
		self._connector = ClientConnector(self, assigned_port)
		self._client_disconnected_listener = on_client_disconnected
		
		self.bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username,
			"port": port
		})
