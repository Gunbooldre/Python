from aiogram import Bot,Dispatcher,types
from aiogram.types import ParseMode,ContentType
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, bold, italic
from pycoingecko import CoinGeckoAPI # крипто библиотека не трогать
import aiogram.utils.markdown as fmt
from aiogram.utils import deep_linking
from aiogram.utils import executor 
import logging

import mark as key
from quizer import Quiz

API_TOKEN = '5094392699:AAFJHT9dE8NKRp_Sz7DzaN7rX6N9M3Ky50s'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
cg = CoinGeckoAPI ()
quizzes_database = {}  # здесь хранится информация о викторинах
quizzes_owners = {}    # здесь хранятся пары "id викторины <--> id её создателя"



@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer:types.PollAnswer):
    quiz_owner = quizzes_owners.get(quiz_answer.poll_id)
    if not quiz_owner:
        logging.error(f"Cant find author with this quiz{quiz_answer.poll_id}")
        return 
    for saved_quiz in quizzes_database(quiz_owner):
        if saved_quiz.quiz_id == quiz_answer.poll_id:
            if saved_quiz.correct_option_id == quiz_answer.option_id[0]:
                saved_quiz.winners.append(quiz_answer.user_id)
                if len(saved_quiz.winners) == 2:
                    await bot.stop_poll(saved_quiz.chat_id,saved_quiz.message_id)


@dp.poll_handler(lambda active_quiz: active_quiz.is_closed is True)
async def just_poll_answer(active_quiz: types.Poll):

    quiz_owner = quizzes_owners.get(active_quiz.id)
    if not quiz_owner:
        logging.error(f"Не могу найти автора викторины с active_quiz.id = {active_quiz.id}")
        return
    for num, saved_quiz in enumerate(quizzes_database[quiz_owner]):
        if saved_quiz.quiz_id == active_quiz.id:
            # Используем ID победителей, чтобы получить по ним имена игроков и поздравить.
            congrats_text = []
            for winner in saved_quiz.winners:
                chat_member_info = await bot.get_chat_member(saved_quiz.chat_id, winner)
                congrats_text.append(chat_member_info.user.get_mention(as_html=True))

            await bot.send_message(saved_quiz.chat_id, "Викторина закончена, всем спасибо! Вот наши победители:\n\n"
                                   + "\n".join(congrats_text), parse_mode="HTML")
            # Удаляем викторину из обоих наших "хранилищ"
            del quizzes_owners[active_quiz.id]
            del quizzes_database[quiz_owner][num]

@dp.message_handler(commands=['start'])
async def  cmd_start(message:types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        poll_keyboard.add(types.KeyboardButton(text="Создать викторину", request_poll = types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
        poll_keyboard.add(types.KeyboardButton(text="Отмена"))
        await message.answer ('Нажмите на кнопку ниже и создайте свою викторину', reply_markup=poll_keyboard)
    else:
        words = message.text.split()
        if len(words) == 1:
            bot_info = await bot.get_me()
            keyboard = types.InlineKeyboardMarkup()
            move_to_dm_button = types.InlineKeyboardButton(text='Перейти в ЛС -> t.me/Gunbooldre_bot')
            keyboard.add(move_to_dm_button)
        else:
            quiz_owner = quiz_owner.get(words[1])
            if not quiz_owner:
                await message.reply('Викторина удалена')
                return
            for saved_quiz in quizzes_database[quiz_owner]:
                if saved_quiz.quiz_id == words[1]:
                    msg = await bot.send_poll(chat_id = message.chat.id, question= saved_quiz.question,
                    is_anonymous=False, options = saved_quiz.options,type = 'quiz',
                    correct_ortion_id = saved_quiz.correct_ortion_id)
                    quizzes_owners[msg.poll.id] = quiz_owner
                    del quizzes_owners[words[1]]
                    saved_quiz.quiz_id = msg.poll.id
                    saved_quiz.chat_id = msg.chat.id
                    saved_quiz.message_id = msg.message.id

@dp.message_handler(lambda message:message.text == 'Отмена')
async def action_cancel(message:types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer('Действие отменено - Введите  /start , чтобы начать все заново', reply_markup = remove_keyboard)


@dp.message_handler(content_types=['poll'])
async def msg_with_poll(message:types.Message):
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []
    if message.poll.type != 'quiz':
        await message.reply('Извините викторина неактивна')
        return
    
    #Сохранение  викорины
    quizzes_database[str(message.from_user.id)].append(Quiz(
        quiz_id = message.poll.id,
        question = message.poll.question,
        options = [o.text for o in message.poll.options],
        correct_option_id = message.poll.correct_option_id,
        owner_id= message.from_user.id)
        )    
    
    quizzes_owners[message.poll.id] = str(message.from_user.id)

    await message.reply(f'Викторина сохранена общее число кол-во викторин: {len(quizzes_database[str(message.from_user.id)])}')


# quizes_databases ={} # Где будут хранятся данные по id  и по пользователю
# quizes_ownew     ={} # Где будут хранятся данные по id  и по викторине
# if not API_TOKEN:
#     exit("Error: Token is not valid")

# @dp.message_handler(commands=['quiz'])
# async def quiz(message:types.Message):
#     await bot.send_message(message.from_user.id,'Welcome to quiz {0.first_name}'.format(message.from_user),reply_markup=key.menu)

# @dp.message_handler(commands=['start'])
# async def start(message:types.Message):
#     try:
#         #if check(await bot.get_chat_member(chat_id= channel_id,user_id = message.from_user.id)):
#         await bot.send_message(message.from_user.id,'Welcome to aiogram {0.first_name}'.format(message.from_user),reply_markup=key.menu)
#        # else:
#            # await bot.send_message(message.from_user.id,not_sub,reply_markup=key.menu)
#     except:
#         await message.reply('BOT is not available please try again use this link -> t.me/Gunbooldre_bot.')

# @dp.message_handler(commands=['help'])
# async def help(message:types.Message):
#     try:
#         await bot.send_message(message.from_user.id,"""For now i got only one command and its ->  /start
#         soon we will got more""")
#     except:
#         await message.reply('BOT is not available please try again use this link -> t.me/Gunbooldre_bot.')

# @dp.message_handler(commands=['test'])
# async def testButton(message:types.Message):
#     await message.answer(
#         fmt.text(
#             fmt.text(fmt.text(fmt.hunderline("Python"),'The best language')),
#             fmt.text(fmt.text(fmt.hstrikethrough("JAVA"),'C language')),
#             fmt.text(fmt.text(fmt.hbold("C++"),'Hardest languages')),
#             sep='\n'
#         ),parse_mode = 'HTML'
#     )

# # def check(chat_member):
# #     print(chat_member['status'])
# #     if chat_member ['status'] != '0':
# #         return True
# #     else:
# #         return False


# @dp.message_handler()
# async def buttons(message:types.Message):
#     if message.text == 'Кинуть кость':
#         await message.answer_dice(emoji='🎲')
#     elif message.text == 'Тест':
#         await testButton(message)
#     elif message.text == 'Далее':
#         await bot.send_message(message.from_user.id,'You r going next page {0.first_name}'.format(message.from_user),reply_markup = key.secMenu)
#     elif message.text == 'Главное меню':
#         await bot.send_message(message.from_user.id,'You r going next page {0.first_name}'.format(message.from_user),reply_markup = key.menu)
#     elif message.text == 'Информация':
#             await message.answer(
#         fmt.text(
#             fmt.text(fmt.text(fmt.hunderline("Это НОВЫЙ-современный  Телеграм бот"))),
#             fmt.text(fmt.text(fmt.hitalic("Сам SpaceX профенансировало"))),
#             fmt.text(fmt.text(fmt.hbold("Сам Илон Маск нас поддерживает"))),
#             fmt.text(fmt.text(fmt.hstrikethrough("ТУТ МОГЛА БЫТЬ ВАША РЕКЛАМА"))),
#             sep='\n'
#         ),parse_mode = 'HTML'
#     )
#     elif message.text == 'Криповалюта':
#         await bot.send_message(message.from_user.id,'Выберите свою Крипту',reply_markup=key.cry_list)


# @dp.callback_query_handler(text_contains = 'cc_')
# async def cryptocurrency(call:types.CallbackQuery):
#     await bot.delete_message(call.from_user.id,call.message.message_id)
#     callback_data = call.data
#     currency = str(callback_data[3:])
#     res = cg.get_price(ids=currency,vs_currencies='usd')
#     await bot.send_message(call.from_user.id,f"Cryptocurrency is {currency} \n The price at the moment is {res[currency]['usd']}",reply_markup=key.cry_list)
    


# @dp.message_handler()
# async def get_message(message:types.Message):
# #     # bot_user = await bot.get_me()
# #     # print(f'Answer is ->{bot_user.username}')

# #     # chat_id = message.chat.id
# #     # text = "I love PYTHON"
# #     # send_message = await bot.send_message(chat_id = chat_id, text = text)
# #     # print(send_message.to_python)
#     await message.answer(message.text)
# #     #await message.reply(message.text)
# #     #await bot.send_message(message.from_user.id,message.text)

# #     # invite_link = await bot.export_chat_invite_link(chat_id=-661719527)
# #     # await bot.send_message(message.from_user.id,invite_link)

# #     # res = await bot.set_chat_title(chat_id=-1001734819966,title="HackerS")
# #     # print(res)   

#     if message.text == 'Hello':
#             await message.answer("Yeah hello my friend ")

# @dp.message_handler(content_types=ContentType.ANY)
# async def unknown_mess(message:types.Message):
#     text1 = text(emojize("Я не понимаю что это такое :new_moon_with_face:"),
#     bold("\n Я напоминаю"),"что есть команда  /help")
#     await message.reply(text1,parse_mode=ParseMode.MARKDOWN)
            
executor.start_polling(dp,skip_updates=True)