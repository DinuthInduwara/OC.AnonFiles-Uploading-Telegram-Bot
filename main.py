import os
import time
import logging
import pyrogram
import aiohttp
import requests
import aiofiles
from random import randint
from progress import progress
from config import Config
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

DOWNLOAD = "./"


APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN

   
OC_AnonFilesBot = Client(
    "AnonFilesBot",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


START_TEXT = """
<b>Hey There,
I can upload any media files to __Anonfile.com__


🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️


Hit 'How To Use' button to find out more about how to use me</b>
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('How To Use', callback_data='help'),
        InlineKeyboardButton('Repo', url='https://github.com/DinuthInduwara/OC.AnonFiles-Uploading-Telegram-Bot'),
        InlineKeyboardButton('Github', url='https://github.com/DinuthInduwara/')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Repo', url='https://github.com/DinuthInduwara/OC.AnonFiles-Uploading-Telegram-Bot'),
        InlineKeyboardButton('Github', url='https://github.com/DinuthInduwara/')
        ]]
    )
HELP_TEXT = """
AnonFilesBot Help!

🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️

Send me any media file, I will upload it to anonfiles.com and give the download link
"""


@OC_AnonFilesBot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@OC_AnonFilesBot.on_message(filters.media & filters.private)
async def upload(client, message):
    m = await message.reply("𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒀𝒐𝒖𝒓 𝑭𝒊𝒍𝒆 𝑻𝒐 𝑴𝒚 𝑺𝒆𝒓𝒗𝒆𝒓...")
    now = time.time()
    sed = await OC_AnonFilesBot.download_media(
                message, DOWNLOAD,
          progress=progress,
          progress_args=(
            "**𝚄𝚙𝚕𝚘𝚊𝚍 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜 𝚂𝚝𝚊𝚛𝚝𝚎𝚍, 𝙿𝚕𝚎𝚊𝚜𝚎 𝚆𝚊𝚒𝚝 !**\n**𝕀ᴛ𝕤 𝕋ᴀᴋᴇ ᴛɪᴍᴇ 𝔸ᴄᴄᴏʀᴅɪɴɢ 𝕐ᴏᴜʀ 𝔽ɪʟᴇ𝕤 𝕊ɪᴢᴇ** \n\n**ᴇᴛᴀ:** ", 
            m,
            now
            )
        )
    try:
        files = {'file': open(sed, 'rb')}
        await m.edit("**𝕌𝕡𝕝𝕠𝕒𝕕𝕚𝕟𝕘 𝕋𝕠 𝔸𝕟𝕠𝕟𝔽𝕚𝕝𝕖𝕤! ℙ𝕝𝕖𝕒𝕤𝕖 𝕎𝕒𝕚𝕥**")
        callapi = requests.post("https://api.anonfiles.com/upload", files=files)
        text = callapi.json()
        output = f"""
<u>**🔅🎁🎁 𝓕𝓲𝓵𝓮 𝓤𝓹𝓵𝓸𝓪𝓭𝓮𝓭 𝓣𝓸 𝓐𝓷𝓸𝓷𝓕𝓲𝓵𝓮𝓼 🎁🎁**</u>

**📂 Fɪʟᴇ Nᴀᴍᴇ:** {text['data']['file']['metadata']['name']}

**📦 Fɪʟᴇ Sɪᴢᴇ:** {text['data']['file']['metadata']['size']['readable']}

**📥Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ:** `{text['data']['file']['url']['full']}`

🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️"""
        btn = InlineKeyboardMarkup(
                                [[InlineKeyboardButton("📥 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 📥", url=f"{text['data']['file']['url']['full']}")]])
        await m.edit(output, reply_markup=btn)
    except Exception:
        OC_AnonFilesBot.send_message(message.chat.id, text="Something Went Wrong!")
       
    os.remove(sed)



@OC_AnonFilesBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    else:
        await update.message.delete()

OC_AnonFilesBot.start()
print("""AnonFilesBot Is Started!

🌷 𝒟𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇 : ✍️✍️𝓞𝓹𝓮𝓷 𝓒𝓸𝓭𝓮 𝓓𝓮𝓿𝓼 ✍️✍️

Send me any media file, I will upload it to anonfiles.com and give the download link
""")
idle()
