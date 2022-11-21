#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

from ConnectorHelper import ConnectorHelper
from OnMessage import OnMessage
from ClientPetition import ClientPetition

class ClientConnector(OnMessage):
	def __init__(self, petition_handler: ClientPetition, port: int, printer):
		self._petition_handler = petition_handler
		self._port = port
		self._printer = printer
		self._socket = None
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), self._port))
		self.socket.listen(5)
		
		while True:
			# accept connections from outside
			(client_socket, address) = self.socket.accept() # TODO send address to the Client so it only replies to that one
			
			self._socket = client_socket
			while True:
				msg = ConnectorHelper.readShort(client_socket)
				if msg == 0b000000000011_0_011:
					message = ConnectorHelper.readString(client_socket)
					self._printer(f"Sending '{message}'...")
					self._petition_handler.send_message(message)
				elif msg == 0b000000000100_0_011:
					command = ConnectorHelper.readString(client_socket)
					self._printer(f"Running '{command}'...")
					self._petition_handler.send_command(command)
				elif msg == 0b000000000101_0_011:
					pos = ConnectorHelper.readPosition(client_socket)
					self._printer(f"Breaking block at {pos}...")
					self._petition_handler.break_block(pos)
				elif msg == 0b000000000110_0_011:
					item = ConnectorHelper.readItem(client_socket)
					self._printer(f"Set {item} as item in hand")
					self._petition_handler.equip_item_in_hand(item)
				else:
					self._printer("Unknown request: " + str(msg))
			self._socket = None # socket closed
	
	def message_received(self, username: str, msg: str):
		if self._socket == None:
			return # no one to send
		
		ConnectorHelper.sendShort(self._socket, 0b000000000011_1_011)
		ConnectorHelper.sendString(self._socket, username)
		ConnectorHelper.sendString(self._socket, msg)
