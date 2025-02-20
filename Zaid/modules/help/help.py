import asyncio
from prettytable import PrettyTable
from pyrogram import Client, enums, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Zaid import app, CMD_HELP
from Zaid.helper.PyroHelpers import ReplyCheck
from Zaid.helper.utility import split_list

# دکمه‌های اینلاین
help_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("👤 دستورات کاربری", callback_data="user_cmds"),
        InlineKeyboardButton("⚙️ دستورات ادمین", callback_data="admin_cmds")
    ],
    [
        InlineKeyboardButton("🛠 ابزارها", callback_data="tools_cmds"),
        InlineKeyboardButton("🎵 موزیک", callback_data="music_cmds")
    ],
    [
        InlineKeyboardButton("بستن ✖️", callback_data="close_help")
    ]
])

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    xyz = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await xyz(*args, **kwargs)

@Client.on_message(filters.command(["help", "helpme"], ".") & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    bot_username = (await app.get_me()).username
    
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif not message.reply_to_message and len(cmd) == 1:
        help_text = "**🤖 راهنمای دستورات ZAID USERBOT**\n\n"
        help_text += "لطفا یکی از بخش‌های زیر را انتخاب کنید:"
        
        await message.edit(help_text, reply_markup=help_buttons)
        return

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"──「 **Help For {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `.{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "© @TG_GP_IRAN"
            await edit_or_reply(
                message, this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **Not a Valid Module Name.**",
            )

@Client.on_callback_query()
async def help_button_callback(client, callback_query):
    data = callback_query.data
    
    if data == "user_cmds":
        text = """
**👤 دستورات کاربری:**
• `.start` - شروع ربات
• `.ping` - تست آنلاین بودن
• `.info` - اطلاعات کاربر
• `.id` - دریافت آیدی
"""
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_help")
        ]])
        await callback_query.edit_message_text(text, reply_markup=back_button)

    elif data == "admin_cmds":
        text = """
**⚙️ دستورات ادمین:**
• `.ban` - مسدود کردن کاربر
• `.unban` - رفع مسدودیت
• `.mute` - سکوت کاربر
• `.unmute` - رفع سکوت
"""
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_help")
        ]])
        await callback_query.edit_message_text(text, reply_markup=back_button)

    elif data == "tools_cmds":
        text = """
**🛠 ابزارها:**
• `.weather` - آب و هوا
• `.tr` - ترجمه متن
• `.tts` - تبدیل متن به گفتار
• `.paste` - اشتراک کد
"""
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_help")
        ]])
        await callback_query.edit_message_text(text, reply_markup=back_button)

    elif data == "music_cmds":
        text = """
**🎵 دستورات موزیک:**
• `.play` - پخش موزیک
• `.skip` - رد کردن
• `.pause` - توقف موقت
• `.resume` - ادامه پخش
"""
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_help")
        ]])
        await callback_query.edit_message_text(text, reply_markup=back_button)

    elif data == "back_to_help":
        help_text = "**🤖 راهنمای دستورات ZAID USERBOT**\n\n"
        help_text += "لطفا یکی از بخش‌های زیر را انتخاب کنید:"
        await callback_query.edit_message_text(help_text, reply_markup=help_buttons)

    elif data == "close_help":
        await callback_query.message.delete()

def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict
