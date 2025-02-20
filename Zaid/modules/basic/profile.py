import os
from asyncio import sleep
import sys
from re import sub
from time import time
from datetime import datetime
import pytz
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from Zaid import SUDO_USER
from Zaid.helper.PyroHelpers import ReplyCheck

from Zaid.modules.help import add_command_help

# تنظیمات گلوبال
time_name = False
time_bio = False

# فونت‌های متنوع برای ساعت
FONTS = {
    "normal": {"0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", ":":":"},
    "bold": {"0":"𝟎", "1":"𝟏", "2":"𝟐", "3":"𝟑", "4":"𝟒", "5":"𝟓", "6":"𝟔", "7":"𝟕", "8":"𝟖", "9":"𝟗", ":":":"},
    "fancy": {"0":"⓪", "1":"①", "2":"②", "3":"③", "4":"④", "5":"⑤", "6":"⑥", "7":"⑦", "8":"⑧", "9":"⑨", ":":"："},
    "square": {"0":"0️⃣", "1":"1️⃣", "2":"2️⃣", "3":"3️⃣", "4":"4️⃣", "5":"5️⃣", "6":"6️⃣", "7":"7️⃣", "8":"8️⃣", "9":"9️⃣", ":":"："},
    "double": {"0":"𝟘", "1":"𝟙", "2":"𝟚", "3":"𝟛", "4":"𝟜", "5":"𝟝", "6":"𝟞", "7":"𝟟", "8":"𝟠", "9":"𝟡", ":":":"},
}

# طرح‌های مختلف برای نمایش ساعت
TIME_DESIGNS = {
    "simple": "{}",
    "brackets": "[{}]",
    "stars": "⭐{}⭐",
    "hearts": "❤️{}❤️",
    "arrows": "➤ {} ➤",
    "fancy_box": "┏━━━━━━━━┓\n┃   {}   ┃\n┗━━━━━━━━┛",
}

def convert_to_font(text, font_type="normal"):
    if font_type not in FONTS:
        font_type = "normal"
    return "".join(FONTS[font_type].get(c, c) for c in text)

async def get_tehran_time(font_type="normal", design="simple"):
    tehran_tz = pytz.timezone('Asia/Tehran')
    tehran_time = datetime.now(tehran_tz).strftime("%H:%M")
    formatted_time = convert_to_font(tehran_time, font_type)
    return TIME_DESIGNS[design].format(formatted_time)

@Client.on_message(
    filters.command(["settime"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def set_time(client: Client, message: Message):
    global time_name
    if len(message.command) == 1:
        return await message.edit("استفاده: `.settime on/off`")
    
    status = message.command[1].lower()
    if status == "on":
        time_name = True
        await message.edit("**نمایش ساعت در نام فعال شد ✅**")
        asyncio.create_task(auto_update_name(client))
    elif status == "off":
        time_name = False
        await message.edit("**نمایش ساعت در نام غیرفعال شد ❌**")
    else:
        await message.edit("**دستور نامعتبر! از `on` یا `off` استفاده کنید**")

@Client.on_message(
    filters.command(["setbiotime"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def set_bio_time(client: Client, message: Message):
    global time_bio
    if len(message.command) == 1:
        return await message.edit("استفاده: `.setbiotime on/off`")
    
    status = message.command[1].lower()
    if status == "on":
        time_bio = True
        await message.edit("**نمایش ساعت در بیو فعال شد ✅**")
        asyncio.create_task(auto_update_bio(client))
    elif status == "off":
        time_bio = False
        await message.edit("**نمایش ساعت در بیو غیرفعال شد ❌**")
    else:
        await message.edit("**دستور نامعتبر! از `on` یا `off` استفاده کنید**")

async def auto_update_name(client):
    while time_name:
        try:
            current_info = await client.get_chat(client.me.id)
            name = current_info.first_name.split('|')[0].strip()
            time_str = await get_tehran_time("bold", "brackets")
            await client.update_profile(first_name=f"{name} | {time_str}")
        except Exception as e:
            print(f"خطا در بروزرسانی نام: {e}")
        await asyncio.sleep(60)

async def auto_update_bio(client):
    while time_bio:
        try:
            current_info = await client.get_chat(client.me.id)
            bio = current_info.bio.split('|')[0].strip()
            time_str = await get_tehran_time("fancy", "stars")
            await client.update_profile(bio=f"{bio} | {time_str}")
        except Exception as e:
            print(f"خطا در بروزرسانی بیو: {e}")
        await asyncio.sleep(60)

@Client.on_message(
    filters.command(["setname"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def setname(client: Client, message: Message):
    tex = await message.reply_text("در حال پردازش...")
    if len(message.command) == 1:
        return await tex.edit("لطفا متنی برای نام خود وارد کنید.")
    
    name = message.text.split(None, 1)[1]
    try:
        if time_name:
            time_str = await get_tehran_time("bold", "brackets")
            full_name = f"{name} | {time_str}"
        else:
            full_name = name
            
        await client.update_profile(first_name=full_name)
        await tex.edit(f"**نام شما با موفقیت به** `{full_name}` **تغییر کرد**")
    except Exception as e:
        await tex.edit(f"**خطا:** `{e}`")

@Client.on_message(
    filters.command(["setbio"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def set_bio(client: Client, message: Message):
    tex = await message.edit_text("در حال پردازش...")
    if len(message.command) == 1:
        return await tex.edit("لطفا متنی برای بیو وارد کنید.")
    
    bio = message.text.split(None, 1)[1]
    try:
        if time_bio:
            time_str = await get_tehran_time("fancy", "stars")
            full_bio = f"{bio} | {time_str}"
        else:
            full_bio = bio
            
        await client.update_profile(bio=full_bio)
        await tex.edit(f"**بیوگرافی شما با موفقیت به** `{full_bio}` **تغییر کرد**")
    except Exception as e:
        await tex.edit(f"**خطا:** `{e}`")

# سایر توابع بدون تغییر می‌مانند...

add_command_help(
    "پروفایل",
    [
        ["settime on/off", "فعال/غیرفعال کردن نمایش ساعت در نام"],
        ["setbiotime on/off", "فعال/غیرفعال کردن نمایش ساعت در بیو"],
        ["setname", "تنظیم نام پروفایل"],
        ["setbio", "تنظیم بیوگرافی"],
        ["block", "برای بلاک کردن کاربر"],
        ["unblock", "برای آنبلاک کردن کاربر"],
        ["setpfp", "تنظیم عکس پروفایل با ریپلای روی عکس"],
        ["vpfp", "نمایش عکس پروفایل کاربر"],
    ],
)
