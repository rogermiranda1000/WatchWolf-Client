#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientsManagerPetition import ClientsManagerPetition
from ClientsManagerConnector import ClientsManagerConnector

class ClientsManager(ClientsManagerPetition):
	def __init__(self):
		self._connector = ClientsManagerConnector(self)
		
	def run(self):
		self._connector.run()
	
	def start_client(self, username: str, server_ip: str) -> str:
		return "" # TODO

if __name__ == '__main__':
	ClientsManager().run()
