from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

MainMenu = KeyboardButton('Главное меню')

b1=KeyboardButton('Кинуть кость')
b2=KeyboardButton('Тест')
b3=KeyboardButton('Далее')

menu = ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2, b3)

btnInfo = KeyboardButton('Информация')
btnCrypto=KeyboardButton('Криповалюта')

secMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnCrypto,MainMenu)

cb1 = InlineKeyboardButton(text ='Bitcoin',callback_data='cc_bitcoin')
cb2 = InlineKeyboardButton(text ='Litecoin',callback_data='cc_litecoin')
cb3 = InlineKeyboardButton(text ='Ethereum',callback_data='cc_ethereum')

cry_list = InlineKeyboardMarkup(row_width=1)
cry_list.insert(cb1)
cry_list.insert(cb2)
cry_list.insert(cb3)