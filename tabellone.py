#!/usr/bin/python

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import StringIO
import time
import urllib
import json
from acmepins import GPIO

OnBoardButton=GPIO('PC17','INPUT')
score_order=1
url = 'http://biliardino.local/get_scores.json'

#Panel size
size = 32, 32

#Load a TTF font
font1 = ImageFont.truetype("fonts/Ubuntu-B.ttf", 14)
font2 = ImageFont.truetype("fonts/Ubuntu-B.ttf", 12)

score_blue=0;
score_red=0;

def nolink():
	im=Image.new("RGB",size,"black")
	draw = ImageDraw.Draw(im)
	draw.fontmode="1" #No antialias
	draw.text((17,0), remote_data["red_score"], (3,0,0), font=font1)
	del draw


while True:
	if OnBoardButton.digitalRead()==0:
		if (score_order==0):
			score_order=1
		else:
			score_order=0
		print "Premuto %d" % score_order
				
	#Create a 32x32 black image  
	im=Image.new("RGB",size,"black")
	#Create a draw object to draw primitives on the new image 
	draw = ImageDraw.Draw(im)
	draw.fontmode="1" #No antialias

	try:
		remote_data = json.load(urllib.urlopen(url))
		
		if score_order==0:
			draw.text((-1,0), remote_data["blue_score"], (0,0,5), font=font1)
			draw.text((17,0), remote_data["red_score"], (3,0,0), font=font1)
		else:
			draw.text((-1,0), remote_data["red_score"], (3,0,0), font=font1)
			draw.text((17,0), remote_data["blue_score"], (0,0,5), font=font1)
			
		draw.text((0,18), remote_data["time_lapse"], (0,3,0), font=font2)
		draw.line([0,17,32,17],(3,3,0),2)
		draw.line([15,0,15,17],(3,3,0),2)
	except:	
		print "File %s non trovato" % url
		draw.text((0,0), "No", (5,0,0), font=font2)
		draw.text((0,10), "Link", (5,0,0), font=font2)

	del draw

	#Generate a PPM image (a format very similar to byte array RGB we need)
	output = StringIO.StringIO()
	im.save(output, format='PPM')
	buf=output.getvalue()

	#Discard the first 13 bytes of header and save the rest (the
	#RGB array) on the ledpanel driver output buffer
	out_file = open("/sys/class/ledpanel/rgb_buffer","w")
	out_file.write(buf[13:])
	out_file.close()
	del im
	time.sleep(1)
