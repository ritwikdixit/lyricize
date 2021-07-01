import requests
from bs4 import BeautifulSoup
import lyricsgenius

# Credit for most of this class goes to Ratin Kumar
# https://towardsdatascience.com/become-a-lyrical-genius-4362e7710e43
#
class Genius:
    def __init__(self, token):
        self.token = token
        self.genius_helper = lyricsgenius.Genius(token)
    
    def request_song_info(self):
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + self.token}
        search_url = base_url + '/search'
        data = {'q': self.track_name + ' ' + self.track_artist}
        response = requests.get(search_url, data=data, headers=headers)
        self.response = response
        return self.response

    def check_hits(self):
        json = self.response.json()
        remote_song_info = None
        for hit in json['response']['hits']:
            if self.track_artist.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break
        self.remote_song_info = remote_song_info
        return self.remote_song_info

    def get_url(self):
        song_url = self.remote_song_info['result']['url']
        self.song_url = song_url
        return self.song_url

    def scrape_lyrics(self):
        page = requests.get(self.song_url)
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics1:
            lyrics = lyrics1.get_text()
        elif lyrics2:
            lyrics = lyrics2.get_text()
        elif lyrics1 == lyrics2 == None:
            lyrics = None
        return lyrics

    def get_lyrics(self, track_name, track_artist):
        self.track_name = track_name
        self.track_artist = track_artist
        response = self.request_song_info()
        remote_song_info = self.check_hits()
        if remote_song_info == None:
            lyrics = None
            return 'Track is not in the Genius database.1'
        url = self.get_url()
        print(url)
        return self.genius_helper.lyrics(song_url=url)