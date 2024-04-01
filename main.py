""""
Данный прелоадер нужен, чтобы собирать пользователей в бот, на стадии разработки бота
"""
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

import config

API_TOKEN = config.TOKEN_BOT
YOUR_CHANNEL_OWNER_ID = config.OWNER_ID  # Замените на ID владельца вашего канала

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создание базы данных SQLite и таблицы для хранения информации о пользователях
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        registration_date TEXT
    )
''')
conn.commit()


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
	"""
	Обработчик команды /start.
	Отправляет приветственное сообщение.
	"""
	# Запись информации о пользователе в базу данных
	user_id = message.from_user.id
	if message.from_user.id != YOUR_CHANNEL_OWNER_ID:
		username = message.from_user.username
		registration_date = message.date
		cursor.execute('INSERT INTO users (id, username, registration_date) VALUES (?, ?, ?)',
		               (user_id, username, registration_date))
		conn.commit()
	
	await message.answer(
		"Данный бот сейчас находится в разработке\n\n"
		"Планируемый запуск проекта 🎇 22 мая 2024 года 🎇🎉\n\n"
		"Вы можете пока подписаться на него, как только мы начнем тестировать его, мы оповестим вас\n"
		f"Если у вас есть вопросы или предложения, или Вам нужна разработка ботов вы можете связаться с [нами](tg://user?id={YOUR_CHANNEL_OWNER_ID})\n\n",
		parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=['users_bot'])
async def show_users(message: types.Message):
	"""
	Обработчик команды /users_bot.
	Выводит список всех пользователей из базы данных.
	"""
	# Проверка на ID владельца канала
	if message.from_user.id != YOUR_CHANNEL_OWNER_ID:
		await message.answer("Извините, у вас нет доступа к этой команде.")
		return
	
	cursor.execute('SELECT * FROM users')
	users = cursor.fetchall()
	if users:
		all_users = len(users)
		response = f"Список пользователей:\nВсего пользователей:     {all_users}\n"
		
		numbers = 0
		for user in users:
			numbers += 1
			response += f"\n№ {numbers} \nID:     {user[0]},\nUsername:      @{user[1]},\n" \
			            f"Registration Date:        {user[2]}\n"
	else:
		response = "Список пользователей пуст."
	await message.answer(response)


@dp.message_handler()
async def echo(message: types.Message):
	"""
	Обработчик всех остальных сообщений.
	Отправляет информацию о статусе разработки.
	"""
	
	# Запись информации о пользователе в базу данных
	user_id = message.from_user.id
	if message.from_user.id != YOUR_CHANNEL_OWNER_ID:
		username = message.from_user.username
		registration_date = message.date
		cursor.execute('INSERT INTO users (id, username, registration_date) VALUES (?, ?, ?)',
		               (user_id, username, registration_date))
		conn.commit()
		
	await message.answer(
		"Данный бот сейчас находится в разработке\n\n"
		"Планируемый запуск проекта 🎇 22 мая 2024 года 🎇🎉\n\n"
		"Вы можете пока подписаться на него, как только мы начнем тестировать его, мы оповестим вас\n"
		f"Если у вас есть вопросы или предложения, или Вам нужна разработка ботов вы можете связаться с [нами](tg://user?id={YOUR_CHANNEL_OWNER_ID})\n\n",
		parse_mode=types.ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
