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
	def readDouble(socket) -> float:
		r = 0
		for _ in range(8):
			r = (r << 8) | int(socket.recv(1)[0])
		
		# @ref https://en.wikipedia.org/w/index.php?title=Double-precision_floating-point_format&oldid=1124030667#IEEE_754_double-precision_binary_floating-point_format:_binary64
		sign = (r >> 63) > 0
		exponent = (r >> 52) & 0b11111111111
		fraction = r & 4503599627370495 # 52 bits
		
		r = (1 + fraction / 10**52) * (2**(exponent - 1023))
		return -r if sign else r
	
	@staticmethod
	def sendDouble(socket, data: float):
		pass
	
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
		world = ConnectorHelper.readString(socket)
		x = ConnectorHelper.readDouble(socket)
		y = ConnectorHelper.readDouble(socket)
		z = ConnectorHelper.readDouble(socket)
		return Position(world, x, y, z)
	
	@staticmethod
	def sendPosition(socket, pos: Position):
		ConnectorHelper.sendString(socket, pos.world)
		ConnectorHelper.sendDouble(socket, pos.x)
		ConnectorHelper.sendDouble(socket, pos.y)
		ConnectorHelper.sendDouble(socket, pos.z)