from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT = os.environ.get("REDIRECT")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT,
        scope="playlist-modify-private",
        cache_path="token.txt",
        show_dialog=True
    )
)


current_id = sp.current_user()['id']


input_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
list = input_date.split()
date = f"{list[0]} {list[1]} {list[2]}"
# print(list)
responce = requests.get(f"https://www.billboard.com/charts/hot-100/{list[0]}-{list[1]}-{list[2]}/")



contents = BeautifulSoup(responce.text, "html.parser")
contents.prettify()
song_titles = [] # there are the titles of songs
# songs = contents.find_all(name="h3", id="title-of-a-story")
songs = contents.select(selector = "li h3")
for title in songs:
    name = title.string
    if name != None:
        song_titles.append(name.strip())

uri_list = []
for name in song_titles:
    result = sp.search(q=f"track:{name} year:{list[0]}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{name} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(
    current_id,
    f"{list[0]}-{list[1]}-{list[2]} Billboard 100",
    public=False,
    description= f"Top song from {date}"
)
playlist_id = playlist["id"]

add_songs = sp.playlist_add_items(playlist_id, uri_list)
