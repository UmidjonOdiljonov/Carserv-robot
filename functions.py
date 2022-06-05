import mysql.connector
from mysql.connector import MySQLConnection, Error
import logging

dbconfig = {'host':'localhost', 'user':'root', 'password':'Umid_djan18072002', 'charset':'utf8mb4', 'database':'carserv'}

try:
	conn = MySQLConnection(**dbconfig)
	cursor = conn.cursor()
except:
	print('Vaaaay')

def get_info_user(chat_id):
	cursor.execute("SELECT * FROM users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		return a[0]
	else:
		return False

def get_info_language(chat_id):
	cursor.execute("SELECT language FROM users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		return a[0]
	else:
		return False

def set_language_user(chat_id, language):
	cursor.execute("UPDATE users SET language='{}' WHERE user_id={}".format(language, chat_id))
	return True

def get_phone_user(chat_id):
	cursor.execute("SELECT phone_number FROM users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		return a[0]
	else:
		return False

def next_step(user_id:int, step:str): #userni stepini edit qilish
	try:
		cursor.execute("SELECT user_id FROM steps WHERE user_id={}".format(user_id))
		if cursor.fetchone():
			cursor.execute("UPDATE steps SET step='{}' WHERE user_id={}".format(step, user_id))
		else:
			cursor.execute("INSERT INTO steps(user_id, step) VALUES ({}, '{}')".format(user_id, step))
		conn.commit()
	except Exception as ex:
		logging.error(ex)
	return True

def step_info(user_id:int): #user danniy moment qayerda turganligi (muhim funksiya emas faqat 1 ta joyda foydalanilgan)
	try:
		cursor.execute("SELECT step FROM steps WHERE user_id={}".format(user_id))
		a = cursor.fetchone()
		return a[0]
	except:
		next_step(user_id, 'main')
		return 'main'

def set_number_function(chat_id, number):
	cursor.execute("UPDATE users SET phone_number='{}' WHERE user_id={}".format(number, chat_id))

	return True

def get_number(chat_id):
	cursor.execute("SELECT phone_number FROM users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		return a[0]
	else:
		return False

def create_user(chat_id):
	cursor.execute("INSERT INTO users(user_id) VALUES (%s)", (chat_id,))
	conn.commit()
	return True

def check_location(chat_id):
	cursor.execute("SELECT `location_date`, `latitude`, `longitude` from users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		print(a)
	else:
		return False