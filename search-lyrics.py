from bs4 import BeautifulSoup
import requests

api_base_url = 'http://api.genius.com'
api_token = '<insert token here>' 

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {0}'.format(api_token)
}

def get_lyrics_from_path(song_api_path):
    song_url = api_base_url + song_api_path
    result = requests.get(song_url, headers=headers).json()
    path = result["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics

url = api_base_url + '/search'

#input song to search
title = input('Search: ')
params = {'q': title}
search_result = requests.get(url, params=params, headers=headers).json()   #request to API

#pick song from list
choice = ''
hits = search_result['response']['hits']
while not choice.isdigit() or not 0 <= int(choice) <= len(hits):
    for i, hit in enumerate(hits):
        print('({0}) {1}'.format(i, hit['result']['full_title'].encode('utf-8', 'ignore').decode('utf-8')))
    choice = input('Choose the song: ')
choice = int(choice)
song_title = hits[choice]['result']['full_title']
song_path = hits[choice]['result']['api_path']

#print lyrics
print('==========================')
print(song_title)
print('==========================')
print(get_lyrics_from_path(song_path))
