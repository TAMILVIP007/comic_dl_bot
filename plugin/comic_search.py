
from pyrogram import *
from pyrogram.types import *
import requests
from bs4 import BeautifulSoup
from pyrogram.errors.exceptions.bad_request_400 import ButtonDataInvalid
import sys

def comicsearch(client, message):
    dt = message.text
    dtSplit = dt.split(" ")
    dtSplit.remove(dtSplit[0])
    data = " "
    data = data.join(dtSplit)
    comiclink = f"https://www.comicextra.com/comic-search?key={data}"
    response = requests.get(comiclink)
    plainText = response.text
    soup = BeautifulSoup(plainText, "html.parser")
    source_url = soup.find_all('div', attrs={'class': 'cartoon-box'})
    n = []
    for links in source_url:
        title = links.find('h3').a.text
        manUrl = links.a['href'].split('/')[-1]
        n.append([InlineKeyboardButton(f"{title}", callback_data=f"but_{manUrl}")])
    if not n:
        message.reply_text("No results found, Please check the Spelling and try again")
    else:
        K = InlineKeyboardMarkup(n)
        message.reply_text(f"Your Search Results for **{data}**", reply_markup=K, parse_mode="markdown")
