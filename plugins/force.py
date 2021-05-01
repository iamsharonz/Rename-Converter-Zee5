import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
from pyrogram import filters
from pyrogram import Client
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel 
from helper_funcs.chat_base import TRChatBase


@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def text(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("You are Banned")
        return
    TRChatBase(update.from_user.id, update.text, "/echo")
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You are **B A N N E D**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            await update.reply_text(
                text="**Please Join My Update Channel Before Using Me..**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Support Channel', url='https://t.me/Nobodys_Bots'),
                    InlineKeyboardButton('Feedback', url='https://t.me/MrNobody_Here')
                ],
                [
                    InlineKeyboardButton('♐ SHARE ♐', url='http://t.me/share/url?url=Hey%20There%E2%9D%A4%EF%B8%8F%2C%0A%20%0A%20I%20Found%20A%20Really%20Awesome%20Bot%20%20For%20Renaming%20and%20Converting%20any%20telegram%20files%20with%20Permanent%20Thumbnail%20support.%20It%20can%20also%20upload%20from%20Zee5%20link.%20Hope%20This%20Bot%20Helps%20You%20Too.%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%E2%9D%A4%EF%B8%8F%0A%20%0A%20Bot%20Link%20%3A-%20%40SpeedyRenamer_Bot'),
                   
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
            return 
