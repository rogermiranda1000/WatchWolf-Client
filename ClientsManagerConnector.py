#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread

class ClientsManagerConnector:
	def __init__(self, ClientsManagerPetition petition_handler):
		self._petition_handler = petition_handler
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), 7000))
		self.socket.listen(5)
		
		while True:
			# accept connections from outside
			(client_socket, address) = serversocket.accept() # TODO send address to the Client so it only replies to that one
			
			Thread(target = _client_manager, args = (self, clientsocket)).start()
	
	def _client_manager(self, socket):
		print(socket)
		print(ConnectorHelper.readShort(socket))
