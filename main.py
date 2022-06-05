import logging

from aiogram import Bot, Dispatcher, executor, types

from configs import *
from functions import *
import text
from keyboards import *

# Configure logging
logging.basicConfig(level=logging.INFO)

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

@dp.message_handler(content_types=['text', 'contact'])
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

@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(call):
	chat_id = call.message.chat.id
	if check_location(chat_id):
		pass

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


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
