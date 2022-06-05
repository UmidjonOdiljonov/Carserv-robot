import mysql.connector
from mysql.connector import MySQLConnection, Error
import logging
import datetime
from datetime import timedelta

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
	cursor.execute("INSERT INTO users(user_id) VALUES ({})".format(chat_id))
	conn.commit()
	return True

def check_location(chat_id):
	cursor.execute("SELECT `location_date`, `latitude`, `longitude` from users WHERE user_id={}".format(chat_id))
	a = cursor.fetchone()
	if a:
		if a[0]:
			date_in_base = a[0] + timedelta(minutes=1000)
			date = datetime.datetime.utcnow() + timedelta(hours=5)
			if date_in_base>date:
				return True
			else:
				False
		else:
			False
	else:
		return False

def set_location(chat_id, latitude, longitude):
	date = datetime.datetime.utcnow() + timedelta(hours=5)
	create_time = date.strftime('%Y-%m-%d %H:%M:%S')
	cursor.execute("UPDATE users SET latitude={}, longitude={}, location_date='{}' WHERE user_id={}".format(latitude, longitude, create_time, chat_id))
	conn.commit()
	return True

def get_elements(chat_id, type_element, page):
	dictionary = {"moyka":3,
				  "zapravka":2,
				  "service":1}

	pagination = page*5
	if type_element == "all":
		cursor.execute("SELECT *, (select latitude from carserv.users WHERE user_id={}) as l1, (select longitude from carserv.users WHERE user_id={}) as l2  FROM services right join location_connection on services.location_id=location_connection.id order by (abs(l1-latitude)+abs(l2-longitude)) asc limit {}, 5;".format(chat_id, chat_id, pagination))
	else:
		cursor.execute("SELECT *, (select latitude from carserv.users WHERE user_id={}) as l1, (select longitude from carserv.users WHERE user_id={}) as l2  FROM services cross join location_connection on services.location_id=location_connection.id having service_type={} order by (abs(l1-latitude)+abs(l2-longitude)) asc limit {}, 5;".format(chat_id, chat_id, dictionary[type_element], pagination))
	a = cursor.fetchall()
	if a:
		return a
	else:
		return False

def get_info(product_id):
	cursor.execute("SELECT * FROM carserv.service_connection left join services on services.id=service_connection.service_id left join service_type on service_type.id=type_id_service left join fueling_types on fueling_types.id=type_id_fueling left join carwash_types on carwash_types.id=type_id_carwash where service_id={};".format(product_id))
	a = cursor.fetchall()
	if a:
		return a
	else:
		return False