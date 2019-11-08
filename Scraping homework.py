import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.music_ranking

url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20191107'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

'''
title = #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
artist = #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
'''

list_selector = "#body-content > div.newest-list > div > table > tbody > tr > td.info"

rank = 1
for music in soup.select(list_selector):

    title = music.select_one(".title")
    artist = music.select_one(".artist")
    print(rank,title,artist)
    rank +=1

    data = {
        'rank': rank,
        'title': title.text,
        'artist': artist.text,
    }

    db.music_ranking_1107.insert_one(data)
