#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Item import Item
from Position import Position
from entities.Entity import Entity

class ClientPetition:
	def send_message(self, msg: str):
		pass
		
	def send_command(self, cmd: str):
		pass
	
	def break_block(self, block: Position):
		pass
	
	def place_block(self, block: Position):
		pass
	
	def equip_item_in_hand(self, item: Item):
		pass
	
	def move_to(self, pos: Position):
		pass
	
	def look_at(self, pitch: float, yaw: float):
		pass
	
	def synchronize(self):
		pass
	
	def hit(self):
		pass
	
	def use(self):
		pass

	def attack(self, entity: Entity):
		pass
