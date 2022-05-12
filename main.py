import spotipy
import requests
from bs4 import BeautifulSoup
import os
from spotipy.oauth2 import SpotifyOAuth


client_id = os.environ["CLIENT_ID"]
secret_id = os.environ["SECRET_ID"]
redirect = "https://example.com"

sp = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                 client_secret=secret_id,
                                 redirect_uri=redirect,
                                 scope="playlist-modify-private",
                                 cache_path="token.txt",
                                 show_dialog=True)

sp_client = spotipy.client.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                             client_secret=secret_id,
                                                             redirect_uri=redirect,
                                                             scope="playlist-modify-private",
                                                             cache_path="token.txt",
                                                             show_dialog=True))

user_name = sp_client.current_user()["display_name"]
user_id = sp_client.current_user()["id"]

print(user_name)
print(user_id)

choice = input("What year you would like to travel to in YYY-MM-DD format: ")
year = choice.split("-")[0]
response = requests.get(f"https://www.billboard.com/charts/hot-100/{choice}")
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all(name="h3",
                      class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
song_list = [song.get_text() for song in songs]
songs_final = []


playlist = sp_client.user_playlist_create(user=user_id, name=f"{year} Billboard Top 100", public=False)
playlist_id = playlist["id"]
print(playlist_id)

for song in song_list:
    new_song = song.strip()
    songs_final.append(new_song)

print(songs_final)
print(len(songs_final))

song_uri = []
for song in songs_final:
    try:
        song_search = sp_client.search(q=f"track:{song} year:{year}",
                                   type="track")
        track_song = song_search["tracks"]["items"][0]["uri"]
        song_uri.append(track_song)

    except IndexError:
        pass
        print(f"The song {song} is not found on Spotify")


track_entry = sp_client.playlist_add_items(playlist_id=playlist_id, items=song_uri)
print(track_entry)
print(len(song_uri))

windows.mainloop()
