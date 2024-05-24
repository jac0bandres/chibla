import os
import json
from dotenv import load_dotenv

load_dotenv()

sp_user_id = os.getenv("SPOTIFY_TARGET")
profile_url = "https://open.spotify.com/user/{sp_user_id}"

class Profile:
    def __init__(self, user_id):
        self.user_id = user_id

    
    def ping_playlists():
        pass


class Song:
    def __init__(self, url, artist):
        self.url = url
        self.artist = artist

class Playlist:
    def __init__(self, url):
        self.url = url
        # scrape playlist contents
        self.list = []

def evaluate_playlist(pl) -> Playlist:
    evaluation = {
        "top artist" : ""
    }

    artists = []
    for song in pl.list:
        if song.artist not in pl.list:
            artists[song.artist] = 0
        elif song.artist in pl.list:
            artists[song.artist] += 1

    top_artists = ""
    for artist in artists:
        if top_artists == "":
            top_artists = artist
        
        if artists[artist] > artists[top_artists]:
            top_artists = artist[artist]
    
    return evaluation

def save_structure(structure):
    pass

def send_message(content):
    pass