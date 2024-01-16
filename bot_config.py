from decouple import config

from aiogram import Bot

bot = Bot(config("TOKEN"), parse_mode="HTML")

