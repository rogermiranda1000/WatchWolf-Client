#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientsManagerPetition import ClientsManagerPetition
from ClientsManagerConnector import ClientsManagerConnector
from MineflayerClient import MineflayerClient
from OnClientDisconnected import OnClientDisconnected

class ClientsManager(ClientsManagerPetition, OnClientDisconnected):
	def __init__(self, client_builder, port: int = 7000):
		self._connector = ClientsManagerConnector(self)
		self._client_builder = client_builder
		
		self._base_port = port+1
		self._client_list = {}
		
	def run(self):
		self._connector.run()
		
	def client_disconnected(self, client):
		pass # TODO remove [syncronized] client from self._client_list
	
	def start_client(self, username: str, server_ip: str) -> str:
		ip = server_ip.split(":")
		port = self.get_min_id()
		client = self._client_builder(username, ip[0], ip[1], port, self)
		self._client_list[port] = client
		return "127.0.0.1:" + str(port) # TODO get IP
	
	def get_min_id(self) -> int:
		current_port = self._base_port
		while (current_port in self._client_list):
			current_port += 1
		return current_port

if __name__ == '__main__':
	client_builder = lambda username, ip, ip_port, assigned_port, on_client_disconnected : MineflayerClient(ip, ip_port, username, assigned_port, on_client_disconnected)
	ClientsManager(client_builder).run()
