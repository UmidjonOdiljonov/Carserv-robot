import logging

from aiogram import Bot, Dispatcher, executor, types

from configs import *
from functions import *
import text
from keyboards import *

# Configure logging
logging.basicConfig(level=logging.INFO)

photo_urls = {"moyka":"https://static.zarnews.uz/crop/9/5/720__80_951e39f4260e1eddddc3a785bac730d4.jpg?img=self&v=1604129918",
				  "zapravka":"https://www.autostrada.uz/wp-content/uploads/2018/12/zapravka-uzbekneftegaz-azs-v-tashkente.jpg",
				  "service":"https://amastercar.ru/img/auto_service_4.jpg"}

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	chat_id = message.chat.id
	if get_info_user(chat_id):  # false qaytsa mavjud emas, yo'qsa til qaytadi
		language = get_info_language(chat_id)
		if language:
			if get_number(chat_id):
				if (language == "uz"):
					kb_menu = kb_menu_uz
				else:
					kb_menu = kb_menu_ru
				next_step(chat_id, 'main')
				await bot.send_message(chat_id, text.main_menu[language], reply_markup=kb_menu, parse_mode='markdown')
			else:
				next_step(chat_id, "set_phone")
				if (language == "uz"):
					kb_phone = kb_phone_uz
				else:
					kb_phone = kb_phone_ru
				await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
				await bot.send_message(chat_id=chat_id, text=text.request_phone[language], reply_markup=kb_phone)
		else:
			next_step(chat_id, "set_language")
			await bot.send_message(chat_id, text.first_start, parse_mode="markdown", reply_markup=kb_language)
	else:
		create_user(chat_id)
		next_step(chat_id, "set_language")
		await bot.send_message(chat_id, text.first_start, parse_mode="markdown", reply_markup=kb_language)


@dp.message_handler(content_types=['text', 'contact', 'location'])
async def main(message: types.Message):
	chat_id = message.chat.id
	step = step_info(chat_id)
	if step == "set_phone":
		if message.contact:
			if message.from_user.id == message.contact.user_id:
				delete_kb = types.ReplyKeyboardRemove()
				a = await bot.send_message(chat_id, "Wait...", reply_markup=delete_kb)
				await bot.delete_message(chat_id=chat_id, message_id=a.message_id)
				set_number_function(chat_id, message.contact.phone_number)
				language = get_info_language(chat_id)
				if (language == "uz"):
					kb_menu = kb_menu_uz
				else:
					kb_menu = kb_menu_ru
				next_step(chat_id, 'main')
				await bot.send_message(chat_id, text.main_menu[language], reply_markup=kb_menu, parse_mode='markdown')
		else:
			language = get_info_language(chat_id)
			next_step(chat_id, "set_phone")
			if (language == "uz"):
				kb_phone = kb_phone_uz
			else:
				kb_phone = kb_phone_ru
			await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
			await bot.send_message(chat_id=chat_id, text=text.request_phone[language], reply_markup=kb_phone)

	elif step == "set_language":
		await bot.send_message(chat_id, text.first_start, parse_mode="markdown", reply_markup=kb_language)

	elif step == "request_location":
		language = get_info_language(chat_id)
		latitude = message.location.latitude
		longitude = message.location.longitude
		set_location(chat_id, latitude, longitude)
		if (language == "uz"):
			kb_menu = kb_menu_uz
		else:
			kb_menu = kb_menu_ru
		await bot.send_message(chat_id, text.main_menu[language], reply_markup=kb_menu)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(call):
	chat_id = call.message.chat.id
	print(call.data)
	if call.data.startswith("set_language"):
		language = call.data.split("_")[-1]
		set_language_user(chat_id, language)
		if get_phone_user(chat_id):
			if (language == "uz"):
				kb_menu = kb_menu_uz
			else:
				kb_menu = kb_menu_ru
			await bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
										text=text.edited_language[language], reply_markup=kb_menu)
		else:
			next_step(chat_id, "set_phone")
			if (language == "uz"):
				kb_phone = kb_phone_uz
			else:
				kb_phone = kb_phone_ru
			await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
			await bot.send_message(chat_id=chat_id, text=text.request_phone[language], reply_markup=kb_phone)

	elif call.data.startswith("get"):
		if not check_location(chat_id):
			next_step(chat_id, "request_location")
			language = get_info_language(chat_id)
			if language == "uz":
				request_location = kb_request_location_uz
			else:
				request_location = kb_request_location_ru
			await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
			await bot.send_message(chat_id, text.request_location[language], reply_markup=request_location)

		elif call.data.startswith("get_"):
			janr = call.data.split("_")[1]
			page = int(call.data.split("_")[2])
			elements = get_elements(chat_id, janr, page)
			kb = types.InlineKeyboardMarkup()

			for i in elements:
				a = types.InlineKeyboardButton(text=i[1], callback_data="info_{}_{}_{}".format(i[0], janr, page))
				kb.add(a)
			back = types.InlineKeyboardButton(text="⬅️Orqaga", callback_data="get_{}_{}".format(janr, page - 1))
			home = types.InlineKeyboardButton(text="🏘", callback_data="home")
			next = types.InlineKeyboardButton(text="➡️Keyingi", callback_data="get_{}_{}".format(janr, page + 1))
			if get_elements(chat_id, janr, page+1):
				if page != 0:
					kb.add(back, home, next)
				else:
					kb.add(home, next)
			else:
				if page != 0:
					kb.add(back, home)
				else:
					kb.add(home)
			try:
				await bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Tanlang: ", reply_markup=kb)
			except:
				await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
				await bot.send_message(chat_id, text="Tanlang: ", reply_markup=kb)

	elif call.data == "home":
		language = get_info_language(chat_id)
		if (language == "uz"):
			kb_menu = kb_menu_uz
		else:
			kb_menu = kb_menu_ru
		next_step(chat_id, 'main')
		await bot.delete_message(message_id=call.message.message_id, chat_id=chat_id)
		await bot.send_message(chat_id, text.main_menu[language], reply_markup=kb_menu, parse_mode='markdown')

	elif call.data.startswith("info_"):
		element_id = call.data.split("_")[1]
		janr = call.data.split("_")[2]
		page = call.data.split("_")[3]
		info = get_info(element_id)
		kb = types.InlineKeyboardMarkup()
		text = "{}\n\n{}\n\nRaqami: {}"
		temp_text = ""
		for i in info:
			service_name = i[15]
			service_text = i[16]
			temp1_text = "{}\n{}\n{}\n\n".format(service_name, service_text, i[5])
			temp_text += temp1_text
		text = text.format(i[7], temp_text, i[9])
		back_button = types.InlineKeyboardButton("⬅️Orqaga", callback_data="get_{}_{}".format(janr, page))
		kb.add(back_button)
		await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
		await bot.send_photo(chat_id, caption=text, reply_markup=kb, photo=photo_urls[janr])


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
