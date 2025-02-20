import html
from pyrogram import Client, enums, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Zaid.helper.basic import edit_or_reply
from Zaid.helper.parser import mention_html, mention_markdown
from Zaid.modules.help import *

# دکمه‌های اینلاین برای منوی اصلی
main_buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("👥 ادمین‌ها", callback_data="admin_list"),
        InlineKeyboardButton("🤖 ربات‌ها", callback_data="bot_list")
    ],
    [
        InlineKeyboardButton("👤 منشن همه", callback_data="mention_all"),
        InlineKeyboardButton("🗑 حذف شده‌ها", callback_data="zombies")
    ],
    [
        InlineKeyboardButton("❌ بستن", callback_data="close_menu")
    ]
])

@Client.on_message(filters.me & filters.command(["admins", "adminlist"], "."))
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    
    creator = []
    admin = []
    badmin = []
    
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(mention_markdown(a.user.id, nama))
    
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    
    teks = f"**لیست ادمین‌های {grup.title}**\n\n"
    teks += "👑 سازنده:\n"
    for x in creator:
        teks += f"• {x}\n"
    teks += f"\n👤 {len(admin)} ادمین انسان:\n"
    for x in admin:
        teks += f"• {x}\n"
    teks += f"\n🤖 {len(badmin)} ربات ادمین:\n"
    for x in badmin:
        teks += f"• {x}\n"
    teks += f"\n📊 مجموع: {totaladmins} ادمین"

    back_button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 برگشت", callback_data="back_to_menu"),
        InlineKeyboardButton("❌ بستن", callback_data="close_menu")
    ]])
    
    await message.edit(teks, reply_markup=back_button)

@Client.on_callback_query()
async def button_callback(client, callback_query):
    data = callback_query.data
    
    if data == "admin_list":
        await adminlist(client, callback_query.message)
        
    elif data == "bot_list":
        chat = callback_query.message.chat.id
        grup = await client.get_chat(chat)
        getbots = client.get_chat_members(chat)
        bots = []
        async for a in getbots:
            if a.user.is_bot:
                try:
                    nama = a.user.first_name + " " + a.user.last_name
                except:
                    nama = a.user.first_name
                if nama is None:
                    nama = "☠️ Deleted account"
                bots.append(mention_markdown(a.user.id, nama))
        
        teks = f"**لیست ربات‌های {grup.title}**\n\n"
        for x in bots:
            teks += f"• {x}\n"
        teks += f"\n📊 مجموع: {len(bots)} ربات"
        
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_menu"),
            InlineKeyboardButton("❌ بستن", callback_data="close_menu")
        ]])
        
        await callback_query.edit_message_text(teks, reply_markup=back_button)
    
    elif data == "mention_all":
        text = "سلام به همه 👋\n"
        async for member in client.get_chat_members(callback_query.message.chat.id):
            if not member.user.is_bot:
                text += mention_html(member.user.id, "\u200b")
        
        back_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 برگشت", callback_data="back_to_menu"),
            InlineKeyboardButton("❌ بستن", callback_data="close_menu")
        ]])
        
        await callback_query.edit_message_text(text, reply_markup=back_button)
    
    elif data == "back_to_menu":
        await callback_query.edit_message_text(
            "**منوی مدیریت گروه**\n\nلطفا یکی از گزینه‌ها را انتخاب کنید:",
            reply_markup=main_buttons
        )
    
    elif data == "close_menu":
        await callback_query.message.delete()

# اضافه کردن دستور جدید برای نمایش منو
@Client.on_message(filters.me & filters.command(["groupmenu", "gmenu"], "."))
async def group_menu(client: Client, message: Message):
    await message.edit(
        "**منوی مدیریت گروه**\n\nلطفا یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=main_buttons
    )

add_command_help(
    "tag",
    [
        [".gmenu", "نمایش منوی مدیریت گروه با دکمه"],
        [".admins", "نمایش لیست ادمین‌ها"],
        [".botlist", "نمایش لیست ربات‌ها"],
        [".everyone", "منشن کردن همه اعضا"],
    ],
)
