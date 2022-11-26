#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Item import Item
from Position import Position
from ItemType import ItemType

class ConnectorHelper:
	@staticmethod
	def readString(socket) -> str:
		size = ConnectorHelper.readShort(socket)
		if size == 0:
			return ""
		data = socket.recv(size)
		return ''.join([chr(e) for e in data])
	
	@staticmethod
	def sendString(socket, data: str):
		size = min(len(data), 65535) # 2 bytes for the size
		ConnectorHelper.sendShort(socket, size)
		if size > 0:
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
	
	@staticmethod
	def readItem(socket) -> Item:
		type = ItemType(ConnectorHelper.readShort(socket))
		amount = int(socket.recv(1)[0])
		return Item(type, amount)
	
	@staticmethod
	def sendItem(socket, item: Item):
		pass
	
	@staticmethod
	def readPosition(socket) -> Position:
		return None
	
	@staticmethod
	def sendPosition(socket, pos: Position):
		pass