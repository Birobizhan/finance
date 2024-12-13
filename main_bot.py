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
    webAppInfo: types.WebAppInfo = types.WebAppInfo(url='https://r2rhnqzl-3000.euw.devtunnels.ms/')
    button1 = InlineKeyboardButton(text='Приложение', web_app=webAppInfo)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])

    await message.answer('Привет, это бот для управления и подсчета финансов!\n'
                         'напиши /help, чтобы узнать функции бота', reply_markup=keyboard)


@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(
        'Перейди в приложение которое я присылал ранее, зарегистрируйся в нем и ты сможешь добавлять, удалять, '
        'изменять свои траты, а так же тебе будет представлена небольшая визуализация!')


@dp.message()
async def other_message(message: Message):
    await message.answer('Я таких команд не знаю, скорее переходи в приложение и регистрируйся!')


if __name__ == "__main__":
    dp.run_polling(bot)
