# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

#!/usr/bin/python

import time
import urllib
import json
import sys
from acmepins import GPIO
from ledpanel import LedPanel 

ledpanel=LedPanel()

while True:
	try:
		#Legge dal web server nel biliardino cosa deve visualizzare
		remote_data = json.load(urllib.urlopen("http://biliardino.local/get_scores.json"))

		#Schermata di default con i punteggi
		if remote_data["datatype"]=="scores":
			#banner.stop()
			print "show_scores"
			ledpanel.show_scores(remote_data["blue_score"],remote_data["red_score"],remote_data["time_lapse"],remote_data["the_winner_is"])

	except:	
		print "Unexpected error:", sys.exc_info()[0]
		ledpanel.nolink()

	time.sleep(1)
