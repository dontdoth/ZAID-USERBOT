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
    "serif": {"0":"𝟬", "1":"𝟭", "2":"𝟮", "3":"𝟯", "4":"𝟰", "5":"𝟱", "6":"𝟲", "7":"𝟳", "8":"𝟴", "9":"𝟵", ":":":"},
    "script": {"0":"𝓪", "1":"𝓫", "2":"𝓬", "3":"𝓭", "4":"𝓮", "5":"𝓯", "6":"𝓰", "7":"𝓱", "8":"𝓲", "9":"𝓳", ":":"："},
    "blackboard": {"0":"𝕒", "1":"𝕓", "2":"𝕔", "3":"𝕕", "4":"𝕖", "5":"𝕗", "6":"𝕘", "7":"𝕙", "8":"𝕚", "9":"𝕛", ":":"："},
    "medieval": {"0":"𝖆", "1":"𝖇", "2":"𝖈", "3":"𝖉", "4":"𝖊", "5":"𝖋", "6":"𝖌", "7":"𝖍", "8":"𝖎", "9":"𝖏", ":":"："},
    "bubble": {"0":"ⓐ", "1":"ⓑ", "2":"ⓒ", "3":"ⓓ", "4":"ⓔ", "5":"ⓕ", "6":"ⓖ", "7":"ⓗ", "8":"ⓘ", "9":"ⓙ", ":":"："},
    "cursive": {"0":"𝒶", "1":"𝒷", "2":"𝒸", "3":"𝒹", "4":"𝑒", "5":"𝒻", "6":"𝑔", "7":"𝒽", "8":"𝒾", "9":"𝒿", ":":"："},
    "decorative": {"0":"𝔸", "1":"𝔹", "2":"ℂ", "3":"𝔻", "4":"𝔼", "5":"𝔽", "6":"𝔾", "7":"ℍ", "8":"𝕀", "9":"𝕁", ":":"："}
}

# طرح‌های مختلف برای نمایش ساعت
TIME_DESIGNS = {
    "simple": "{}",
    "brackets": "[{}]",
    "stars": "⭐{}⭐",
    "hearts": "❤️{}❤️",
    "arrows": "➤ {} ➤",
    "fancy_box": "┏━━━━━━━━┓\n┃   {}   ┃\n┗━━━━━━━━┛",
    "circle": "⭕️ {} ⭕️",
    "diamond": "💎 {} 💎",
    "fire": "🔥 {} 🔥",
    "crown": "👑 {} 👑",
    "leaves": "🍃 {} 🍃",
    "sparkles": "✨ {} ✨",
    "magic": "🌟 {} 🌟",
    "rainbow": "🌈 {} 🌈",
    "cloud": "☁️ {} ☁️",
    "moon": "🌙 {} 🌙"
}

async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None

async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason

async def extract_user(message):
    return (await extract_user_and_reason(message))[0]

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
            # استفاده از فونت‌های مختلف به صورت چرخشی
            font_types = list(FONTS.keys())
            design_types = list(TIME_DESIGNS.keys())
            current_font = font_types[int(time()) % len(font_types)]
            current_design = design_types[int(time()) % len(design_types)]
            time_str = await get_tehran_time(current_font, current_design)
            await client.update_profile(first_name=f"{name} | {time_str}")
        except Exception as e:
            print(f"خطا در بروزرسانی نام: {e}")
        await asyncio.sleep(60)

async def auto_update_bio(client):
    while time_bio:
        try:
            current_info = await client.get_chat(client.me.id)
            bio = current_info.bio.split('|')[0].strip()
            # استفاده از فونت‌های مختلف به صورت چرخشی
            font_types = list(FONTS.keys())
            design_types = list(TIME_DESIGNS.keys())
            current_font = font_types[int(time()) % len(font_types)]
            current_design = design_types[int(time()) % len(design_types)]
            time_str = await get_tehran_time(current_font, current_design)
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

@Client.on_message(
    filters.command(["block"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def block_user_func(client: Client, message: Message):
    user_id = await extract_user(message)
    tex = await message.reply_text("`در حال پردازش...`")
    if not user_id:
        return await message.edit(
            "برای بلاک کردن کاربر، شناسه یا نام کاربری او را وارد کنید یا روی پیام او ریپلای کنید."
        )
    if user_id == client.me.id:
        return await tex.edit("نمی‌توانید خودتان را بلاک کنید!")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await message.edit(f"**کاربر {umention} با موفقیت بلاک شد ✅**")

@Client.on_message(
    filters.command(["unblock"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def unblock_user_func(client: Client, message: Message):
    user_id = await extract_user(message)
    tex = await message.reply_text("`در حال پردازش...`")
    if not user_id:
        return await message.edit(
            "برای آنبلاک کردن کاربر، شناسه یا نام کاربری او را وارد کنید یا روی پیام او ریپلای کنید."
        )
    if user_id == client.me.id:
        return await tex.edit("نمی‌توانید خودتان را آنبلاک کنید!")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await message.edit(f"**کاربر {umention} با موفقیت آنبلاک شد ✅**")

@Client.on_message(
    filters.command(["setpfp"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def set_pfp(client: Client, message: Message):
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        await client.download_media(message=replied, file_name="profile_photo.jpg")
        await client.set_profile_photo(photo="profile_photo.jpg")
        if os.path.exists("profile_photo.jpg"):
            os.remove("profile_photo.jpg")
        await message.edit("**عکس پروفایل شما با موفقیت تغییر کرد ✅**")
    else:
        await message.edit(
            "برای تغییر عکس پروفایل، روی یک عکس ریپلای کنید."
        )
        await sleep(3)
        await message.delete()

@Client.on_message(
    filters.command(["vpfp"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def view_pfp(client: Client, message: Message):
    user_id = await extract_user(message)
    if user_id:
        user = await client.get_users(user_id)
    else:
        user = await client.get_me()
    if not user.photo:
        await message.edit("کاربر عکس پروفایل ندارد!")
        return
    await client.download_media(user.photo.big_file_id, file_name="profile_photo.jpg")
    await client.send_photo(
        message.chat.id, "profile_photo.jpg", reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
    if os.path.exists("profile_photo.jpg"):
        os.remove("profile_photo.jpg")

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
