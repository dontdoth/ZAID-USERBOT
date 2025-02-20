from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import datetime
import random
import json
import os
from typing import Optional
from Zaid import app

# فونت‌های یونیکد
FONTS = {
    'serif': {
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢',
        'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫',
        's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    },
    'bold': {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶',
        'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿',
        's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    },
    'fancy': {
        'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲',
        'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻',
        's': '𝓼', 't': '𝓽', 'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    },
    'double': {
        'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚',
        'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣',
        's': '𝕤', 't': '𝕥', 'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫',
        '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜', '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡'
    }
}
# طرح‌های زمان، نام و بیو
TIME_DESIGNS = [
    "⌚️ {time}",
    "🕐 {time}",
    "⏰ {time} ⌛️",
    "◄ {time} ►",
    "✧ {time} ✧",
    "⟦ {time} ⟧",
    "『 {time} 』",
    "〖 {time} 〗",
    "【 {time} 】",
    "❰ {time} ❱",
    "⦗ {time} ⦘",
    "⎨ {time} ⎬",
    "⚡️ {time} ⚡️",
    "✺ {time} ✺",
    "❈ {time} ❈",
]

NAME_PATTERNS = [
    "{name} | {time}",
    "⟨ {name} ⟩ {time}",
    "✧ {name} ✧ {time}",
    "⎯⎯ {name} ⎯⎯ {time}",
    "✿ {name} ✿ {time}",
    "⚡️ {name} ⚡️ {time}",
    "☆ {name} ☆ {time}",
    "✵ {name} ✵ {time}",
    "⪼ {name} ⪻ {time}",
    "❥ {name} ❥ {time}",
    "◈ {name} ◈ {time}",
    "❖ {name} ❖ {time}",
    "✾ {name} ✾ {time}",
]

BIO_PATTERNS = [
    "{bio} | {time}",
    "✎ {bio} ⌚️ {time}",
    "➺ {bio} ⏰ {time}",
    "❈ {bio} ❈ {time}",
    "✧ {bio} ✧ {time}",
    "⚜️ {bio} ⚜️ {time}",
    "✴️ {bio} ✴️ {time}",
    "⟣ {bio} ⟢ {time}",
    "⚡️ {bio} ⚡️ {time}",
    "✺ {bio} ✺ {time}",
    "❋ {bio} ❋ {time}",
]

# ایموجی‌های تصادفی
RANDOM_EMOJIS = ["⚡️", "✨", "💫", "🌟", "⭐️", "🌙", "☀️", "🌈", "🔥", "💥"]

class ProfileManager:
    def __init__(self):
        self.name_time_enabled = False
        self.bio_time_enabled = False
        self.current_font = "serif"
        self.current_time_design = 0
        self.current_name_pattern = 0
        self.current_bio_pattern = 0
        self.original_name = ""
        self.original_bio = ""
        self.auto_name_change = False
        self.auto_bio_change = False
        self.name_change_interval = 300
        self.bio_change_interval = 600
        self.emoji_enabled = True
        self.load_config()

    def save_config(self):
        config = {
            "name_time_enabled": self.name_time_enabled,
            "bio_time_enabled": self.bio_time_enabled,
            "current_font": self.current_font,
            "current_time_design": self.current_time_design,
            "current_name_pattern": self.current_name_pattern,
            "current_bio_pattern": self.current_bio_pattern,
            "original_name": self.original_name,
            "original_bio": self.original_bio,
            "auto_name_change": self.auto_name_change,
            "auto_bio_change": self.auto_bio_change,
            "name_change_interval": self.name_change_interval,
            "bio_change_interval": self.bio_change_interval,
            "emoji_enabled": self.emoji_enabled
        }
        with open("profile_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def load_config(self):
        try:
            with open("profile_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                self.__dict__.update(config)
        except FileNotFoundError:
            self.save_config()
class ProfileAnimator:
    def __init__(self, manager: ProfileManager):
        self.manager = manager
        self.animation_tasks = set()

    async def animate_name(self):
        """انیمیشن نام"""
        while self.manager.auto_name_change:
            try:
                emoji = random.choice(RANDOM_EMOJIS) if self.manager.emoji_enabled else ""
                pattern = random.choice(NAME_PATTERNS)
                font = random.choice(list(FONTS.keys()))
                
                current_time = datetime.datetime.now().strftime("%H:%M")
                styled_name = self.apply_font(self.manager.original_name, font)
                new_name = pattern.format(name=styled_name, time=current_time) + emoji
                
                await app.update_profile(first_name=new_name)
                await asyncio.sleep(self.manager.name_change_interval)
            except Exception as e:
                print(f"خطا در انیمیشن نام: {e}")
                break

    async def animate_bio(self):
        """انیمیشن بیو"""
        while self.manager.auto_bio_change:
            try:
                emoji = random.choice(RANDOM_EMOJIS) if self.manager.emoji_enabled else ""
                pattern = random.choice(BIO_PATTERNS)
                
                current_time = datetime.datetime.now().strftime("%H:%M")
                new_bio = pattern.format(bio=self.manager.original_bio, time=current_time) + emoji
                
                await app.update_profile(bio=new_bio)
                await asyncio.sleep(self.manager.bio_change_interval)
            except Exception as e:
                print(f"خطا در انیمیشن بیو: {e}")
                break

    @staticmethod
    def apply_font(text: str, font_name: str) -> str:
        """اعمال فونت روی متن"""
        if font_name not in FONTS:
            return text
        
        result = ""
        for char in text.lower():
            if char in FONTS[font_name]:
                result += FONTS[font_name][char]
            else:
                result += char
        return result

# ایجاد نمونه از کلاس‌ها
profile_manager = ProfileManager()
profile_animator = ProfileAnimator(profile_manager)

# Commands handlers
@app.on_message(filters.command(["setname", "نام"], ".") & filters.me)
async def set_name_command(client: Client, message: Message):
    """تنظیم نام"""
    if len(message.command) < 2:
        await message.edit("**راهنما:** `.نام متن_مورد_نظر`")
        return
    
    profile_manager.original_name = " ".join(message.command[1:])
    styled_name = profile_animator.apply_font(profile_manager.original_name, profile_manager.current_font)
    
    try:
        await app.update_profile(first_name=styled_name)
        await message.edit(f"**✅ نام با موفقیت به `{styled_name}` تغییر کرد**")
        profile_manager.save_config()
    except Exception as e:
        await message.edit(f"**❌ خطا در تغییر نام: {str(e)}**")
@app.on_message(filters.command(["setbio", "بیو"], ".") & filters.me)
async def set_bio_command(client: Client, message: Message):
    """تنظیم بیو"""
    if len(message.command) < 2:
        await message.edit("**راهنما:** `.بیو متن_مورد_نظر`")
        return
    
    profile_manager.original_bio = " ".join(message.command[1:])
    
    try:
        await app.update_profile(bio=profile_manager.original_bio)
        await message.edit(f"**✅ بیو با موفقیت به `{profile_manager.original_bio}` تغییر کرد**")
        profile_manager.save_config()
    except Exception as e:
        await message.edit(f"**❌ خطا در تغییر بیو: {str(e)}**")

@app.on_message(filters.command(["autoname", "نام_خودکار"], ".") & filters.me)
async def auto_name_command(client: Client, message: Message):
    """فعال/غیرفعال کردن تغییر نام خودکار"""
    profile_manager.auto_name_change = not profile_manager.auto_name_change
    
    if profile_manager.auto_name_change:
        await message.edit("**✅ تغییر نام خودکار فعال شد**")
        asyncio.create_task(profile_animator.animate_name())
    else:
        await message.edit("**❌ تغییر نام خودکار غیرفعال شد**")
    
    profile_manager.save_config()

@app.on_message(filters.command(["autobio", "بیو_خودکار"], ".") & filters.me)
async def auto_bio_command(client: Client, message: Message):
    """فعال/غیرفعال کردن تغییر بیو خودکار"""
    profile_manager.auto_bio_change = not profile_manager.auto_bio_change
    
    if profile_manager.auto_bio_change:
        await message.edit("**✅ تغییر بیو خودکار فعال شد**")
        asyncio.create_task(profile_animator.animate_bio())
    else:
        await message.edit("**❌ تغییر بیو خودکار غیرفعال شد**")
    
    profile_manager.save_config()

@app.on_message(filters.command(["font", "فونت"], ".") & filters.me)
async def font_command(client: Client, message: Message):
    """تغییر فونت"""
    if len(message.command) < 2:
        available_fonts = ", ".join(FONTS.keys())
        await message.edit(f"**فونت‌های موجود:** `{available_fonts}`\n**راهنما:** `.فونت نام_فونت`")
        return
    
    font_name = message.command[1].lower()
    if font_name not in FONTS:
        await message.edit("**❌ فونت نامعتبر است**")
        return
    
    profile_manager.current_font = font_name
    profile_manager.save_config()
    await message.edit(f"**✅ فونت به `{font_name}` تغییر کرد**")

@app.on_message(filters.command(["emoji", "ایموجی"], ".") & filters.me)
async def emoji_command(client: Client, message: Message):
    """فعال/غیرفعال کردن ایموجی‌های تصادفی"""
    profile_manager.emoji_enabled = not profile_manager.emoji_enabled
    profile_manager.save_config()
    
    status = "فعال" if profile_manager.emoji_enabled else "غیرفعال"
    await message.edit(f"**✅ ایموجی‌های تصادفی {status} شد**")

@app.on_message(filters.command(["interval", "فاصله"], ".") & filters.me)
async def interval_command(client: Client, message: Message):
    """تنظیم فاصله زمانی تغییرات"""
    if len(message.command) < 3:
        await message.edit("**راهنما:** `.فاصله [name/bio] [زمان_به_ثانیه]`")
        return
    
    try:
        interval = int(message.command[2])
        if interval < 30:
            await message.edit("**❌ فاصله زمانی نباید کمتر از 30 ثانیه باشد**")
            return
        
        if message.command[1].lower() in ["name", "نام"]:
            profile_manager.name_change_interval = interval
            await message.edit(f"**✅ فاصله زمانی تغییر نام به `{interval}` ثانیه تنظیم شد**")
        elif message.command[1].lower() in ["bio", "بیو"]:
            profile_manager.bio_change_interval = interval
            await message.edit(f"**✅ فاصله زمانی تغییر بیو به `{interval}` ثانیه تنظیم شد**")
        else:
            await message.edit("**❌ نوع نامعتبر. از `name` یا `bio` استفاده کنید**")
            return
        
        profile_manager.save_config()
    except ValueError:
        await message.edit("**❌ لطفا یک عدد معتبر وارد کنید**")

@app.on_message(filters.command(["help", "راهنما"], ".") & filters.me)
async def help_command(client: Client, message: Message):
    """نمایش راهنما"""
    help_text = """
**🔰 راهنمای دستورات پروفایل:**

• `.نام` متن - تنظیم نام
• `.بیو` متن - تنظیم بیو
• `.نام_خودکار` - تغییر خودکار نام
• `.بیو_خودکار` - تغییر خودکار بیو
• `.فونت` نام_فونت - تغییر فونت
• `.ایموجی` - فعال/غیرفعال کردن ایموجی
• `.فاصله [name/bio] زمان` - تنظیم فاصله زمانی

**فونت‌های موجود:** `serif`, `bold`, `fancy`, `double`
"""
    await message.edit(help_text)                    
