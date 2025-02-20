import aiohttp
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.helper.basic import edit_or_reply
from Zaid.modules.help import *

# API های جایگزین رایگان
SEARCH_APIS = [
    "https://ddg-api.herokuapp.com/search",
    "https://api.duckduckgo.com",
    "https://serpapi.com/search.json",
    "https://api.searchapi.io/v1/search"
]

async def perform_search(query):
    """انجام جستجو با استفاده از API های مختلف"""
    async with aiohttp.ClientSession() as session:
        for api_url in SEARCH_APIS:
            try:
                params = {
                    'q': query,
                    'limit': 10,
                    'api_key': 'f3ccd2a0-d9b5-4393-8e42-e37b8c1d6b1c'  # API key رایگان
                }
                
                async with session.get(api_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
            except:
                continue
    return None

@Client.on_message(filters.command(["gs", "google", "جستجو"], ".") & filters.me)
async def google_search(client: Client, message: Message):
    msg = await edit_or_reply(message, "🔍 در حال جستجو...")
    
    # دریافت متن جستجو
    query = message.text.split(None, 1)
    if len(query) < 2:
        await msg.edit("❌ لطفا عبارت مورد نظر برای جستجو را وارد کنید\n\nمثال: `.جستجو پایتون چیست`")
        return
    
    search_query = query[1]
    await msg.edit(f"🔍 در حال جستجوی: **{search_query}**")

    try:
        results = await perform_search(search_query)
        
        if not results:
            await msg.edit("❌ نتیجه‌ای یافت نشد!")
            return

        response_text = f"🔍 نتایج جستجو برای: **{search_query}**\n\n"
        
        # پردازش نتایج بسته به نوع API
        if isinstance(results, list):
            search_results = results
        elif isinstance(results, dict):
            search_results = results.get('results', []) or results.get('items', []) or results.get('organic_results', [])
        else:
            search_results = []

        for i, result in enumerate(search_results[:10], 1):
            if isinstance(result, dict):
                title = result.get('title', 'بدون عنوان')
                link = result.get('link', result.get('url', ''))
                snippet = result.get('snippet', result.get('description', ''))
            else:
                continue

            response_text += f"**{i}. [{title}]({link})**\n"
            if snippet:
                response_text += f"💡 {snippet}\n"
            response_text += f"🔗 {link}\n\n"

        # تقسیم پیام‌های طولانی
        if len(response_text) > 4096:
            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk in chunks:
                await msg.reply_text(chunk)
            await msg.delete()
        else:
            await msg.edit(response_text)

    except Exception as e:
        await msg.edit(f"❌ خطا در جستجو: {str(e)}")

# جستجوی جایگزین با DuckDuckGo
async def duckduckgo_search(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('RelatedTopics', [])
    except:
        return []

add_command_help(
    "جستجو",
    [
        [
            "جستجو [متن]",
            "جستجو و نمایش نتایج با جزئیات",
        ],
        [
            "gs [متن]",
            "مشابه دستور جستجو",
        ],
        [
            "google [متن]",
            "مشابه دستور جستجو",
        ],
    ],
)
