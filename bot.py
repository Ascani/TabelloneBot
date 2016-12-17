# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from telegram.ext import Updater, CommandHandler, Handler
from telegram import ReplyKeyboardMarkup

class Bot():
	job_queue=None
	chat_ids=[]

	menu_keyboard = ReplyKeyboardMarkup([['/start','/stop']])
	menu_keyboard.one_time_keyboard=False
	menu_keyboard.resize_keyboard=True

	def __init__(self,token):
		updater = Updater(token)
		self.job_queue = updater.job_queue

		updater.dispatcher.add_handler(CommandHandler('start', self.cmd_start))
		updater.dispatcher.add_handler(CommandHandler('stop', self.cmd_stop))
		updater.start_polling()

	def send_alert(self,text):
		if len(self.chat_ids)>=0:
			for chat_id in self.chat_ids:
				self.job_queue.bot.sendMessage(chat_id,text)

	def cmd_start(self,bot, update):
		print "Ricevuto /start"
		bot.sendMessage(update.message.chat_id, text="Benvenuto in TabelloneBot.", reply_markup=self.menu_keyboard)
		#update.message.reply_text('Hello' . format(update.message.from_user.first_name))
		self.chat_ids+=[update.message.chat_id]
		
	def cmd_stop(self, bot, update):	
		print "Ricevuto /stop"
		bot.sendMessage(update.message.chat_id, text="Non riceverai piu' aggiornamenti", reply_markup=self.menu_keyboard)
		try:
			self.chat_ids.remove(update.message.chat_id)	
			return
		except ValueError:
			pass

