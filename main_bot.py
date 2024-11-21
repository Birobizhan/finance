from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import F
from environs import Env

env = Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    webAppInfo: types.WebAppInfo = types.WebAppInfo(url='https://pro.guap.ru')
    button1 = InlineKeyboardButton(text='Приложение', web_app=webAppInfo)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])

    await message.answer('Привет, это бот для управления и подсчета финансов!\n'
                         'напиши /help, чтобы узнать функции бота', reply_markup=keyboard)


@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Пока такой функции не добавили')


@dp.message(F.text.lower().in_(['menu', 'меню', '/menu']))
async def menu(message: Message):
    button1 = KeyboardButton(text='Пока что пусто')
    button2 = KeyboardButton(text='И тут пусто')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button1, button2]])
    await message.answer(text='Вот меню', reply_markup=keyboard)


@dp.message()
async def other_message(message: Message):
    await message.answer('Я таких команд не знаю')


if __name__ == "__main__":
    dp.run_polling(bot)
