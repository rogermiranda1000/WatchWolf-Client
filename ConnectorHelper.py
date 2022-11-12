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
		size = min(len(data), 65535) # 2 bytes for the size
		ConnectorHelper.sendShort(socket, size)
		socket.sendall(b''.join([bytes([ord(e)]) for e in data[:size]])) # convert the string characters (from 0 to size-1) into an array of bytes
	
	@staticmethod
	def readShort(socket) -> int:
		lsb = int(socket.recv(1)[0])
		msb = int(socket.recv(1)[0])
		return (msb<<8) | lsb
	
	@staticmethod
	def sendShort(socket, data: int):
		lsb = bytes([data & 0b11111111])
		msb = bytes([(data >> 8) & 0b11111111]) # AND just in case
		socket.sendall(b''.join([lsb, msb]))