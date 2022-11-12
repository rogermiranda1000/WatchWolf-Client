#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition

class ClientConnector:
	def __init__(self, petition_handler: ClientPetition, port: int):
		self._petition_handler = petition_handler
		self._port = port
