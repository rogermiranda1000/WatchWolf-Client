#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ConnectorHelper:
	@staticmethod
	def readString(socket) -> str:
		return ""
	
	@staticmethod
	def sendString(socket, data: str):
		pass
	
	@staticmethod
	def readShort(socket) -> int:
		lsb = int(socket.recv(1))
		msb = int(socket.recv(1))
		return (msb<<8) | lsb