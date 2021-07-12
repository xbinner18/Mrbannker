import logging
import os
import requests
import time

from aiogram import Bot, Dispatcher, executor, types

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
URL = os.environ.get("URL", None) 
PREFIX = "!/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def send_welcome(message: types.Message):
    await message.answer_chat_action("typing")
    await message.reply(
        "Hello how to use <code>/chk cc/mm/yy/cvv</code>"
    )
    
    
@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/chk '):]
    if not cc:
        return await message.reply(
            "<code>Send Card /chk cc|mm|yy|cvv.</code>"
        )   
    res = requests.get(
        f"{URL}/api.php/?lista={cc}"
    ).json()
    toc = time.perf_counter()
    INFO = f'''
<b>STRIPE AUTH</b>
CC ➟ <code>{cc}</code>
STATUS ➟ <b>{res["res"]}</b>
BRAND ➟ <b>{res["brand"]}</b>
BANK ➟ <b>{res["bank"]}</b>
COUNTRY ➟ <b>{res["country"]}</b>
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b> ➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
'''
    await message.reply(INFO)  
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
