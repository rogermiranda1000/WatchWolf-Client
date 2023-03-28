#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ClientPetition import ClientPetition
from MinecraftClient import MinecraftClient
from ClientConnector import ClientConnector
from OnClientConnected import OnClientConnected
from OnClientDisconnected import OnClientDisconnected

from Position import Position
from Item import Item
from entities.Entity import Entity

import socket
from threading import Thread, Lock
from math import ceil
from time import sleep
import datetime

from javascript import require, On, Once, console
mineflayer = require('mineflayer', 'latest')
pathfinder = require('mineflayer-pathfinder').pathfinder
Movements = require('mineflayer-pathfinder').Movements
GoalBlock = require('mineflayer-pathfinder').goals.GoalBlock
Vec3 = require("vec3").Vec3

# time to force the login
login_timeout_sec = 120

# the MC packets also have a timeout
packet_timeout_sec = 120

class MineflayerClient(MinecraftClient):
	TIMEOUT_BETWEEN_MESSAGESS = 400
    
	def __init__(self, host: str, port: int, username: str, assigned_port: int, on_client_connected: OnClientConnected, on_client_disconnected: OnClientDisconnected):
		super().__init__(host, port, username)
		self._printer = lambda msg,username=username,host=host,port=port : print(f"[{username} - {host}:{str(port)}] {msg}")
		self._connector = ClientConnector(self, assigned_port, self._printer)
		self._client_connected_listener = on_client_connected
		self._client_disconnected_listener = on_client_disconnected
		
		self._thread_lock = Lock()
		self._timedout = None
		Thread(target = self._login_timeout).start()
		
		self._bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username,

			"checkTimeoutInterval": packet_timeout_sec * 1000
		})
        
		self._cmd_return_lock = threading.Lock()
		self._cmd_return = []
		
		# add-ons
		self._bot.loadPlugin(pathfinder)
		
		Thread(target = self._connector.run, args = ()).start()
		
		@On(self._bot, "login")
		def login(_):
			self._thread_lock.acquire()
			if self._timedout != None:
				# too late
				self._thread_lock.release()
				return
			self._timedout = False
			self._thread_lock.release()
			
			print(self._username + " connected to the server (" + self.server + ")")
			
			# pathfinder initialization
			defaultMove = Movements(self._bot)
			defaultMove.canDig = False
			defaultMove.placeCost = 8000
			self._bot.pathfinder.setMovements(defaultMove)
			
			# notify 
			if self._client_connected_listener != None:
				self._client_connected_listener.client_connected(self)
			
		@On(self._bot, "end")
		def end(_, reason): # TODO is it really the reason?
			print("Bot ended: " + reason)
		
		@On(self._bot, "chat")
		def handle(_, username, message, *args):
			self._connector.message_received(username, message)
            
		@On(self._bot, "message")
		def message(_, message, position, *args):
			if position != "system": return # we expect returns to commands; ignore other things
			self._cmd_return_lock.acquire()
			self._cmd_return.append(message.toString())
			self._cmd_return_lock.release()
	
	def __del__(self):
		pass # TODO stop socket server
	
	def _login_timeout(self):
		if self._client_connected_listener != None:
			sleep(login_timeout_sec)
			
			self._thread_lock.acquire()
			timedout = (self._timedout == None)
			if timedout:
				self._timedout = True
				self._client_connected_listener.client_connected(self)
			self._thread_lock.release()
			
			if timedout:
				print(self._username + ", at " + self.server + " timedout")
	
	@property
	def timedout(self) -> bool:
		return self._timedout
	
	def send_message(self, msg: str):
		self._bot.chat(msg)
		
	def send_command(self, cmd: str, timeout: int) -> str:
        # new command -> new reply (empty the queue)
		self._cmd_return_lock.acquire()
		self._cmd_return = []
		self._cmd_return_lock.release()

		self._bot.chat(f"/{cmd}")

        # we'll be waiting for <timeout>ms for a response, unless we get data and
        # then got nothing during <TIMEOUT_BETWEEN_MESSAGESS>ms
		sent_at = datetime.datetime.now()
		previous_lenght = 0
		while (datetime.datetime.now() - sent_at).total_seconds() * 1000 < timeout:
			self._cmd_return_lock.acquire()
			current_lenght = len(self._cmd_return)
			self._cmd_return_lock.release()

			if current_lenght > 0 and current_lenght == previous_lenght:
				break # TIMEOUT_BETWEEN_MESSAGESS has passed, and no new messages had been readed

			previous_lenght = current_lenght
			sleep(MineflayerClient.TIMEOUT_BETWEEN_MESSAGESS / 1000)

		self._cmd_return_lock.acquire()
		r = '\n'.join(self._cmd_return)
		self._cmd_return_lock.release()
		return r
        
	@staticmethod
	def _pos_to_vec3(pos: Position) -> Vec3:
		# 10.5 -> 10; -27.5 -> -28
		return Vec3(-ceil(-pos.x), ceil(pos.y), -ceil(-pos.z)) # TODO world
	
	def _find_item_in_player(self, item: Item): # TODO return type
		filter = (i for i in self._bot.inventory.items() if i.name == item.type.name.lower() and i.count == item.amount)
		return next(filter, None) # get the first item that matches (None if none)
	
	# @ref https://github.com/PrismarineJS/mineflayer/blob/master/examples/digger.js
	def break_block(self, block: Position):
		target = self._bot.blockAt(MineflayerClient._pos_to_vec3(block))
		if target and self._bot.canDigBlock(target):
			try:
				self._bot.dig(target)
				self._printer(f"Finished breaking block at {block}")
			except Exception as err:
				self._printer(f"[e] Break block at {block} raised error {err.message}")
	
	def place_block(self, block: Position):
		try:
			# find a block & face to place
			for offset in [(0,-1,0),(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0)]:
				base_block_location=MineflayerClient._pos_to_vec3(block+offset)
				base_block=self._bot.blockAt(base_block_location)
				if base_block is not None and base_block.id != "minecraft:air":
					face=Vec3(-offset[0],-offset[1],-offset[2]) # the face will be the inverse of position
					self._bot.placeBlock(base_block, face)
					return # TODO check if placed (it can be a block where you can't place any item)
		except Exception as err:
			self._printer(f"Exception while placing a block at {block}: {err}")
	
	# @ref https://github.com/PrismarineJS/mineflayer/blob/master/examples/digger.js
	# @ref https://github.com/PrismarineJS/mineflayer/blob/b7650c69e2b3db8e6c0fe8d227f66cb5c2c959a0/lib/plugins/simple_inventory.js#L88
	# @ref https://github.com/PrismarineJS/mineflayer/issues/2383
	def equip_item_in_hand(self, item: Item):
		target = self._find_item_in_player(item)
		if not target:
			self._printer(f"{item} not found in player's inventory")
			return
			
		self._bot.equip(target, 'hand') # TODO bot.moveSlotItem? @ref https://stackoverflow.com/a/55584100/9178470
	
	# @ref https://github.com/PrismarineJS/mineflayer-pathfinder#example
	def move_to(self, pos: Position):
		goal = GoalBlock(pos.x, pos.y, pos.z)
		self._bot.pathfinder.goto(goal)
		
	def look_at(self, pitch: float, yaw: float):
		self._bot.look(yaw, pitch, True) # look transition-free
	
	def hit(self):
		self._bot.swingArm() # TODO attack
	
	# @ref https://github.com/PrismarineJS/mineflayer/issues/421
	# @ref https://github.com/PrismarineJS/mineflayer/issues/766
	def use(self):
		self._bot.activateItem() # TODO useOn, mount, openContainer...
		sleep(0.1)
		self._bot.deactivateItem()

	# @ref https://github.com/PrismarineJS/mineflayer/blob/master/docs/api.md#botattackentity-swing--true
	# @ref https://github.com/PrismarineJS/prismarine-entity#entityid
	# @ref https://github.com/PrismarineJS/mineflayer/blob/master/examples/trader.js#L49
	def attack(self, uuid: str):
		entities = [self._bot.entities[id] for id in self._bot.entities] # Python equivalent of `Object.keys(self._bot.entities).map(id => self._bot.entities[id])`
		match = next((e for e in entities if e.uuid == uuid), None)
		if match != None:
			self._bot.attack(match)
			sleep(2) # TODO is attack async?
		else:
			self._printer(f"Entity with uuid={uuid} not found nearby")
