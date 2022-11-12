#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ConnectorHelper:
	@staticmethod
	def readString(socket) -> str:
		size = ConnectorHelper.readShort(socket)
		data = socket.recv(size)
		return ''.join([chr(e) for e in data])
	
	@staticmethod
	def sendString(socket, data: str):
		pass
	
	@staticmethod
	def readShort(socket) -> int:
		lsb = int(socket.recv(1)[0])
		msb = int(socket.recv(1)[0])
		return (msb<<8) | lsb