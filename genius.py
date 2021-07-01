import json
import os
import sys
import random
from genius_scrape import Genius
import pickle

token = 'LJQrfZxkdEb8azPIshqa5c-XeSGKD58obsMd_k4Ao3AGS7XJCgwpyzJvIi5YVsvO'
genius = Genius(token)
f = open('saved_songs.json')
lines = json.loads(f.read())

nickname_dict = {}
try:
    nickname_dict = pickle.load( open('save.pkl', 'rb'))
except:
    pass


# preprocessing:
artists = {}
albums = {}
for line in lines:
    for key in line['artists']:
        key = key.lower()
        if key in artists:
            artists[key].append(line)
        else:
            artists[key] = [line]
    alb_key = line['album'].lower()
    if alb_key in albums:
        albums[alb_key].append(line)
    else:
        albums[alb_key] = [line]

for full_name in nickname_dict:
    if full_name in artists:
        artists[nickname_dict[full_name]] = artists[full_name]
    elif full_name in albums:
        albums[nickname_dict[full_name]] = albums[full_name]

# utility
randidx = lambda lst: random.randint(0, len(lst) - 1)
last_msg = ''

# returns what's needed from song
# line verse or full
def get_from_song(lyrics, req='line'):
    lines = lyrics.split('\n')[2:]
    verses = lyrics.split('\n\n')
    if req == 'line':
        i = randidx(lines)
        while not lines[i].strip() or '[' in lines[i]:
            i = randidx(lines)
        return '\n'.join(lines[i:i+4])
    elif req == 'verse':
        return verses[randidx(verses)]
    elif req.startswith('verse_') and len(req) >= 7:
        if req[6:].isnumeric() and int(req[6:]) < len(verses):
            return verses[int(req[6:])]
        else:
            return 'not a valid verse #'
 
    return 'Invalid (line/verse/verse_[i])'

# line from artist Kendrick Lamar
# verse from album good kid
# verse from song good kid
def get_lyrics(incoming):
    global last_msg
    if incoming == 'r':
        incoming = last_msg
    words = incoming.split()
    last_msg = incoming

    if len(words) < 4:
        return 'invalid format (length req)'
    query = ' '.join(words[3:])
    prefix = ''
    if words[2] == 'song':
        matched_songs = [line for line in lines if line['name'].lower().startswith(query)]
        if matched_songs:
            prefix = matched_songs[0]['artists'][0]
            lyrics = genius.get_lyrics(matched_songs[0]['name'], prefix)
        else:
            lyrics = genius.get_lyrics(query, '')
    elif words[2] == 'artist':
        if query in artists:
            matched_songs = artists[query]
            i = randidx(matched_songs)
            prefix = matched_songs[i]['name']
            lyrics = genius.get_lyrics(prefix, matched_songs[i]['artists'][0])
        else:
            return 'no matches'
    elif words[2] == 'album':
        if query in albums:
            matched_songs = albums[query]
            i = randidx(matched_songs)
            prefix = matched_songs[i]['name']
            lyrics = genius.get_lyrics(prefix, matched_songs[i]['artists'][0])            
        else:
            return 'no matches'
    else:
        return 'Invalid entity'

    return prefix + '\n' + get_from_song(lyrics, words[0])

f.close()

def set_nickname(incoming):
    p = open('save.pkl', 'wb')

    # nickname kendrick=kendrick lamar
    if '=' not in incoming or len(incoming) < 12:
        return 'invalid format'
    equals_indx = incoming.index('=')
    nick = incoming[9:equals_indx]
    full_name = incoming[equals_indx+1:]

    if full_name not in artists and full_name not in albums:
        return 'artist or album not found'

    if full_name in artists:
        artists[nick] = artists[full_name]
    if full_name in albums:
        albums[nick] = artists[full_name]

    nickname_dict[full_name] = nick
    pickle.dump(nickname_dict, p)
    p.close()
    return 'nickname set!'

def examples(incoming):
    # list 10 artists
    words = incoming.split()
    if len(words) < 3 or not words[1].isnumeric():
        return 'invalid'
    n = int(words[1])
    res = []
    if words[2] == 'artists':
        if n > len(artists):
            return 'too large number'
        res = random.sample(artists.keys(), n)
    elif words[2] == 'albums':
        if n > len(albums):
            return 'too large number'
        res = random.sample(albums.keys(), n)
    return '\n'.join(res)