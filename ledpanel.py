# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from PIL import Image, ImageDraw, ImageFont
import StringIO
import sys
import os
from acmepins import GPIO

class LedPanel():	
	extra_small_font=None
	small_font=None
	medium_font=None
	large_font=None
	arietta_button=None
	scores_order=None
	im=None
	
	def __init__(self):
		#Panel size
		size = 32, 32

		#True time fonts
		self.extra_small_font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 8)	
		self.small_font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 12)	
		self.medium_font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 14)
		self.large_font = ImageFont.truetype("fonts/Ubuntu-B.ttf", 24)	

		self.arietta_button=GPIO('PC17','INPUT')
		self.scores_order=1

		#Create a 32x32 black image  
		self.im=Image.new("RGB",size,"black")

	def refresh(self):
		#Generate a PPM image (a format very similar to byte array RGB we need)
		output = StringIO.StringIO()
		self.im.save(output, format='PPM')
		buf=output.getvalue()

		#Discard the first 13 bytes of header and save the rest (the
		#RGB array) on the ledpanel driver output buffer
		out_file = open("/sys/class/ledpanel/rgb_buffer","w")
		out_file.write(buf[13:])
		out_file.close()

	#Visualizzazione punteggio
	def show_scores(self,blue_score,red_score,time_lapse,the_winner_is):

		#Legge il tastino dietro Arietta per vedere se deve
		#scambiare i risultati 
		if self.arietta_button.digitalRead()==0:
			if (self.scores_order==0):
				self.scores_order=1
			else:
				self.scores_order=0
				
			print "Premuto %d" % self.scores_order
					
		#Create a draw object to draw primitives on the new image 
		draw = ImageDraw.Draw(self.im)
		
		#No anti-aliasing
		draw.fontmode="1" 
		
		#Disegna un rettangolo nero per coprire scritte precedenti
		draw.rectangle((0,0,31,31), outline=0, fill=0)
	
		#Scrive i punteggi
			
		if the_winner_is=="none":
			blue_color=(0,0,5)
			red_color=(5,0,0)
		if the_winner_is=="blue":
			blue_color=(0,0,31)
			red_color=(2,0,0)
		if the_winner_is=="red":
			blue_color=(0,0,2)
			red_color=(31,0,0)
				
		if self.scores_order==0:
			draw.text((-1,0), blue_score, blue_color, font=self.medium_font)
			draw.text((17,0), red_score,  red_color,  font=self.medium_font)
		else:
			draw.text((-1,0), red_score,  red_color,  font=self.medium_font)
			draw.text((17,0), blue_score, blue_color, font=self.medium_font)
			
		#Scrive il tempo
		if the_winner_is=="none":
			draw.text((0,18), time_lapse, (0,3,0), font=self.small_font)
		else:
			draw.text((0,18), time_lapse, (15,15,0), font=self.small_font)
		
		if the_winner_is=="none":
			#Disegna le linee divisorie
			draw.line([0,16,32,16],(3,3,0),2)
			draw.line([15,0,15,16],(3,3,0),2)

		if the_winner_is=="blue":
			draw.line([15,0,15,16],(0,0,5),2)
			draw.line([0,16,32,16],(0,0,5),4)

		if the_winner_is=="red":
			draw.line([15,0,15,16],(5,0,0),2)
			draw.line([0,16,32,16],(5,0,0),4)

		del draw

		self.refresh()
