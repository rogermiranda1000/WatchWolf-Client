#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition

class MinecraftClient(ClientPetition): # every client implements ClientPetition
	# every client has a nickname and a server target
	def __init__(self, host: str, port: int, username: str):
		self._server_ip = host
		self._server_port = port
		self._username = username
	
	@property
	def server(self) -> str:
		return self._server_ip + ":" + str(self._server_port)
