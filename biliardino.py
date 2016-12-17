# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import tornado.ioloop
import tornado.web
from crono import Crono
from acmepins import GPIO,PWM
import time
import thread
import threading

# PWM a 38KHz per led IR
led_ir_out = PWM("J4.34",38000)    

# Imposta il duty cycle al 50%
led_ir_out.start(50)
 
crono=Crono()
blue_score=0
red_score=0
last_score="none"


#Controllo di chi ha vinto
def score_check(blue_score,red_score,crono):
	if abs(blue_score-red_score)>=2 and blue_score>=10:
		print "blue wins" 
		crono.stop()
		return True
	if abs(blue_score-red_score)>=2 and red_score>=10:
		print "red wins" 
		crono.stop()
		return True
	return False
	
def blink(gpio,times=1,delay=0.5):
	for i in range(times):
		gpio.on()
		time.sleep(delay)
		gpio.off()
		time.sleep(delay)

def game():
	global crono, blue_score, red_score, last_score

	#Ingressi fotoaccoppiatori IR
	IR_RED=GPIO("J4.36","INPUT")
	IR_BLUE=GPIO("J4.38","INPUT")
	IR_PULL=GPIO("J4.40","INPUT")

	#Led segnalatore on board
	LED=GPIO("J4.24","LOW")

	while True:
		
		if IR_PULL.get_value()==1:
			print "Pull"
			blink(LED,1,0.2)
			counter=0
			while IR_PULL.get_value()==1:
				time.sleep(1)
				counter+=1
				if counter>=2:
					crono.reset()
					crono.start()
					blue_score=0
					red_score=0
					last_score="none"
					print "Reset"
					break
					
			#Annulla l'ultimo goal
			if last_score=="red" and red_score>0:
				red_score-=1
				last_score="none"
				crono.start()
			if last_score=="blue" and blue_score>0:
				blue_score-=1
				last_score="none"
				crono.start()

		if score_check(blue_score,red_score,crono)==False:
			#Lettura IR porta dei rossi	
			if IR_RED.get_value()==1:
				blue_score=blue_score+1
				last_score="blue"
				print "Goal for blue %d" % blue_score
				blink(LED,2,0.2)
				time.sleep(1)

			#Lettura IR porta dei blue	
			if IR_BLUE.get_value()==1:
				red_score=red_score+1
				last_score="red"
				print "Goal for red %d" % red_score
				blink(LED,3,0.2)
				time.sleep(1)

class get_scores(tornado.web.RequestHandler):
	def get(self):
		global crono,blue_score,red_score
		
#		print "Remote IP: %s" % repr(self.request.remote_ip)
		self.write('{"blue_score":"%02d","red_score":"%02d","time_lapse":"%s"}' % (blue_score,red_score,crono.get()))

application = tornado.web.Application([
	(r"/get_scores.json", get_scores),
	(r"/(.*)", tornado.web.StaticFileHandler, {"path": ".","default_filename": "index.html"}),
])

if __name__ == "__main__":
	thread.start_new_thread(game,())

	application.listen(80,"0.0.0.0")	
	tornado.ioloop.IOLoop.instance().start()
	
