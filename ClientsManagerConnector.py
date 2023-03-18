#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from threading import Thread
from ClientsManagerPetition import ClientsManagerPetition
from ConnectorHelper import ConnectorHelper
import ipaddress

class ClientsManagerConnector:
	def __init__(self, petition_handler: ClientsManagerPetition, port: int = 7000):
		self._petition_handler = petition_handler
		self._port = port
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), self._port))
		self.socket.listen(5)
		
		while True:
			# accept connections from outside
			(client_socket, address) = self.socket.accept() # TODO send address to the Client so it only replies to that one
			
			Thread(target = self._client_manager, args = (client_socket,ClientsManagerConnector._is_public_ip(address))).start()
	
	@staticmethod
	def _is_public_ip(address) -> bool:
		ip = ipaddress.ip_address(address[0])
		return not ip.is_private
	
	def _client_manager(self, socket, public_access: bool):
		while True:
			msg = ConnectorHelper.readShort(socket)
			if msg == 0b000000000001_0_010:
				# start client petition
				username = ConnectorHelper.readString(socket)
				ip = ConnectorHelper.readString(socket)
				
				print("Starting client " + username + " at server " + ip + "...")
				user_ip = self._petition_handler.start_client(username, ip, public_access)
				if user_ip != "":
					print("Client started at " + user_ip)
				
				# send response
				ConnectorHelper.sendShort(socket, 0b000000000001_1_010)
				ConnectorHelper.sendString(socket, user_ip)
			else:
				print("Unknown request: " + str(msg))
