#bibleoteki
import asyncio
from aiogram import types, Dispatcher, executor, Bot
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import tok
import datetime
import sqlite3
import random
from random import randint
import time
from time import sleep
from base import *
#storage state
storage = MemoryStorage()
#sqlite3 connection
db = sqlite3.connect('database.db', check_same_thread=False)
sql = db.cursor()
#bot connection telegram_api
bot = Bot(token=tok)
dp = Dispatcher(bot, storage=storage)

admin = 1689403986

class UserState(StatesGroup):
	users = State()

class AdminState(StatesGroup):
	admins = State()
	bans = State()
	unban = State()
	analitic = State()

def create_users(user_id: int, name: str, ids: int):
	sql.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
	if sql.fetchone() is None:
		sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, 0, 0, 0, 0, name, ids))
		db.commit()

def proverka(user_id: int, text: str):
	global a
	try:
		a = 0
		for ids in sql.execute(f"SELECT ids FROM users WHERE ids = '{text}'").fetchone():
			text = text
			if ids == text:
				print('money ok')
			else:
				a += 1
				print('money no')
				pass
			return a
	except Exception as e:
		pass

def user_info(user_id: int):
	global name,ban,admin,user,exit_bot,ids
	name = sql.execute(f"SELECT name FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	ban = sql.execute(f"SELECT ban FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	admin = sql.execute(f"SELECT admin FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	user = sql.execute(f"SELECT user FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	exit_bot = sql.execute(f"SELECT exit_bot FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	ids = sql.execute(f"SELECT ids FROM users WHERE user_id = '{user_id}'").fetchone()[0]
	db.commit()
	return name,ban,admin,user,exit_bot,ids

def участники(user_id: int):
	global text
	sql.execute(f"SELECT user_id, ids FROM users ORDER BY ids")
	data = sql.fetchall()
	text = f"Участники:\n"
	for value, item in enumerate(data):
		print(item[0], item[1])
		value += 1
		sql.execute(f"SELECT name FROM users WHERE user_id = '{item[0]}'")
		if value <= 10:
			text += f"{value}) {sql.fetchall()[0][0]}\n"
		elif value > 10:
			pass
	return text
	print(text)

@dp.message_handler(commands=['start'], state=None)
async def starting(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	name = msg.from_user.first_name
	ids = randint(1, 9999)
	create_users(user_id=user_id, name=name, ids=ids)
	user_info(user_id=user_id)
	if user_id == admin:
		sql.execute(f"UPDATE users SET admin == '{admin}' WHERE user_id = '{user_id}'")
		db.commit()
		await msg.answer('Приветствую тебя админ вот команды которые я могу делать для тебя:\n /ban - заблокировать пользователя\n/unban - разблокировать пользователя\n/analitic - Статистика чата\n/offline_bot - Выйду из данного чата')
		await AdminState.admins.set()
		print(f"Имя: {name}\nID_tg: {user_id}\nID_user: {ids}")
	else:
		await msg.answer('Приветствую тебя человек вот какие команды я могу выполнить для тебя:\n /analitic')
		await UserState.users.set()
		print(f"Имя: {name}\nID_tg: {user_id}\nID_user: {ids}")

@dp.message_handler(content_types=['text'], state=UserState.users)
async def user_handler(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	user_info(user_id=user_id)
	if ban == 0:
		if msg.text.lower() == '/analitic':
			await msg.answer('то то то то то то то то то то то')
	else:
		pass

@dp.message_handler(content_types=['text'], state=AdminState.admins)
async def admin_handler(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	user_info(user_id=user_id)
	if exit_bot == 0:
		if ban == 0:
			if msg.text.lower() == '/ban':
				await msg.answer('Пришли мне id профиля того кого хочешь забанить')
				await AdminState.bans.set()
			if msg.text.lower() == '/unban':
				await msg.answer('Пришли мне id профиля того кого хочешь разбанить')
				await AdminState.unban.set()
			if msg.text.lower() == '/analitic':
				участники(user_id=user_id)
				ad = sql.execute(f"SELECT name FROM users WHERE user_id = '{admin}'").fetchone()[0]
				db.commit()
				await msg.answer(f'{text}\nАдмины:\n1) {ad}')
			if msg.text.lower() == '/offline_bot':
				group_id = -143718357518
				await msg.answer('Бот выключен или удален')
				await bot.kick_chat_member(chat_id=group_id, user_id=user_id)
		else:
			pass
	else:
		pass

@dp.message_handler(content_types=['text'], state=AdminState.bans)
async def bans(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	text = msg.text
	proverka(user_id=user_id, text=text)
	user_info(user_id=user_id)
	if a == 1:
		имя = sql.execute(f"SELECT name FROM users WHERE ids = '{text}'").fetchone()[0]
		db.commit()
		await msg.answer(f'Успешный бан {имя}')
		user_ban = sql.execute(f"SELECT user_id FROM users WHERE ids = '{text}'").fetchone()[0]
		db.commit()
		print(user_ban)
		sql.execute(f"UPDATE users SET ban == {1} WHERE user_id = '{user_ban}'")
		db.commit()
		print(ids)
		await AdminState.admins.set()
	elif a == 0:
		await msg.answer('Увы бан не сработал...\nПопробуйте ещё раз')
		print(ids)

@dp.message_handler(content_types=['text'], state=AdminState.unban)
async def unban(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	text = msg.text
	proverka(user_id=user_id, text=text)
	user_info(user_id=user_id)
	if a == 1:
		имя = sql.execute(f"SELECT name FROM users WHERE ids = '{text}'").fetchone()[0]
		db.commit()
		await msg.answer(f'Успешный разбан {имя}')
		user_ban = sql.execute(f"SELECT user_id FROM users WHERE ids = '{text}'").fetchone()[0]
		db.commit()
		sql.execute(f"UPDATE users SET ban == {0} WHERE user_id = '{user_ban}'")
		db.commit()
		await AdminState.admins.set()
	elif a == 0:
		await msg.answer('Увы такого пользователя нет в базе забаненых...\nПопробуйте ещё раз')

@dp.message_handler(content_types=['text'], state=AdminState.analitic)
async def analitic(msg: types.Message, state: FSMContext):
	user_id = msg.from_user.id
	user_info(user_id=user_id)


executor.start_polling(dp, skip_updates=True)
