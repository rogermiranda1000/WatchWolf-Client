#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

from ClientsManagerPetition import ClientsManagerPetition
from ClientsManagerConnector import ClientsManagerConnector
from MineflayerClient import MineflayerClient

from MinecraftClient import MinecraftClient
from OnClientConnected import OnClientConnected
from OnClientDisconnected import OnClientDisconnected

class ClientsManager(ClientsManagerPetition, OnClientConnected, OnClientDisconnected):
	def __init__(self, client_builder, port: int = 7000):
		self._connector = ClientsManagerConnector(self)
		self._client_builder = client_builder
		
		self._base_port = port+1
		self._client_list = {}
		
		self._done_clients = []
		self._thread_lock = threading.Lock()
		
	def run(self):
		self._connector.run()
	
	def client_connected(self, client: MinecraftClient):
		self._thread_lock.acquire()
		self._done_clients.append(client)
		self._thread_lock.release()
		
	def client_disconnected(self, client: MinecraftClient):
		pass # TODO remove [syncronized] client from self._client_list
	
	def start_client(self, username: str, server_ip: str) -> str:
		ip = server_ip.split(":")
		port = self.get_min_id()
		client = self._client_builder(username, ip[0], int(ip[1]), port, self, self)
		self._client_list[port] = client
		
		# wait for client_connected signal
		# TODO move as anync message
		stay = True
		while stay:
			self._thread_lock.acquire()
			stay = not (client in self._done_clients)
			self._thread_lock.release()
		self._thread_lock.acquire()
		self._done_clients.remove(client)
		self._thread_lock.release()
		
		if client.timedout:
			return "" # error
		else:
			return "127.0.0.1:" + str(port) # TODO get IP
	
	def get_min_id(self) -> int:
		current_port = self._base_port
		while (current_port in self._client_list):
			current_port += 1
		return current_port

if __name__ == '__main__':
	client_builder = lambda username, ip, ip_port, assigned_port, on_client_connected, on_client_disconnected : MineflayerClient(ip, ip_port, username, assigned_port, on_client_connected, on_client_disconnected)
	ClientsManager(client_builder).run()
