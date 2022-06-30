
from pyrogram import *
from pyrogram.types import *
import requests
from bs4 import BeautifulSoup
import os
import shutil
import img2pdf
import re

def comic2Pdf(client, callback_query):
    chat_id = callback_query.from_user.id
    dtInitial = callback_query.data
    dtSplit = dtInitial.split("_")
    comic = dtSplit[1]
    chapNumber = dtSplit[2]
    strSplit = comic.split("-")
    empty = " "
    comicTitle = empty.join(strSplit).title()   
    if os.path.exists(f"Download") == True:
        shutil.rmtree(f"Download")
        os.mkdir(f"Download")
    else:
        os.mkdir(f"Download")
    comiclink = f"https://www.comicextra.com/{comic}/chapter-{chapNumber}/full"
    response = requests.get(comiclink)
    plainText = response.text
    soup = BeautifulSoup(plainText, "html.parser")
    source_url = soup.find_all('img', attrs={'class': 'chapter_img'})
    comicUrlsSplit = []
    for url in source_url:
        comicUrlsSplit.append(url['src'])
        print(f"k {mangaUrlsSplit}")
        total = len(mangaUrlsSplit)
        i = 1
        for urls in comicUrlsSplit:   
            callback_query.edit_message_text(f"""DOWNLOADING NOW\nProgress: `{round((int(i)/int(total)*100))}%`""", parse_mode="markdown")
            print(f"n {urls}")       
            response = requests.get(urls)
            with open(f"Download/{i}.png", "wb") as pic:
                pic.write(response.content)
                pic.close()
            i += 1       
        callback_query.edit_message_text("""Uploading Now""", parse_mode="markdown")
        file_paths = []
        for root, directories, files in os.walk(f"Download"):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        file_paths.sort(key=lambda f: int(re.sub('\D', '', f)))

        with open(f"{chat_id}.pdf", "wb") as f:
            f.write(img2pdf.convert(file_paths))
            f.close()

        os.rename(r"{}.pdf".format(chat_id), r'{}_{}_{}pdf'.format(mangaTitle, chapNumber, chat_id))        
        client.send_document(chat_id=chat_id,
                             document='{}_{}_{}.pdf'.format(comicTitle, chapNumber, chat_id),
                             caption=f""".""", parse_mode="markdown")    

        shutil.rmtree(f"Download")
        os.remove('{}_{}_{}.pdf'.format(comicTitle, chapNumber, chat_id))
