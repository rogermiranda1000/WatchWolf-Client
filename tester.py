#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse # Arguments
from deps.minecraft.networking.packets.clientbound.play import ChatMessagePacket
from deps.minecraft.networking.connection import Connection
from deps.minecraft.authentication import AuthenticationToken

def getArgs():
	parser = argparse.ArgumentParser(description='Minecraft Plugins tester [client].')
	parser.add_argument('-a','--address', help='Minecraft server\'s IP', type=str,required=True)
	parser.add_argument('-p','--port', help='Minecraft server\'s port', type=int, required=False, default=25565)
	return parser.parse_args()

def getToken():
	data = None
	with open('login.txt') as file:
		for line in file.readlines():
			data = line.split()
	token = AuthenticationToken()
	if data is None or not token.authenticate(data[0], data[1]): return None
	return token

connection = None
if __name__ == '__main__':
	server = getArgs()
	connection = Connection(server.address, server.port, auth_token=getToken())
	connection.connect()
	
	while connection != None:
		try:
			pass
			
		except KeyboardInterrupt:
			connection.disconnect
			connection = None

@connection.listener(ChatMessagePacket)
def print_chat(chat_packet):
    print("Position: " + str(chat_packet.position))
    print("Data: " + chat_packet.json_data)
