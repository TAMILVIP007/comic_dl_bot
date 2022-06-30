
from pyrogram import *
from pyrogram.types import *
import requests
from bs4 import BeautifulSoup

def comicindex2(client, callback_query):
    dataInitial = callback_query.data
    dataSplit = dataInitial.split("_")
    comicIndexNo = dataSplit[1]
    comic = dataSplit[2]
    comiclink = f"https://www.comicextra.com/comic/{comic}"
    response = requests.get(comiclink)
    plainText = response.text
    source_url = BeautifulSoup(plainText, "html.parser")
    title = souce_url.find('span', attrs={'class': 'title-1'}).text
    chapters_div = source_url.find('tbody', attrs={'id': 'list'})
    chapters = chapters_div.find_all('tr')
    lastChapList = []
    number = 1
    for _ in chapters:
        chapterNo = number
        lastChapList.append(chapterNo)
        number = number + 1
    lastChapterNo = len(lastChapList)
    listInitial = list(range(lastChapterNo))
    n = 41
    listOrganisedInitial = [listInitial[i:i + n] for i in range(0, len(listInitial), n)]
    n = [
        InlineKeyboardButton(f'{kn}', callback_data=f"pdfr_{comic}_{kn}")
        for kn in listOrganisedInitial[int(comicIndexNo)]
    ]

    m = 5
    K = [n[i:i + m] for i in range(0, len(n), m)]
    kb = InlineKeyboardMarkup(K)
    callback_query.edit_message_reply_markup(reply_markup=kb)
