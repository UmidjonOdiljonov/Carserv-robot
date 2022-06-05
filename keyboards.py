from aiogram import types

kb_language = types.InlineKeyboardMarkup()
button_uz = types.InlineKeyboardButton(text="🇺🇿O'zbek tili", callback_data="set_language_uz")
button_ru = types.InlineKeyboardButton(text="🇷🇺Rus tili", callback_data="set_language_ru")
kb_language.add(button_uz, button_ru)

kb_menu_uz = types.InlineKeyboardMarkup()
service_menu_uz = types.InlineKeyboardButton(text="🔧 Avto servislar", callback_data="get_service_0")
moyka_menu_uz = types.InlineKeyboardButton(text="💦 Avto yuvish xizmati", callback_data="get_moyka_0")
zapravka_menu_uz = types.InlineKeyboardButton(text="⛽️Yoqilg'i quyish", callback_data="get_zapravka_0")
favourites_menu_uz = types.InlineKeyboardButton(text="⭐️Tanlanganlar", callback_data="get_favourites_0")
search_menu_uz = types.InlineKeyboardButton(text="🔍 Qidiruv", switch_inline_query_current_chat="")
profile_menu_uz = types.InlineKeyboardButton(text="👤 Profil", callback_data="set_profile")
kb_menu_uz.add(service_menu_uz)
kb_menu_uz.add(moyka_menu_uz, zapravka_menu_uz)
kb_menu_uz.add(search_menu_uz)
kb_menu_uz.add(profile_menu_uz, favourites_menu_uz)

kb_menu_ru = types.InlineKeyboardMarkup()
service_menu_ru = types.InlineKeyboardButton(text="🔧 Avto servislar", callback_data="get_service_0")
moyka_menu_ru = types.InlineKeyboardButton(text="💦 Avto yuvish xizmati", callback_data="get_moyka_0")
zapravka_menu_ru = types.InlineKeyboardButton(text="⛽️Yoqilg'i quyish", callback_data="get_zapravka_0")
favourites_menu_ru = types.InlineKeyboardButton(text="⭐️Tanlanganlar", callback_data="get_favourites_0")
search_menu_ru = types.InlineKeyboardButton(text="🔍 Qidiruv", switch_inline_query_current_chat="")
profile_menu_ru = types.InlineKeyboardButton(text="👤 Profil", callback_data="set_profile")
kb_menu_ru.add(service_menu_ru)
kb_menu_ru.add(moyka_menu_ru, zapravka_menu_ru)
kb_menu_ru.add(search_menu_ru)
kb_menu_ru.add(profile_menu_ru, favourites_menu_ru)

kb_phone_uz = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
give_number_uz = types.KeyboardButton("✉ ️Yuborish", request_contact=True)
kb_phone_uz.add(give_number_uz)

kb_phone_ru = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
give_number_ru = types.KeyboardButton("✉ ️Yuborish", request_contact=True)
kb_phone_ru.add(give_number_ru)

kb_request_location_uz = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
request_location_uz = types.KeyboardButton("📍 Manzilni yuborish", request_location=True)
kb_request_location_uz.add(request_location_uz)

kb_request_location_ru = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
request_location_ru = types.KeyboardButton("📍 Manzilni yuborish", request_location=True)
kb_request_location_ru.add(request_location_uz)

