from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import filters
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *

# منوی اصلی با دکمه‌های فارسی
MAIN_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="👤 حساب من", callback_data="MyAccount")
    ],
    [
        InlineKeyboardButton(text="💎 خرید اشتراک", callback_data="BuySub")
    ],
    [
        InlineKeyboardButton(text="💰 قیمت‌ها", callback_data="Price"),
        InlineKeyboardButton(text="👛 کیف پول", callback_data="Wallet")
    ],
    [
        InlineKeyboardButton(text="🔄 کلون اکانت", callback_data="clone_account")
    ],
    [
        InlineKeyboardButton(text="❓ سوالات متداول", url="https://t.me/atrinmusic_tm"),
        InlineKeyboardButton(text="ℹ️ سلف چیست؟", callback_data="WhatSelf")
    ],
    [
        InlineKeyboardButton(text="📞 پشتیبانی", callback_data="Support")
    ]
])

PHONE_NUMBER_TEXT = """
**👋 سلام به ربات مدیریت سلف خوش آمدید!**

• با این ربات می‌توانید:
- اکانت خود را مدیریت کنید
- اشتراک تهیه کنید
- کلون اکانت بسازید
- از پشتیبانی کمک بگیرید

🔰 لطفا از منوی زیر گزینه مورد نظر خود را انتخاب کنید.
"""

@app.on_message(filters.user(OWNER_ID) & filters.command("start"))
async def start_command(client: app, message):
    await client.send_photo(
        message.chat.id,
        ALIVE_PIC,
        caption=PHONE_NUMBER_TEXT,
        reply_markup=MAIN_BUTTONS
    )

@app.on_callback_query()
async def callback_handlers(client: app, callback_query: CallbackQuery):
    if callback_query.data == "clone_account":
        await callback_query.message.edit_text(
            "**🔄 کلون اکانت**\n\n"
            "برای کلون کردن اکانت خود، لطفا string session خود را به صورت زیر ارسال کنید:\n"
            "`/clone YOUR_STRING_SESSION`\n\n"
            "⚠️ نکته: string session باید معتبر و مربوط به اکانت شما باشد.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
            ]])
        )
    
    elif callback_query.data == "back_to_main":
        await callback_query.message.edit_text(
            PHONE_NUMBER_TEXT,
            reply_markup=MAIN_BUTTONS
        )

@app.on_message(filters.user(OWNER_ID) & filters.command("clone"))
async def clone_command(bot: app, msg: Message):
    try:
        if len(msg.command) < 2:
            await msg.reply(
                "**⚠️ خطا در دستور**\n\n"
                "لطفا string session خود را همراه با دستور ارسال کنید:\n"
                "`/clone YOUR_STRING_SESSION`",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 برگشت به منو", callback_data="back_to_main")
                ]])
            )
            return

        session = msg.command[1]
        status_msg = await msg.reply("🔄 در حال راه‌اندازی کلاینت...")
        
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session,
            plugins=dict(root="Zaid/modules")
        )
        
        await client.start()
        user = await client.get_me()
        
        await status_msg.edit(
            f"✅ کلاینت شما با نام {user.first_name} با موفقیت راه‌اندازی شد!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 برگشت به منو", callback_data="back_to_main")
            ]])
        )
        
    except Exception as e:
        await msg.reply(
            f"**❌ خطا در راه‌اندازی کلاینت:**\n`{str(e)}`\n\n"
            "لطفا دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 برگشت به منو", callback_data="back_to_main")
            ]])
        )

# اضافه کردن سایر callback handlers برای دکمه‌های دیگر
@app.on_callback_query(filters.regex('^(MyAccount|BuySub|Price|Wallet|WhatSelf|Support)$'))
async def other_callbacks(client: app, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "MyAccount":
        text = "👤 **اطلاعات حساب شما**\n\nدر حال توسعه..."
    elif data == "BuySub":
        text = "💎 **خرید اشتراک**\n\nدر حال توسعه..."
    elif data == "Price":
        text = "💰 **لیست قیمت‌ها**\n\nدر حال توسعه..."
    elif data == "Wallet":
        text = "👛 **کیف پول**\n\nدر حال توسعه..."
    elif data == "WhatSelf":
        text = "ℹ️ **سلف چیست؟**\n\nدر حال توسعه..."
    elif data == "Support":
        text = "📞 **پشتیبانی**\n\nدر حال توسعه..."
    
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
        ]])
    )
