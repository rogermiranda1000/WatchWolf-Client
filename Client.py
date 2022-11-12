#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from javascript import require
mineflayer = require("mineflayer", "latest")

class Client:
	def __init__(self):
		self.bot = mineflayer.createBot({
			"host": host,
			"port": port,
			"username": username,
			"port": port
		})
