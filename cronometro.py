# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import time

class Cronometro():
	start=None
	
	def __init__(self):
		self.start = time.time()

	def parziale(self):
		end = time.time()
		temp = end-self.start
		hours = temp//3600
		temp = temp - 3600*hours
		minutes = temp//60
		seconds = temp - 60*minutes
		return "%02d:%02d" % (minutes,seconds)

	def reset(self):
		self.start = time.time()
