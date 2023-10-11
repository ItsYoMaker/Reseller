import asyncio
import logging
import re

from aiogram import types, exceptions

import requests
from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup

import config
import dbmanager
from bot import bot
#навалил говнокода


previous_names = {url: None for url in dbmanager.get_list_of_urls()}


async def get_page_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()


async def check_for_changes(url):
    try:
        page_content = await get_page_content(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        for section in soup.find_all("section"):
            vip_link = section.find('a', class_=re.compile(r'^styles_polepos'))
            if vip_link:
                continue
            else:
                name = section.find('h3', class_=re.compile(r'^styles_title')).text
                break

        if name != previous_names.get(url):
            for section in soup.find_all("section"):
                vip_link = section.find('a', class_=re.compile(r'^styles_polepos'))
                if vip_link:
                    continue
                else:
                    link = section.find('a', class_=re.compile(r'^styles_wrapper'))['href']
                    price = section.find('p', class_=re.compile(r'^styles_price')).text
                    img = section.find('img', class_=re.compile(r'styles_image'))['data-src']
                    break

            db_urlname = dbmanager.get_urlname(url)
            caption = f"Новый товар в категории <u>{db_urlname}</u>\n🪧<b>{name}</b>\n💸<b>{price}</b>"
            button = types.InlineKeyboardButton(text='Открыть', url=link)
            inline_markup = types.InlineKeyboardMarkup(inline_keyboard=[[button]])

            await bot.send_photo(chat_id=config.ADMIN_ID, caption=caption, parse_mode="HTML", photo=img,
                                 reply_markup=inline_markup)
            previous_names[url] = name
        else:
            print("ok2")
    except exceptions.TelegramAPIError:
        print(f"Telegram API error occurred.")
    except Exception as e:
        print(f"An error occurred: {e}")

    await asyncio.sleep(10)
    await check_for_changes(url)