from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import filters
import os
import asyncio
from pyrogram import *
from pyrogram.types import *

# تنظیم لینک‌های کانال و گروه
SUPPORT_GROUP = "https://t.me/atrinmusic_tm1"
CHANNEL_LINK = "https://t.me/atrinmusic_tm"

# منوی اصلی
MAIN_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="👤 حساب من", callback_data="account_menu")
    ],
    [
        InlineKeyboardButton(text="💎 خرید اشتراک", callback_data="buy_menu")
    ],
    [
        InlineKeyboardButton(text="💰 قیمت‌ها", callback_data="price_menu"),
        InlineKeyboardButton(text="👛 کیف پول", callback_data="wallet_menu")
    ],
    [
        InlineKeyboardButton(text="🔄 ساخت سلف", callback_data="clone_menu")
    ],
    [
        InlineKeyboardButton(text="❓ سوالات متداول", url=CHANNEL_LINK),
        InlineKeyboardButton(text="📞 پشتیبانی", url=SUPPORT_GROUP)
    ]
])

# متن شروع
START_TEXT = """
**👋 سلام به ربات مدیریت سلف خوش آمدید!**

• با این ربات می‌توانید:
- اکانت خود را مدیریت کنید
- اشتراک تهیه کنید
- سلف بسازید
- از پشتیبانی کمک بگیرید

🔰 لطفا از منوی زیر گزینه مورد نظر خود را انتخاب کنید.
"""

# متن منوی کلون
CLONE_TEXT = """
**🔄 ساخت سلف**

برای ساخت سلف، مراحل زیر را انجام دهید:

1️⃣ ابتدا استرینگ سشن خود را از @StringSessionBot دریافت کنید

2️⃣ سپس استرینگ سشن را با دستور زیر ارسال کنید:
`/clone YOUR_STRING_SESSION`

⚠️ نکته: استرینگ سشن باید معتبر و مربوط به اکانت شما باشد.
"""

# متن منوی قیمت
PRICE_TEXT = """
**💰 تعرفه‌های اشتراک سلف**

⭐️ اشتراک 1 ماهه: 50,000 تومان
⭐️ اشتراک 3 ماهه: 140,000 تومان
⭐️ اشتراک 6 ماهه: 260,000 تومان
⭐️ اشتراک نامحدود: 500,000 تومان

برای خرید از دکمه "خرید اشتراک" استفاده کنید.
"""

@app.on_message(filters.user(OWNER_ID) & filters.command("start"))
async def start_command(client: app, message):
    await client.send_photo(
        message.chat.id,
        ALIVE_PIC,
        caption=START_TEXT,
        reply_markup=MAIN_BUTTONS
    )

@app.on_callback_query()
async def callback_handlers(client: app, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "clone_menu":
        await callback_query.message.edit_text(
            CLONE_TEXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
            ]])
        )
    
    elif data == "price_menu":
        await callback_query.message.edit_text(
            PRICE_TEXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💎 خرید اشتراک", callback_data="buy_menu"),
                InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
            ]])
        )
    
    elif data == "account_menu":
        user_id = callback_query.from_user.id
        await callback_query.message.edit_text(
            f"**👤 اطلاعات حساب کاربری**\n\n"
            f"🆔 شناسه کاربری: `{user_id}`\n"
            f"⭐️ نوع اشتراک: رایگان\n"
            f"⏰ زمان باقیمانده: 0 روز\n\n"
            "برای ارتقا حساب، از بخش خرید اشتراک اقدام کنید.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💎 خرید اشتراک", callback_data="buy_menu"),
                InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
            ]])
        )
    
    elif data == "buy_menu":
        await callback_query.message.edit_text(
            "**💎 خرید اشتراک**\n\n"
            "برای خرید اشتراک، لطفا یکی از روش‌های زیر را انتخاب کنید:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 پرداخت مستقیم", callback_data="direct_pay")],
                [InlineKeyboardButton("👛 پرداخت با کیف پول", callback_data="wallet_pay")],
                [InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")]
            ])
        )
    
    elif data == "wallet_menu":
        await callback_query.message.edit_text(
            "**👛 کیف پول**\n\n"
            "💰 موجودی فعلی: 0 تومان\n\n"
            "برای شارژ کیف پول از دکمه زیر استفاده کنید:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 شارژ کیف پول", callback_data="charge_wallet")],
                [InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")]
            ])
        )
    
    elif data == "back_to_main":
        await callback_query.message.edit_text(
            START_TEXT,
            reply_markup=MAIN_BUTTONS
        )

@app.on_message(filters.user(OWNER_ID) & filters.command("clone"))
async def clone_command(bot: app, msg: Message):
    try:
        if len(msg.command) < 2:
            await msg.reply(
                "**⚠️ خطا در دستور**\n\n"
                "لطفا استرینگ سشن خود را همراه با دستور ارسال کنید:\n"
                "`/clone YOUR_STRING_SESSION`",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 برگشت به منو", callback_data="back_to_main")
                ]])
            )
            return

        session = msg.command[1]
        status_msg = await msg.reply("🔄 در حال ساخت سلف...")
        
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
            f"✅ سلف شما با نام {user.first_name} با موفقیت ساخته شد!\n\n"
            "🔰 برای دریافت راهنمای دستورات از /help استفاده کنید.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 برگشت به منو", callback_data="back_to_main")
            ]])
        )
        
    except Exception as e:
        await msg.reply(
            f"**❌ خطا در ساخت سلف:**\n`{str(e)}`\n\n"
            "لطفا از استرینگ سشن معتبر استفاده کنید یا با پشتیبانی تماس بگیرید.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📞 پشتیبانی", url=SUPPORT_GROUP),
                InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")
            ]])
        )
