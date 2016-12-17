# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import time

class Crono():
	last_get=0
	total_time=0
	run=False
	
	def __init__(self):
		self.total_time=0
		self.last_get=time.time()
		self.run=True
		
	def stop(self):
		self.run=False

	def start(self):
		self.run=True
		
	def get(self):
		if self.run==True:
			now = time.time()
			delta_time = now-self.last_get
			self.total_time+=delta_time
			self.last_get = now
		else:
			self.last_get=time.time()			
		
		hours = self.total_time//3600
		self.total_time = self.total_time - 3600*hours
		minutes = self.total_time//60
		seconds = self.total_time - 60*minutes
		return "%02d:%02d" % (minutes,seconds)

	def reset(self):
		self.total_time=0
		self.last_get=time.time()
		self.run=False
		
