import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token='5384310724:AAFtbJZ1ppL2EWTR96Tpib46WNnL7i-HdY0')
dp = Dispatcher(bot)


@dp.message_handler()
async def all_messages(message: types.Message):
    
    endpoint = 'http://127.0.0.1:8000/api/answer/'
    
    
    requested_data = requests.post(endpoint, data = {'text':message.text})
    
    
    # @# - is for new line
    obtained_text = requested_data.text.replace('\n', '@#').replace('@#', '\n').replace('"', '')
    

    
    if obtained_text:
        print(obtained_text)
        await message.reply(obtained_text)
        
    
    
    
executor.start_polling(dp)