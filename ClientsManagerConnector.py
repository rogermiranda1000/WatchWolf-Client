#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Thread
from ClientsManagerPetition import ClientsManagerPetition
from ConnectorHelper import ConnectorHelper

class ClientsManagerConnector:
	def __init__(self, petition_handler: ClientsManagerPetition):
		self._petition_handler = petition_handler
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), 7000))
		self.socket.listen(5)
		
		while True:
			# accept connections from outside
			(client_socket, address) = self.socket.accept() # TODO send address to the Client so it only replies to that one
			
			Thread(target = self._client_manager, args = (client_socket,)).start()
	
	def _client_manager(self, socket):
		print(socket)
		print(ConnectorHelper.readShort(socket))
		print(ConnectorHelper.readString(socket)) # user
		print(ConnectorHelper.readString(socket)) # ip
